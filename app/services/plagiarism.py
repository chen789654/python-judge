"""
代码查重模块

算法：
1. Token规范化后Jaccard相似度
2. Token序列n-gram结构相似度
3. 变量命名模式相似度（检测重命名）
4. 最终加权综合得分
"""
import re
from collections import Counter

# Python关键字（不参与变量名比对）
KEYWORDS = {
    'if', 'else', 'elif', 'for', 'while', 'in', 'not', 'and', 'or',
    'is', 'def', 'class', 'return', 'yield', 'import', 'from', 'as',
    'try', 'except', 'finally', 'raise', 'with', 'pass', 'break',
    'continue', 'lambda', 'True', 'False', 'None', 'print', 'range',
    'len', 'int', 'str', 'float', 'list', 'dict', 'set', 'tuple',
    'type', 'input', 'open', 'map', 'filter', 'zip', 'enumerate',
    'sorted', 'reversed', 'abs', 'max', 'min', 'sum', 'any', 'all',
    'self', 'super', 'global', 'nonlocal', 'del', 'assert',
}


def tokenize_code(source_code):
    """将Python代码转换为token序列"""
    code = re.sub(r'#.*$', '', source_code, flags=re.MULTILINE)
    code = re.sub(r'"""[\s\S]*?"""', '', code)
    code = re.sub(r"'''[\s\S]*?'''", '', code)
    code = re.sub(r'"[^"]*"', '"STR"', code)
    code = re.sub(r"'[^']*'", "'STR'", code)
    tokens = re.findall(r'[a-zA-Z_]\w*|[{}()\[\];,.:=+\-*/%&|^~<>!@]', code)
    return tokens


def normalize_tokens(tokens):
    """规范化token：变量→VAR，数字→NUM，关键字保留"""
    normalized = []
    user_vars = []  # 记录变量名用于命名模式分析
    for t in tokens:
        if t.isidentifier() and t not in KEYWORDS:
            normalized.append('VAR')
            user_vars.append(t)
        elif t.isdigit() or (t.startswith('-') and t[1:].isdigit()):
            normalized.append('NUM')
        else:
            normalized.append(t)
    return normalized, user_vars


def extract_structure_tokens(tokens):
    """提取结构token（只看分支、循环、函数定义等结构关键字）"""
    structural = {'if', 'else', 'elif', 'for', 'while', 'def', 'class',
                  'try', 'except', 'return', 'break', 'continue', 'with'}
    return [t for t in tokens if t in structural]


def compute_similarity(code1, code2):
    """
    综合相似度计算 (0.0 ~ 1.0)

    加权组合：
    - 结构相似度 30%（控制流结构）
    - Token序列相似度 40%（n-gram）
    - 变量命名模式相似度 30%（检测简单重命名）
    """
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)

    if not tokens1 or not tokens2:
        return 0.0

    norm1, vars1 = normalize_tokens(tokens1)
    norm2, vars2 = normalize_tokens(tokens2)

    # 1. 结构相似度（控制流关键字）
    struct1 = extract_structure_tokens(tokens1)
    struct2 = extract_structure_tokens(tokens2)
    struct_sim = _sequence_similarity(struct1, struct2)

    # 2. Token序列相似度（n-gram）
    ngram_sim = _ngram_similarity(norm1, norm2, n=5)

    # 3. 变量命名模式相似度
    naming_sim = _varname_similarity(vars1, vars2)

    # 加权综合
    similarity = struct_sim * 0.30 + ngram_sim * 0.40 + naming_sim * 0.30

    return round(similarity, 4)


def _sequence_similarity(seq1, seq2):
    """序列相似度（改进版Jaccard）"""
    if not seq1 or not seq2:
        return 0.0
    set1, set2 = set(seq1), set(seq2)
    inter = set1 & set2
    union = set1 | set2
    return len(inter) / len(union) if union else 0


def _ngram_similarity(norm1, norm2, n=5):
    """n-gram序列相似度"""
    if len(norm1) < n or len(norm2) < n:
        # 短代码使用直接序列比对
        return _lcs_similarity(norm1, norm2)

    ngram1 = set(tuple(norm1[i:i+n]) for i in range(len(norm1) - n + 1))
    ngram2 = set(tuple(norm2[i:i+n]) for i in range(len(norm2) - n + 1))

    if not ngram1 or not ngram2:
        return 0.0

    inter = ngram1 & ngram2
    union = ngram1 | ngram2
    return len(inter) / len(union) if union else 0


