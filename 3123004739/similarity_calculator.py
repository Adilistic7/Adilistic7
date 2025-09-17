import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import jieba
import jieba.analyse
from collections import Counter
import sys
import os

# 扩展停用词列表
STOP_WORDS = set(
    ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要',
     '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '就', '和', '与', '及', '或', '等', '可以', '能够',
     '需要', '应该', '必须', '着', '了', '过'])

# 同义词词典（简化版，实际应用中应该使用更完整的同义词库）
SYNONYMS = {
    '研究': ['探究', '探讨', '分析', '调查'],
    '应用': ['运用', '使用', '利用', '采用'],
    '发展': ['进步', '进展', '成长', '壮大'],
    '技术': ['科技', '技艺', '方法', '手段'],
    '教育': ['教学', '教导', '培养', '培育'],
    '系统': ['体系', '系统', '制度', '机制'],
    '数据': ['信息', '资料', '数值', '数字'],
    '学习': ['学业', '研习', '修习', '攻读'],
    '挑战': ['难题', '困难', '问题', '障碍'],
    '趋势': ['动向', '方向', '潮流', '态势']
}


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


def replace_synonyms(words):
    """将同义词替换为标准词，减少同义词造成的差异"""
    result = []
    for word in words:
        # 查找同义词
        replaced = False
        for standard, synonyms in SYNONYMS.items():
            if word in synonyms:
                result.append(standard)
                replaced = True
                break

        # 如果没有找到同义词，保留原词
        if not replaced:
            result.append(word)

    return result


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


def main():
    """主函数：处理命令行参数并执行抄袭检测"""
    # 检查命令行参数数量
    if len(sys.argv) != 4:
        print("用法: python main.py <源文章地址> <抄袭文章地址> <输出结果文件地址>")
        sys.exit(1)

    # 获取命令行参数
    original_file = sys.argv[1]
    suspicious_file = sys.argv[2]
    output_file = sys.argv[3]

    # 检查文件是否存在
    if not os.path.exists(original_file):
        print(f"错误: 源文件 '{original_file}' 不存在")
        sys.exit(1)

    if not os.path.exists(suspicious_file):
        print(f"错误: 疑似抄袭文件 '{suspicious_file}' 不存在")
        sys.exit(1)

    # 读取文件内容
    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            original_text = f.read()

        with open(suspicious_file, 'r', encoding='utf-8') as f:
            suspicious_text = f.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        sys.exit(1)

    # 计算相似度
    try:
        similarity = advanced_plagiarism_check(original_text, suspicious_text)
    except Exception as e:
        print(f"计算相似度时出错: {e}")
        sys.exit(1)

    # 输出结果到文件和屏幕
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"源文件: {original_file}\n")
            f.write(f"疑似抄袭文件: {suspicious_file}\n")
            f.write(f"相似度: {similarity:.2%}\n")
            f.write(f"详细结果:\n")

            if similarity < 0.3:
                f.write("结果: 两篇文章相似度较低，可能不存在抄袭\n")
            elif similarity < 0.6:
                f.write("结果: 两篇文章有一定相似度，可能存在部分借鉴\n")
            elif similarity < 0.8:
                f.write("结果: 两篇文章相似度较高，可能存在大量抄袭\n")
            else:
                f.write("结果: 两篇文章非常相似，极有可能存在抄袭\n")

        # 同时在屏幕上显示结果
        print(f"检测完成!")
        print(f"源文件: {original_file}")
        print(f"疑似抄袭文件: {suspicious_file}")
        print(f"相似度: {similarity:.2%}")

        if similarity < 0.3:
            print("结果: 两篇文章相似度较低，可能不存在抄袭")
        elif similarity < 0.6:
            print("结果: 两篇文章有一定相似度，可能存在部分借鉴")
        elif similarity < 0.8:
            print("结果: 两篇文章相似度较高，可能存在大量抄袭")
        else:
            print("结果: 两篇文章非常相似，极有可能存在抄袭")

        print(f"详细结果已保存至: {output_file}")

    except Exception as e:
        print(f"写入结果文件时出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()