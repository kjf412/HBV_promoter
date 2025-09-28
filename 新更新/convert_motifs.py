import sys

def convert_meme_to_homer(input_file_path, output_file_path):
    """
    将JASPAR生成的MEME格式的motif文件转换为HOMER格式。

    Args:
        input_file_path (str): 输入的MEME格式文件名。
        output_file_path (str): 输出的HOMER格式文件名。
    """
    try:
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            motif_id = None
            motif_name = None
            reading_matrix = False
            matrix_lines = []

            for line in infile:
                line = line.strip()
                if line.startswith("MOTIF"):
                    if motif_id:  # 如果已经有一个motif信息，先写入文件
                        # 写入上一个motif
                        outfile.write(f">{motif_id}\t{motif_name}\t0.0\t0\n")
                        for matrix_line in matrix_lines:
                            outfile.write(f"{matrix_line}\n")
                    
                    # 开始处理新的motif
                    parts = line.split()
                    motif_id = parts[1]
                    motif_name = parts[2] if len(parts) > 2 else motif_id
                    reading_matrix = False
                    matrix_lines = []

                elif "letter-probability matrix" in line:
                    reading_matrix = True
                
                elif reading_matrix and line and not line.startswith("URL"):
                    # MEME格式的矩阵有时候一行有多个碱基的概率，需要处理
                    # 将多个空格替换为一个制表符
                    formatted_line = "\t".join(line.split())
                    matrix_lines.append(formatted_line)
            
            # 写入最后一个motif
            if motif_id:
                outfile.write(f">{motif_id}\t{motif_name}\t0.0\t0\n")
                for matrix_line in matrix_lines:
                    outfile.write(f"{matrix_line}\n")
        
        print(f"转换成功！输出文件已保存为: {output_file_path}")

    except FileNotFoundError:
        print(f"错误: 输入文件 '{input_file_path}' 未找到。")
    except Exception as e:
        print(f"发生错误: {e}")

# --- 使用方法 ---
# 1. 将上面的代码保存为一个Python文件，例如 "convert_motifs.py"。
# [cite_start]2. 将你上传的JASPAR txt文件 "20250920101742_JASPAR2024_combined_matrices_543965_meme.txt" [cite: 1] 和这个Python脚本放在同一个文件夹下。
# 3. 打开终端或命令行，进入该文件夹，然后运行以下命令：
#    python convert_motifs.py 20250920101742_JASPAR2024_combined_matrices_543965_meme.txt homer_motifs.txt

# 假设你已经将代码保存并在命令行中运行，这里直接调用函数来演示
# 注意：在实际使用中，你需要通过命令行来传递文件名参数
# convert_meme_to_homer("20250920101742_JASPAR2024_combined_matrices_543965_meme.txt", "homer_motifs.txt")


if __name__ == "__main__":
  
        convert_meme_to_homer(sys.argv[1], sys.argv[2])