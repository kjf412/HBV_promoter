import argparse
import glob
import os

def extract_polymerase_from_file(input_filepath, outfile_handle):
    """
    从单个FASTA文件中读取内容，并将包含'polymerase'的序列写入
    到已打开的输出文件句柄中。
    python extract_all_fasta.py -i all_sequences -o combined_polymerase.fasta
    python extract_all_fasta.py -o combined_polymerase.fasta
    
    python tiqu_4cds.py -i output -o Bat_primate_polymerase.fasta
    Args:
        input_filepath (str): 输入的FASTA文件的路径。
        outfile_handle (file object): 一个已打开并可写入的文件对象。
    """
    try:
        with open(input_filepath, 'r') as infile:
            current_header = None
            current_sequence = []

            for line in infile:
                line = line.strip()
                if not line:
                    continue

                if line.startswith('>'):
                    # 如果已存在一个序列，先检查并写入
                    if current_header and 'polymerase' in current_header.lower():
                        outfile_handle.write(current_header + '\n')
                        outfile_handle.write(''.join(current_sequence) + '\n\n')
                    
                    # 开始处理新序列
                    current_header = line
                    current_sequence = []
                else:
                    # 拼接序列
                    current_sequence.append(line)

            # 不要忘记处理文件中的最后一个序列
            if current_header and 'polymerase' in current_header.lower():
                outfile_handle.write(current_header + '\n')
                outfile_handle.write(''.join(current_sequence) + '\n\n')
        
        print(f"已处理: {os.path.basename(input_filepath)}")

    except Exception as e:
        print(f"处理文件 {input_filepath} 时出错: {e}")


def main():
    """
    主函数，用于解析命令行参数并处理目录中所有的FASTA文件。
    """
    parser = argparse.ArgumentParser(
        description="从一个文件夹内所有的 .fasta 文件中提取 'polymerase' 序列，并合并到一个输出文件中。"
    )

    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        type=str,
        required=True,
        help="用于保存所有提取序列的输出文件路径。"
    )
    
    parser.add_argument(
        "-i", "--input-dir",
        dest="input_dir",
        type=str,
        default='.',  # 默认为当前目录
        help="包含 .fasta 文件的输入文件夹路径。默认为当前脚本所在的目录。"
    )

    args = parser.parse_args()

    # 使用 os.path.join 确保路径在不同操作系统下都能正确拼接
    search_path = os.path.join(args.input_dir, '*.fasta')
    fasta_files = glob.glob(search_path)

    if not fasta_files:
        # 使用 os.path.abspath 获取绝对路径，使提示信息更清晰
        print(f"在文件夹 '{os.path.abspath(args.input_dir)}' 中没有找到 .fasta 文件。")
        return

    print(f"找到 {len(fasta_files)} 个 .fasta 文件，准备开始处理...")

    try:
        # 打开一个输出文件，用于写入所有结果
        with open(args.output_file, 'w') as outfile:
            # 遍历所有找到的fasta文件
            for filepath in fasta_files:
                extract_polymerase_from_file(filepath, outfile)
        
        print(f"\n成功！所有提取的序列都已保存到 {args.output_file}")

    except Exception as e:
        print(f"写入输出文件时发生错误: {e}")


# 当该脚本被直接执行时，运行 main 函数
if __name__ == "__main__":
    main()