"""
代码查重模块

使用Token序列比对算法检测代码相似度，
帮助教师发现抄袭行为。
"""
import re
import math


def tokenize_code(source_code):
    """
    将Python代码转换为token序列用于比对

    移除注释、字符串字面量和空白，提取关键字和标识符
    """
    # 移除注释
    code = re.sub(r'#.*$', '', source_code, flags=re.MULTILINE)
    # 移除多行字符串
    code = re.sub(r'"""[\s\S]*?"""', '', code)
    code = re.sub(r"'''[\s\S]*?'''", '', code)
    # 移除单行字符串（保留结构）
    code = re.sub(r'"[^"]*"', '"STR"', code)
    code = re.sub(r"'[^']*'", "'STR'", code)

    # 提取tokens
    tokens = re.findall(r'[a-zA-Z_]\w*|[{}()\[\];,.:=+\-*/%&|^~<>!@]', code)

    return tokens


def normalize_tokens(tokens):
    """
    规范化token序列：
    - 变量名统一为 VAR
    - 数字统一为 NUM
    """
    normalized = []
    for t in tokens:
        if t.isidentifier() and t not in [
            'if', 'else', 'elif', 'for', 'while', 'in', 'not', 'and', 'or',
            'is', 'def', 'class', 'return', 'yield', 'import', 'from', 'as',
            'try', 'except', 'finally', 'raise', 'with', 'pass', 'break',
            'continue', 'lambda', 'True', 'False', 'None', 'print', 'range',
            'len', 'int', 'str', 'float', 'list', 'dict', 'set', 'tuple',
            'type', 'input', 'open', 'map', 'filter', 'zip', 'enumerate',
            'sorted', 'reversed', 'abs', 'max', 'min', 'sum', 'any', 'all',
            'self', 'super', 'global', 'nonlocal', 'del', 'assert',
        ]:
            normalized.append('VAR')
        elif t.isdigit() or (t.startswith('-') and t[1:].isdigit()):
            normalized.append('NUM')
        else:
            normalized.append(t)
    return normalized


def compute_similarity(code1, code2):
    """
    计算两段代码的相似度 (0.0 ~ 1.0)

    算法: 基于Token序列的Jaccard相似度 + 最长公共子序列(LCS)
    """
    tokens1 = normalize_tokens(tokenize_code(code1))
    tokens2 = normalize_tokens(tokenize_code(code2))

    if not tokens1 or not tokens2:
        return 0.0

    # 方法1: Jaccard相似度
    set1 = set(tokens1)
    set2 = set(tokens2)
    intersection = set1 & set2
    union = set1 | set2
    jaccard = len(intersection) / len(union) if union else 0

    # 方法2: 序列相似度 (基于公共子序列长度)
    n, m = len(tokens1), len(tokens2)
    if n > 200 or m > 200:
        # 长代码使用简化的n-gram方法
        ngram_size = 5
        ngram1 = set(tuple(tokens1[i:i+ngram_size])
                     for i in range(len(tokens1) - ngram_size + 1))
        ngram2 = set(tuple(tokens2[i:i+ngram_size])
                     for i in range(len(tokens2) - ngram_size + 1))
        if ngram1 and ngram2:
            ng_intersection = ngram1 & ngram2
            ng_union = ngram1 | ngram2
            sequence_sim = len(ng_intersection) / len(ng_union) if ng_union else 0
        else:
            sequence_sim = 0
    else:
        # 短代码使用LCS
        lcs_len = _lcs_length(tokens1, tokens2)
        sequence_sim = (2 * lcs_len) / (n + m) if (n + m) > 0 else 0

    # 综合得分: Jaccard 40% + 序列相似度 60%
    similarity = jaccard * 0.4 + sequence_sim * 0.6

    return round(similarity, 4)


def _lcs_length(a, b):
    """计算最长公共子序列长度 (空间优化版)"""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 0
    # 只保留两行
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
    return prev[m]


def find_plagiarism(problem_id, threshold=0.75, limit_submissions=100):
    """
    对某道题的所有提交进行两两查重

    参数:
        problem_id: 题目ID
        threshold: 相似度阈值，高于此值标记为可疑
        limit_submissions: 最多检查的提交数（最新的N条）

    返回:
        [(sub1_id, sub2_id, similarity), ...]
    """
    from app.models import Submission

    submissions = Submission.query.filter_by(problem_id=problem_id)\
        .order_by(Submission.submitted_at.desc())\
        .limit(limit_submissions).all()

    results = []
    checked = set()

    for i in range(len(submissions)):
        for j in range(i + 1, len(submissions)):
            key = (min(submissions[i].id, submissions[j].id),
                   max(submissions[i].id, submissions[j].id))
            if key in checked:
                continue
            checked.add(key)

            sim = compute_similarity(submissions[i].source_code,
                                     submissions[j].source_code)
            if sim >= threshold:
                results.append({
                    'submission_a': submissions[i].id,
                    'submission_b': submissions[j].id,
                    'similarity': sim,
                    'student_a': submissions[i].author.username,
                    'student_b': submissions[j].author.username,
                })

    # 按相似度降序排列
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results
