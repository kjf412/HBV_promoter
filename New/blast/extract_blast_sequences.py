import sys
from Bio import SeqIO

def read_fasta_file(fasta_file):
    """读取FASTA文件，返回一个字典{序列ID(空格前部分): 序列}"""
    sequences = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        # 只提取空格前的部分作为序列ID
        seq_id = record.id.split()[0]  # 分割空格，取第一个元素
        sequences[seq_id] = str(record.seq)
    return sequences

def extract_sequences(blast_result, fasta_sequences, output_file):
    """根据BLAST结果中的坐标提取序列片段"""
    with open(blast_result, 'r') as blast_file, open(output_file, 'w') as out_file:
        for line_num, line in enumerate(blast_file, 1):
            # 去除行尾换行符并分割列
            parts = line.strip().split('\t')
            
            # 检查列数是否正确（根据之前的格式应该是14列）
            if len(parts) != 13:
                print(f"警告: 第{line_num}行格式不正确，列数不是13，已跳过", file=sys.stderr)
                continue
            
            # 提取所需信息（根据之前定义的列顺序）
            qseqid = parts[0]
            qstart = int(parts[6])
            qend = int(parts[7])
            
            # 检查序列是否存在于FASTA文件中
            if qseqid not in fasta_sequences:
                print(f"警告: 在FASTA文件中未找到序列 {qseqid}，已跳过第{line_num}行", file=sys.stderr)
                continue
            
            # 获取完整序列
            full_sequence = fasta_sequences[qseqid]
            
            # 注意：BLAST使用1-based坐标，而Python字符串是0-based
            # 所以需要调整起始位置（减1）
            start = qstart - 1
            end = qend  # 因为Python切片是右开区间
            
            # 确保坐标在有效范围内
            if start < 0 or end > len(full_sequence):
                print(f"警告: 序列 {qseqid} 的坐标超出范围（起始位置：{qstart}，终止位置：{qend}，序列长度：{len(full_sequence)}），已跳过第{line_num}行", file=sys.stderr)
                continue
            
            # 截取序列片段
            extracted_sequence = full_sequence[start:end]
            
            # 写入输出文件（FASTA格式）
            out_file.write(f">{qseqid}_from_{qstart}_to_{qend}\n")
            # 按每行80个字符分割序列，方便阅读
            for i in range(0, len(extracted_sequence), 80):
                out_file.write(f"{extracted_sequence[i:i+80]}\n")

def main():
    if len(sys.argv) != 4:
        print("用法: python extract_blast_sequences_improved.py <blast_result_file> <fasta_file> <output_file>")
        print("示例: python extract_blast_sequences_improved.py all_add.blast1 Human.fasta extracted_sequences.fasta")
        sys.exit(1)
    
    blast_result_file = sys.argv[1]
    fasta_file = sys.argv[2]
    output_file = sys.argv[3]
    
    print(f"读取FASTA文件: {fasta_file}")
    fasta_sequences = read_fasta_file(fasta_file)
    print(f"成功读取 {len(fasta_sequences)} 条序列")
    
    print(f"从BLAST结果 {blast_result_file} 提取序列...")
    extract_sequences(blast_result_file, fasta_sequences, output_file)
    
    print(f"提取完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    main()
    