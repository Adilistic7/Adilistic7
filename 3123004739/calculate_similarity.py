from sklearn.feature_extraction.text import TfidfVectorizer
from prepare_text import preprocess_text
from replace_synonyms import replace_synonyms
import jieba

def calculate_similarity(text1, text2):
    """
    计算两篇文本的相似度
    返回0-1之间的相似度分数
    """
    # 预处理文本
    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)

    # 同义词替换
    words1 = replace_synonyms(words1)
    words2 = replace_synonyms(words2)

    # 如果文本过短，直接返回低相似度
    if len(words1) < 20 or len(words2) < 20:
        return 0.0

    # 提取关键词（减少常见词的影响）
    keywords1 = jieba.analyse.extract_tags(' '.join(words1), topK=50)
    keywords2 = jieba.analyse.extract_tags(' '.join(words2), topK=50)

    # 将分词结果转换为字符串
    text1_processed = ' '.join(keywords1)
    text2_processed = ' '.join(keywords2)

    # 创建TF-IDF向量器，使用1-2gram
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    try:
        # 计算TF-IDF矩阵
        tfidf_matrix = vectorizer.fit_transform([text1_processed, text2_processed])

        # 计算余弦相似度
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        return similarity
    except Exception as e:
        print(f"计算相似度时出错: {e}")
        return 0.0