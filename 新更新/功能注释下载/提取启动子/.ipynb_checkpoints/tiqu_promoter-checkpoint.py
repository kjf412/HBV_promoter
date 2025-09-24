import argparse
import sys

def parse_fasta(fasta_file: str) -> dict[str, str]:
    """
    解析一个FASTA文件并返回一个序列名称到序列的字典。
    序列中的换行符会被移除。
    """
    sequences = {}
    current_seq_id = None
    current_seq_parts = []
    try:
        with open(fasta_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('>'):
                    # 如果已有序列，先保存
                    if current_seq_id:
                        sequences[current_seq_id] = ''.join(current_seq_parts)
                    
                    # 记录新的序列ID，注意去掉'>'和可能存在的空格
                    current_seq_id = line[1:].split()[0]
                    current_seq_parts = []
                else:
                    if current_seq_id:
                        current_seq_parts.append(line)
        
        # 保存文件中的最后一个序列
        if current_seq_id:
            sequences[current_seq_id] = ''.join(current_seq_parts)
            
    except FileNotFoundError:
        print(f"错误: 文件未找到 -> {fasta_file}", file=sys.stderr)
        sys.exit(1) # 退出程序
        
    return sequences

def extract_promoters(cat_file: str, genome_dict: dict, output_file: str):
    """
    根据cat文件中的坐标信息，从基因组字典中提取启动子序列并写入输出文件。
    """
    promoter_length = 500
    
    try:
        with open(cat_file, 'r') as cat_f, open(output_file, 'w') as out_f:
            for line in cat_f:
                line = line.strip()
                if not line or not line.startswith('>'):
                    continue
                
                # --- 1. 解析cat文件中的行 ---
                # >序列名称:第一段起始位点-第一段终止位点,第二段...
                try:
                    header = line[1:]
                    seq_name, coords_str = header.split(':', 1)
                    first_coord_pair = coords_str.split('_')[0]
                    start_str, end_str = first_coord_pair.split('-')
                    
                    cds_start = int(start_str)
                    cds_end = int(end_str)
                    
                except ValueError:
                    print(f"警告: 无法解析行, 格式错误. 跳过此行: {line}", file=sys.stderr)
                    continue

                # --- 2. 在基因组字典中查找对应序列 ---
                if seq_name not in genome_dict:
                    print(f"警告: 在Domestic基因组文件中未找到序列 '{seq_name}'. 跳过.", file=sys.stderr)
                    continue
                
                genome_seq = genome_dict[seq_name]
                genome_len = len(genome_seq)
                
                # --- 3. 计算并提取启动子序列 (处理环状基因组) ---
                # Python的字符串索引是0-based，而生物学坐标是1-based
                # 我们需要的区域是 [cds_start - 500, cds_start - 1] (1-based)
                # 转换为0-based切片是 [cds_start - 501, cds_start - 1]
                
                promoter_seq = ""
                promoter_start_1based = cds_start - promoter_length
                
                if promoter_start_1based >= 1:
                    # 情况一：启动子不跨越原点
                    start_index = cds_start - promoter_length - 1
                    end_index = cds_start - 1
                    promoter_seq = genome_seq[start_index:end_index]
                else:
                    # 情况二：启动子跨越原点 (环状基因组)
                    # 需要从序列末尾取一段，再从序列开头取一段
                    
                    # 需要从末尾取的长度
                    len_from_end = abs(promoter_start_1based) + 1
                    
                    # 需要从开头取的长度
                    len_from_start = promoter_length - len_from_end
                    
                    # 提取序列
                    seq_from_end = genome_seq[-len_from_end:]
                    seq_from_start = genome_seq[:len_from_start]
                    
                    promoter_seq = seq_from_end + seq_from_start

                # --- 4. 检查长度并写入文件 ---
                if len(promoter_seq) != promoter_length:
                     print(f"警告: 为'{seq_name}'提取的启动子长度不为{promoter_length} (实际为{len(promoter_seq)}). "
                           f"可能是基因组序列本身太短.", file=sys.stderr)

                # 构建新的FASTA头
                output_header = f">{seq_name}:{cds_start}_{cds_end}"
                
                # 写入文件
                out_f.write(output_header + '\n')
                out_f.write(promoter_seq + '\n')

    except FileNotFoundError:
        print(f"错误: 输入文件未找到 -> {cat_file}", file=sys.stderr)
        sys.exit(1)
    
    print(f"启动子序列提取完成，已保存至: {output_file}")


def main():
    """
    主函数，用于解析命令行参数并启动程序。
    """
    parser = argparse.ArgumentParser(
        description="根据cat文件定义的CDS起始位点，从一个环状基因组FASTA文件中提取上游500bp的启动子序列。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助信息格式
    )
    
    parser.add_argument(
        '--cat_file', 
        required=True, 
        help='输入的cat坐标文件。\n格式: >SeqName:start1-end1,start2-end2...'
    )
    
    parser.add_argument(
        '--genome_file', 
        required=True,
        help='包含完整基因组序列的FASTA文件 (例如 Domestic_cat.fasta)。'
    )
    
    parser.add_argument(
        '--output_file', 
        required=True, 
        help='输出启动子序列的FASTA文件名。'
    )
    
    args = parser.parse_args()
    
    # 1. 解析基因组文件
    print(f"正在解析基因组文件: {args.genome_file}...")
    genome_sequences = parse_fasta(args.genome_file)
    if not genome_sequences:
        print("错误: 基因组文件为空或格式不正确。", file=sys.stderr)
        sys.exit(1)
    print(f"解析完成，共找到 {len(genome_sequences)} 条序列。")
    
    # 2. 提取启动子并写入文件
    print(f"正在根据 {args.cat_file} 提取启动子...")
    extract_promoters(args.cat_file, genome_sequences, args.output_file)

if __name__ == "__main__":
    main()