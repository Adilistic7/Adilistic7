import sys
from read_file import read_file
from similarity_calculator import calculate_similarity
from text_processor import preprocess_text

def main():
    # 检查命令行参数是否正确
    if len(sys.argv) != 4:
        print("用法: python main.py [原文文件] [抄袭版论文的文件] [答案文件]")
        sys.exit(1)

    # 获取文件路径
    orig_path = sys.argv[1]
    copy_path = sys.argv[2]
    result_path = sys.argv[3]

    # 读取文件内容
    orig_text = read_file(orig_path)
    copy_text = read_file(copy_path)

    # 预处理文本
    orig_words = preprocess_text(orig_text)
    copy_words = preprocess_text(copy_text)

    # 计算相似度（重复率）
    similarity = calculate_similarity(orig_words, copy_words)

    # 将结果写入输出文件，精确到小数点后两位
    try:
        with open(result_path, 'w', encoding='utf-8') as file:
            file.write(f"{similarity:.2f}")
    except Exception as e:
        print(f"写入文件错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
