import re
import jieba

def preprocess_text(text):
    """文本预处理函数"""
    # 去除标点符号和数字
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)

    # 中文分词
    words = jieba.cut(text)

    # 去除停用词和单字词
    words = [word for word in words if word not in STOP_WORDS and len(word) > 1]

    return words