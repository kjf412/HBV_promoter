import argparse
import sys

def extract_gene_names(input_file, output_file):
    """
    从FASTA文件中读取内容，提取基因名称，并写入输出文件。

    :param input_file: 输入的FASTA文件名
    :param output_file: 输出的文本文件名
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            print(f"正在读取文件: {input_file}...")
            count = 0
            for line in infile:
                # 检查是否为标题行
                if line.startswith('>'):
                    # 去除行首的'>'和行尾的换行符
                    header = line.strip()[1:]
                    
                    # 按第一个空格分割，获取基因名称
                    # split(maxsplit=1) 确保只在第一个空格处分割
                    try:
                        gene_name = header.split(maxsplit=1)[0]
                        
                        # 将基因名称写入输出文件，并添加换行符
                        outfile.write(gene_name + '\n')
                        count += 1
                    except IndexError:
                        # 处理可能是空标题行的情况 (例如 ">")
                        print(f"警告: 发现一个空的或格式不正确的标题行: {line.strip()}", file=sys.stderr)

            print(f"处理完成。共提取了 {count} 个基因名称到 {output_file}")

    except FileNotFoundError:
        print(f"错误: 无法找到输入文件 '{input_file}'", file=sys.stderr)
    except Exception as e:
        print(f"发生了一个未预料的错误: {e}", file=sys.stderr)

def main():
    """
    主函数，用于解析命令行参数并调用提取功能。
    """
    # 1. 初始化参数解析器
    parser = argparse.ArgumentParser(
        description="从FASTA文件中提取基因名称 (例如 'AF046996.1')."
    )
    
    # 2. 添加必需的参数
    parser.add_argument(
        "input_file", 
        type=str,
        help="输入的FASTA文件名"
    )
    parser.add_argument(
        "output_file", 
        type=str,
        help="用于保存提取名称的输出文件名"
    )
    
    # 3. 解析命令行参数
    args = parser.parse_args()
    
    # 4. 调用核心处理函数
    extract_gene_names(args.input_file, args.output_file)

if __name__ == "__main__":
    main()