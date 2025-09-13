import jieba
def preprocess_text(text):
    """文本预处理：分词并过滤标点符号等"""
    # 使用jieba进行中文分词
    words = jieba.cut(text)

    # 过滤标点符号和空白字符
    filtered_words = []
    for word in words:
        # 保留有实际意义的词语
        if word.strip() and not word.strip().isdigit() and len(word.strip()) > 0:
            filtered_words.append(word.strip())

    return filtered_words