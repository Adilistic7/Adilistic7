from prepare_text import preprocess_text
from replace_synonyms  import replace_synonyms


def calculate_lcs_similarity(text1, text2):
    """计算基于最长公共子序列的相似度"""
    # 预处理文本
    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)

    # 同义词替换
    words1 = replace_synonyms(words1)
    words2 = replace_synonyms(words2)

    if not words1 or not words2:
        return 0.0

    # 计算公共词汇比例
    common_words = set(words1) & set(words2)
    similarity = len(common_words) / min(len(set(words1)), len(set(words2)))

    return similarity
