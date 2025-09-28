import sys

def extract_fasta_names(input_file, output_file):
    """
    从FASTA文件中提取序列名称并将其写入输出文件。
    序列名称是“>”和第一个空格之间的字符串。
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if line.startswith('>'):
                    # 找到第一个空格
                    first_space_index = line.find(' ')
                    # 提取名称
                    if first_space_index != -1:
                        name = line[1:first_space_index]
                    else:
                        # 如果没有空格，则取“>”后面的整个标识符
                        name = line[1:].strip()
                    outfile.write(name + '\n')
        print(f"成功提取名称到 {output_file}")
    except FileNotFoundError:
        print(f"错误：找不到输入文件 '{input_file}'。")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python extract_fasta_names.py <输入fasta文件> <输出文件名>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    extract_fasta_names(input_filename, output_filename)