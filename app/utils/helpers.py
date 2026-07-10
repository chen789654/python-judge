"""工具函数"""
import os
import re
import string
import random


def generate_invite_code(length=6):
    """生成班级邀请码"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def sanitize_filename(filename):
    """清理文件名中的危险字符"""
    return re.sub(r'[^\w\-_.]', '_', filename)


def ensure_dir(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)
    return path


def truncate_text(text, max_length=200):
    """截断文本"""
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text


def parse_tags(tag_string):
    """解析逗号分隔的标签为列表"""
    return [t.strip() for t in tag_string.split(',') if t.strip()]
