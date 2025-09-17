import sys
import os
from similarity_calculator import advanced_plagiarism_check

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
    # 将前面定义的函数放在这里，或者导入它们
    # 这里假设所有函数都已经定义或导入
    main()