from calculate_lcs_similarity import calculate_lcs_similarity
from calculate_word_frequency_similarity import calculate_word_frequency_similarity
from calculate_similarity import calculate_similarity

# 扩展停用词列表
STOP_WORDS = {(
    '的','了','在','是','我','有','和','就','不','人','都','一','一个','上','也','很','到','说','要',
     '去','你','会','着','没有','看','好','自己','这','那','就','和','与','及','或','等','可以','能够',
     '需要','应该','必须','着','了','过')}







def advanced_plagiarism_check(original_text, suspicious_text):
    """
    高级抄袭检测函数
    结合多种方法提高检测准确性
    """
    # 方法1: TF-IDF余弦相似度
    tfidf_similarity = calculate_similarity(original_text, suspicious_text)

    # 方法2: 最长公共子序列比例（检测改写抄袭）
    lcs_ratio = calculate_lcs_similarity(original_text, suspicious_text)

    # 方法3: 基于词频的相似度
    word_freq_similarity = calculate_word_frequency_similarity(original_text, suspicious_text)

    # 动态权重分配
    # 对于高度相似的文本，降低TF-IDF权重，提高其他方法的权重
    if tfidf_similarity > 0.9:
        # 高度相似，可能只是表面改写，降低TF-IDF权重
        final_similarity = 0.4 * tfidf_similarity + 0.4 * lcs_ratio + 0.2 * word_freq_similarity
    else:
        # 一般相似度，使用正常权重
        final_similarity = 0.6 * tfidf_similarity + 0.3 * lcs_ratio + 0.1 * word_freq_similarity

    return min(final_similarity, 1.0)  # 确保不超过1.0