def _lcs_similarity(a, b):
    """基于LCS的相似度"""
    if not a or not b:
        return 0.0
    lcs_len = _lcs_length(a, b)
    return (2 * lcs_len) / (len(a) + len(b)) if (len(a) + len(b)) > 0 else 0


def _lcs_length(a, b):
    """最长公共子序列长度（空间优化版）"""
    n, m = len(a), len(b)
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


def _varname_similarity(vars1, vars2):
    """变量命名模式相似度"""
    if not vars1 or not vars2:
        return 0.0

    # 变量名长度分布相似度
    lengths1 = [len(v) for v in vars1]
    lengths2 = [len(v) for v in vars2]

    # 变量名风格统计（下划线、缩写、完整单词比例）
    def name_style(vars_list):
        short = sum(1 for v in vars_list if len(v) <= 2)
        has_underscore = sum(1 for v in vars_list if '_' in v)
        return (short / len(vars_list), has_underscore / len(vars_list))

    style1 = name_style(vars1)
    style2 = name_style(vars2)

    # 长度分布相似度
    if len(lengths1) == len(lengths2):
        match = sum(1 for a, b in zip(lengths1, lengths2) if a == b)
        len_sim = match / len(lengths1)
    else:
        len_sim = 0.5  # 长度不同时取中值

    # 风格相似度
    style_sim = 1.0 - min(1.0,
        abs(style1[0] - style2[0]) + abs(style1[1] - style2[1]))

    return len_sim * 0.5 + style_sim * 0.5


def highlight_diff(code_a, code_b):
    """
    对两段代码进行逐行diff，返回带高亮标记的HTML行列表
    返回: (lines_a, lines_b) 每项是 (text, class)
    class: 'same' / 'changed' / 'added' / 'removed'
    """
    lines_a = code_a.split('\n')
    lines_b = code_b.split('\n')

    # 简单的逐行比对
    max_len = max(len(lines_a), len(lines_b))
    result_a, result_b = [], []

    # 使用简单的LCS匹配行
    m, n = len(lines_a), len(lines_b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if lines_a[i-1].strip() == lines_b[j-1].strip():
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # 回溯找到对齐
    i, j = m, n
    aligned_a, aligned_b = [], []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and lines_a[i-1].strip() == lines_b[j-1].strip():
            aligned_a.append((lines_a[i-1], 'same'))
            aligned_b.append((lines_b[j-1], 'same'))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j-1] >= dp[i-1][j]):
            aligned_a.append(('', 'added'))
            aligned_b.append((lines_b[j-1], 'added'))
            j -= 1
        else:
            aligned_a.append((lines_a[i-1], 'removed'))
            aligned_b.append(('', 'removed'))
            i -= 1

    aligned_a.reverse()
    aligned_b.reverse()
    return aligned_a, aligned_b


def find_plagiarism(problem_id, threshold=0.75, limit_submissions=100):
    """
    对某道题的所有提交进行两两查重

    返回:
        [{ submission_a, submission_b, similarity,
           student_a, student_b, class_a, class_b,
           score_a, score_b, time_a, time_b }, ...]
    """
    from app.models import Submission

    submissions = Submission.query.filter_by(problem_id=problem_id)\
        .order_by(Submission.submitted_at.desc())\
        .limit(limit_submissions).all()

    results = []
    checked = set()

    for i in range(len(submissions)):
        for j in range(i + 1, len(submissions)):
            sa, sb = submissions[i], submissions[j]
            key = (min(sa.id, sb.id), max(sa.id, sb.id))
            if key in checked:
                continue
            checked.add(key)

            sim = compute_similarity(sa.source_code, sb.source_code)
            if sim >= threshold:
                results.append({
                    'submission_a': sa.id,
                    'submission_b': sb.id,
                    'similarity': sim,
                    'student_a': sa.author.username,
                    'student_b': sb.author.username,
                    'realname_a': sa.author.real_name or sa.author.username,
                    'realname_b': sb.author.real_name or sb.author.username,
                    'class_a': sa.author.class_.name if sa.author.class_ else '-',
                    'class_b': sb.author.class_.name if sb.author.class_ else '-',
                    'score_a': sa.score,
                    'score_b': sb.score,
                    'time_a': sa.submitted_at.strftime('%m-%d %H:%M'),
                    'time_b': sb.submitted_at.strftime('%m-%d %H:%M'),
                })

    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results
