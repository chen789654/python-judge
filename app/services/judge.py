"""
┌──────────────────────────────────────────────────────────────┐
│                Python 代码自动评分引擎                         │
│                                                              │
│  核心功能：在安全沙箱中执行学生提交的代码，                      │
│  逐测试用例比对输出，返回得分和运行结果                         │
└──────────────────────────────────────────────────────────────┘

执行流程:
  1. 接收源代码 + 测试用例列表
  2. 将代码写入临时文件
  3. 对每个测试用例:
     a. 构造 stdin 输入
     b. 在受限环境中执行代码 (subprocess)
     c. 捕获 stdout, stderr, 运行时间, 内存
     d. 比对实际输出与期望输出
     e. 记录该用例得分
  4. 汇总总分 → 返回结果
  5. 清理临时文件
"""
import os
import sys
import uuid
import signal
import subprocess
import tempfile
import threading
from datetime import datetime
from flask import current_app
from app.extensions import db


class JudgeResult:
    """一次提交的完整评测结果"""
    def __init__(self):
        self.status = 'pending'           # pending / accepted / wrong / error
        self.score = 0.0
        self.max_score = 0.0
        self.exec_time = 0.0              # 总执行时间(ms)
        self.memory_used = 0.0            # 最大内存使用(KB)
        self.compiler_message = ''        # 错误信息
        self.test_results = []            # 每条用例的结果


class TestCaseResult:
    """单个测试用例的执行结果"""
    def __init__(self):
        self.test_case_id = None
        self.passed = False
        self.actual_output = ''
        self.expected_output = ''
        self.score_earned = 0.0
        self.exec_time = 0.0


