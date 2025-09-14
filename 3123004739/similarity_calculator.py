from collections import Counter
import math
from word_filter import filter_stop_words
def calculate_similarity(words1, words2):
    """计算两个词列表的余弦相似度"""
    #过滤停用词
    filtered1 = filter_stop_words(words1)
    filtered2 = filter_stop_words(words2)

    # 计算词频
    counter1 = Counter(filtered1)
    counter2 = Counter(filtered2)

    # 获取所有独特的词
    all_words = set(counter1.keys()).union(set(counter2.keys()))

    # 计算点积
    dot_product = 0
    for word in all_words:
        dot_product += counter1.get(word, 0) * counter2.get(word, 0)

    # 计算向量长度
    norm1 = math.sqrt(sum(count ** 2 for count in counter1.values()))
    norm2 = math.sqrt(sum(count ** 2 for count in counter2.values()))

    # 处理空文本情况
    if norm1 == 0 or norm2 == 0:
        return 0.0

    # 计算余弦相似度
    return dot_product / (norm1 * norm2)