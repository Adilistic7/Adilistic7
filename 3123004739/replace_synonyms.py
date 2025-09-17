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