from collections import Counter
from prepare_text import preprocess_text
from replace_synonyms import replace_synonyms

def calculate_word_frequency_similarity(text1, text2):
    """计算基于词频分布的相似度"""
    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)

    # 同义词替换
    words1 = replace_synonyms(words1)
    words2 = replace_synonyms(words2)

    if not words1 or not words2:
        return 0.0

    # 计算词频
    freq1 = Counter(words1)
    freq2 = Counter(words2)

    # 计算余弦相似度
    all_words = set(freq1.keys()) | set(freq2.keys())
    vector1 = [freq1.get(word, 0) for word in all_words]
    vector2 = [freq2.get(word, 0) for word in all_words]

    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = sum(a ** 2 for a in vector1) ** 0.5
    magnitude2 = sum(b ** 2 for b in vector2) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)