class CodeJudge:
    """
    代码评测器

    用法:
        judge = CodeJudge()
        result = judge.run(source_code, test_cases, max_score=100)
    """

    def __init__(self):
        self.config = {
            'max_cpu_time': current_app.config.get('JUDGE_MAX_CPU_TIME', 5),
            'max_memory': current_app.config.get('JUDGE_MAX_MEMORY', 256 * 1024),
            'max_code_length': current_app.config.get('JUDGE_MAX_CODE_LENGTH', 10000),
            'temp_dir': current_app.config.get('JUDGE_TEMP_DIR',
                                                os.path.join(os.getcwd(), 'sandbox')),
        }
        os.makedirs(self.config['temp_dir'], exist_ok=True)

        # 禁止导入的危险模块列表
        self.forbidden_modules = [
            'os', 'sys', 'subprocess', 'shutil', 'socket',
            'ctypes', 'signal', 'multiprocessing', 'threading',
            'importlib', 'code', 'codeop', 'compileall',
            'inspect', 'ast', 'py_compile', 'zipimport',
            'pdb', 'trace', 'webbrowser', 'antigravity',
        ]

    # ────────────────────────────────────────────
    # 安全校验
    # ────────────────────────────────────────────
    def validate_code(self, source_code):
        """检查代码安全性"""
        errors = []

        # 检查代码长度
        if len(source_code) > self.config['max_code_length']:
            errors.append(f'代码过长（{len(source_code)}字符），最大允许{self.config["max_code_length"]}字符')
            return errors

        # 检查禁止的危险模块
        for mod in self.forbidden_modules:
            # import xxx
            pattern1 = rf'^\s*import\s+{mod}\s*$'
            # from xxx import ...
            pattern2 = rf'^\s*from\s+{mod}\s+import'
            # __import__('xxx')
            pattern3 = rf"__import__\s*\(\s*['\"]{mod}['\"]\s*\)"

            for line in source_code.split('\n'):
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if (re.search(pattern1, stripped, re.MULTILINE) or
                    re.search(pattern2, stripped, re.MULTILINE) or
                    re.search(pattern3, stripped)):
                    errors.append(f'禁止使用危险模块: {mod}')
                    break

        # 检查 eval/exec/compile
        dangerous_calls = ['eval(', 'exec(', 'compile(', '__import__(']
        for call in dangerous_calls:
            if call in source_code:
                errors.append(f'禁止使用危险函数: {call}')

        return errors

    # ────────────────────────────────────────────
    # 代码执行
    # ────────────────────────────────────────────
    def _execute_code(self, source_code, stdin_input, file_id):
        """
        在子进程中执行Python代码

        参数:
            source_code: Python源代码
            stdin_input: 标准输入字符串
            file_id: 唯一标识，用于临时文件

        返回:
            (stdout, stderr, exec_time, timed_out)
        """
        # 写临时文件
        filename = f'submission_{file_id}.py'
        filepath = os.path.join(self.config['temp_dir'], filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(source_code)

        try:
            # 构造执行命令
            cmd = [
                sys.executable,              # 当前Python解释器
                '-W', 'ignore',              # 忽略警告
                filepath,
            ]

            # 执行并计时
            start_time = datetime.now()

            proc = subprocess.run(
                cmd,
                input=stdin_input,
                capture_output=True,
                text=True,
                timeout=self.config['max_cpu_time'],
                cwd=self.config['temp_dir'],
                env={                        # 清空环境变量，提高安全性
                    'PATH': os.environ.get('PATH', ''),
                    'HOME': self.config['temp_dir'],
                },
            )

            end_time = datetime.now()
            exec_time = (end_time - start_time).total_seconds() * 1000  # 转为ms

            stdout = proc.stdout
            stderr = proc.stderr

            return stdout, stderr, exec_time, False

        except subprocess.TimeoutExpired:
            return '', '错误: 程序运行超时', self.config['max_cpu_time'] * 1000, True
        except Exception as e:
            return '', f'运行时错误: {str(e)}', 0, False
        finally:
            # 清理临时文件
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                # 清理可能的 __pycache__
                cache_dir = os.path.join(self.config['temp_dir'], '__pycache__')
                if os.path.exists(cache_dir):
                    import shutil
                    shutil.rmtree(cache_dir, ignore_errors=True)
            except Exception:
                pass

    # ────────────────────────────────────────────
    # 输出比对
    # ────────────────────────────────────────────
    def _compare_output(self, actual, expected):
        """
        比对实际输出与期望输出
        采用规范化比对: 去除首尾空白，统一换行符
        """
        if actual is None:
            actual = ''
        if expected is None:
            expected = ''

        actual = actual.rstrip('\n').rstrip('\r').rstrip()
        expected = expected.rstrip('\n').rstrip('\r').rstrip()

        return actual == expected

    # ────────────────────────────────────────────
    # 主评测入口
    # ────────────────────────────────────────────
    def run(self, source_code, test_cases, max_score=100):
        """
        执行完整评测

        参数:
            source_code: 学生提交的Python源代码
            test_cases: 测试用例列表，每项为TestCase对象
            max_score: 本题满分

        返回:
            JudgeResult对象
        """
        result = JudgeResult()
        result.max_score = max_score

        # 1. 安全校验
        errors = self.validate_code(source_code)
        if errors:
            result.status = 'error'
            result.compiler_message = ';\n'.join(errors)
            return result

        # 2. 计算所有公开用例总分权重
        total_weight = sum(tc.score_weight for tc in test_cases)
        if total_weight == 0:
            total_weight = len(test_cases)

        # 3. 逐一执行测试用例
        file_id = uuid.uuid4().hex[:12]
        total_score = 0.0
        max_exec_time = 0.0
        all_passed = True
        has_public = False
        has_hidden = False

        for tc in test_cases:
            tc_result = TestCaseResult()
            tc_result.test_case_id = tc.id
            tc_result.expected_output = tc.expected_output or ''

            if tc.is_public:
                has_public = True
            else:
                has_hidden = True

            # 执行代码
            stdout, stderr, exec_time, timed_out = self._execute_code(
                source_code,
                tc.input_data or '',
                f'{file_id}_{tc.id}',
            )

            tc_result.exec_time = exec_time
            tc_result.actual_output = stdout
            max_exec_time = max(max_exec_time, exec_time)

            # 判分
            if stderr and not timed_out:
                # 有错误输出
                tc_result.passed = False
                tc_result.score_earned = 0.0
                all_passed = False
                result.compiler_message = stderr
            elif timed_out:
                tc_result.passed = False
                tc_result.score_earned = 0.0
                all_passed = False
            else:
                passed = self._compare_output(stdout, tc.expected_output)
                tc_result.passed = passed
                if passed:
                    weight_ratio = tc.score_weight / total_weight
                    tc_result.score_earned = round(max_score * weight_ratio, 2)
                    total_score += tc_result.score_earned
                else:
                    all_passed = False

            result.test_results.append(tc_result)

        # 4. 汇总结果
        result.score = round(total_score, 2)
        result.exec_time = round(max_exec_time, 2)

        if all_passed and len(test_cases) > 0:
            result.status = 'accepted'
        elif not result.compiler_message:
            result.status = 'wrong'
        else:
            result.status = 'error'

        return result


# ────────────────────────────────────────────
# 便捷函数：直接评测并存入数据库
# ────────────────────────────────────────────
def judge_submission(submission):
    """
    对一条Submission进行评测，更新数据库结果

    参数:
        submission: Submission模型实例

    返回:
        更新后的submission
    """
    from app.models import TestResult as TRModel

    judge = CodeJudge()

    # 获取该题的所有测试用例
    test_cases = submission.problem.test_cases.order_by(TestCase.sort_order).all()

    # 执行评测
    result = judge.run(submission.source_code, test_cases, max_score=100)

    # 更新提交记录
    submission.status = result.status
    submission.score = result.score
    submission.max_score = result.max_score
    submission.exec_time = result.exec_time
    submission.compiler_message = result.compiler_message
    submission.judged_at = datetime.utcnow()

    # 删除旧的测试结果（重新评测时）
    TRModel.query.filter_by(submission_id=submission.id).delete()

    # 写入每条测试用例结果
    for tc_result in result.test_results:
        tr = TRModel(
            submission_id=submission.id,
            test_case_id=tc_result.test_case_id,
            actual_output=tc_result.actual_output,
            passed=tc_result.passed,
            score_earned=tc_result.score_earned,
            exec_time=tc_result.exec_time,
        )
        db.session.add(tr)

    # 自动生成评语和等级
    submission.auto_comment = submission.generate_auto_comment()
    submission.grade_level = submission.calc_grade_level()

    # 更新题目的统计数据
    problem = submission.problem
    problem.total_submissions = (problem.total_submissions or 0) + 1
    if submission.status == 'accepted':
        problem.accepted_submissions = (problem.accepted_submissions or 0) + 1

    db.session.commit()
    return submission


# 延迟导入避免循环
from app.models import TestCase
