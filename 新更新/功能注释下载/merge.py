import os
import sys

def merge_fasta_files(output_filename):
    """
    合并当前目录下所有fasta文件到指定的输出文件
    
    参数:
        output_filename: 输出文件的名称
    """
    # 获取当前目录下所有.fasta文件
    fasta_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.lower().endswith('.fasta')]
    
    if not fasta_files:
        print("错误：当前目录下没有找到任何.fasta文件")
        return
    
    print(f"找到 {len(fasta_files)} 个fasta文件，准备合并...")
    print("将合并以下文件：")
    for file in fasta_files:
        print(f"  - {file}")
    
    # 合并文件
    with open(output_filename, 'w') as outfile:
        for filename in fasta_files:
            with open(filename, 'r') as infile:
                # 读取文件内容并写入输出文件
                outfile.write(infile.read())
                # 在文件之间添加一个空行，避免序列连接在一起
                outfile.write('\n')
    
    print(f"合并完成！结果已保存到 {output_filename}")

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法：python merge_fasta.py <输出文件名>")
        print("示例：python merge_fasta.py merged_result.fasta")
        sys.exit(1)
    
    # 获取输出文件名
    output_file = sys.argv[1]
    
    # 检查输出文件是否为.fasta格式
    if not output_file.lower().endswith('.fasta'):
        print("警告：输出文件建议使用.fasta扩展名")
    
    # 执行合并
    merge_fasta_files(output_file)
    