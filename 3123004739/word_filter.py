# 中文停用词列表（可根据需求扩展）
STOP_WORDS = {
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "到", "说",
    "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这", "今天", "天气", "晚上"
}
def filter_stop_words(words):
    """过滤停用词"""
    return [word for word in words if word not in STOP_WORDS and len(word) > 0]