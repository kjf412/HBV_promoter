from Bio import SeqIO
import argparse
from typing import Dict, Tuple


def load_genome_database(fasta_path: str) -> Dict[str, Dict[str, str | int]]:
    """
    加载DATA_fasta.txt，提取基因组名称（>到第一个_之间的字符串）和序列信息
    返回格式：{基因组名称: {"seq": 完整序列, "len": 序列长度}}
    """
    genome_dict = {}
    try:
        for record in SeqIO.parse(fasta_path, "fasta"):
            # 提取基因组名称：>到第一个_之间的部分（如>ACNDV_... → ACNDV；>NC076022.1_... → NC076022.1）
            fasta_header = record.id  # 不含">"的序列名
            first_underscore_idx = fasta_header.find("_")
            if first_underscore_idx == -1:
                print(f"警告：{fasta_header} 无下划线，跳过（需符合'名称_...'格式）")
                continue
            genome_name = fasta_header[:first_underscore_idx]
            
            # 处理序列（转为大写，确保无换行）
            genome_seq = str(record.seq).upper()
            genome_len = len(genome_seq)
            
            # 去重（重复名称覆盖）
            if genome_name in genome_dict:
                print(f"警告：基因组{genome_name}重复，覆盖前序序列")
            genome_dict[genome_name] = {
                "seq": genome_seq,
                "len": genome_len
            }
        print(f"成功加载 {len(genome_dict)} 个基因组，名称列表：{list(genome_dict.keys())}")
    except Exception as e:
        raise RuntimeError(f"加载DATA_fasta.txt失败：{str(e)}") from e
    return genome_dict


def parse_homer_line(homer_line: str) -> Tuple[str, int, str]:
    """
    解析Homer_1.txt的一行，提取关键信息：
    返回：(基因组名称, CDS起始位点, Homer原始行)
    """
    # 去除行首尾空白和可能的换行符，保留原始头部（含">"）
    homer_line = homer_line.strip()
    if not homer_line.startswith(">"):
        raise ValueError(f"Homer行格式错误：{homer_line}（需以'>'开头）")
    
    # 提取不含">"的核心内容用于解析
    core_header = homer_line[1:]  # 如"AMDV_1_620_3127_1_ID=2_1"
    parts = core_header.split("_")
    
    # 验证格式（至少需3部分：名称_序号_起始位点_...）
    if len(parts) < 3:
        raise ValueError(f"Homer行解析失败：{homer_line}（需符合'>名称_序号_起始位点_...'格式）")
    
    # 提取基因组名称（第一个_前的部分）
    genome_name = parts[0]
    # 提取CDS起始位点（第二个_后的部分，需为数字）
    try:
        cds_start = int(parts[2])  # 第二个_后是起始位点（如AMDV_1_620... → 620）
    except ValueError:
        raise ValueError(f"Homer行{homer_line}的起始位点不是数字：{parts[2]}")
    
    return genome_name, cds_start, homer_line


def extract_circular_promoter(genome_info: Dict[str, str | int], cds_start: int, promoter_len: int = 100) -> str:
    """
    提取环状基因组的启动子（向上100bp，不足时从末端补足）
    参数：
        genome_info: 含"seq"（基因组序列）和"len"（序列长度）的字典
        cds_start: CDS起始位点（1-based）
        promoter_len: 启动子长度（默认100bp）
    返回：100bp启动子序列
    """
    genome_seq = genome_info["seq"]
    genome_len = genome_info["len"]
    
    # 验证CDS起始位点合法性（1-based）
    if cds_start < 1 or cds_start > genome_len:
        raise ValueError(f"CDS起始位点{cds_start}超出基因组范围（1~{genome_len}）")
    
    # 极端情况：基因组长度 < 启动子长度，返回全基因组
    if genome_len < promoter_len:
        print(f"警告：基因组长度{genome_len}bp < 启动子长度{promoter_len}bp，返回全基因组")
        return genome_seq
    
    # 计算启动子区域（1-based：[cds_start - promoter_len, cds_start - 1]）
    prom_1based_start = cds_start - promoter_len
    prom_1based_end = cds_start - 1
    
    # 情况1：上游区域完全在基因组内（无需跨环）
    if prom_1based_start >= 1:
        # 转换为0-based切片（左闭右开）
        prom_seq = genome_seq[prom_1based_start - 1 : prom_1based_end]
        # 验证长度（防止计算错误）
        if len(prom_seq) != promoter_len:
            raise ValueError(f"启动子长度异常：{len(prom_seq)}bp（预期{promoter_len}bp）")
        return prom_seq
    
    # 情况2：上游不足，从末端补足（环状逻辑）
    else:
        # 上游有效长度（1-based：1 ~ prom_1based_end）
        valid_upstream_len = prom_1based_end
        # 需从末端补充的长度
        supplement_len = promoter_len - valid_upstream_len
        
        # 提取末端补充序列（0-based：基因组末端向前截取supplement_len）
        supplement_seq = genome_seq[-supplement_len:]
        # 提取上游有效序列（0-based：0 ~ prom_1based_end - 1）
        valid_upstream_seq = genome_seq[:prom_1based_end]
        # 拼接：末端补充 + 上游有效（符合环状连续性）
        prom_seq = supplement_seq + valid_upstream_seq
        
        # 验证最终长度
        if len(prom_seq) != promoter_len:
            raise ValueError(
                f"环状启动子拼接失败：补充{len(supplement_seq)}bp + 上游{len(valid_upstream_seq)}bp → 共{len(prom_seq)}bp"
            )
        print(f"提示：启动子跨环状边界（末端{supplement_len}bp + 上游{valid_upstream_len}bp → 共100bp）")
        return prom_seq


def main(homer_path: str, fasta_path: str, output_path: str, promoter_len: int = 100):
    # 1. 加载基因组数据库
    genome_dict = load_genome_database(fasta_path)
    
    # 2. 处理Homer_1.txt并提取启动子
    with open(homer_path, "r", encoding="utf-8") as homer_f, \
         open(output_path, "w", encoding="utf-8") as out_f:
        
        success_count = 0
        total_count = 0
        
        for line_num, line in enumerate(homer_f, 1):
            line = line.strip()
            # 跳过空行
            if not line:
                continue
            total_count += 1
            
            try:
                # 解析Homer行
                genome_name, cds_start, original_header = parse_homer_line(line)
                
                # 检查基因组是否存在
                if genome_name not in genome_dict:
                    print(f"跳过第{line_num}行：{original_header} → 未找到匹配基因组{genome_name}")
                    continue
                
                # 提取启动子
                genome_info = genome_dict[genome_name]
                promoter_seq = extract_circular_promoter(genome_info, cds_start, promoter_len)
                
                # 按FASTA格式写入输出（保留Homer原始名称，序列每80字符换行）
                out_f.write(f"{original_header}\n")
                for i in range(0, len(promoter_seq), 80):
                    out_f.write(promoter_seq[i:i+80] + "\n")
                
                success_count += 1
                print(f"处理成功第{line_num}行：{original_header}")
            
            except Exception as e:
                print(f"跳过第{line_num}行：{line} → 错误：{str(e)}")
                continue
    
    # 输出统计结果
    print(f"\n处理完成！成功提取 {success_count}/{total_count} 个启动子")
    print(f"结果保存至：{output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取HBV类环状基因组的启动子序列（适配Homer_1和DATA_fasta格式）")
    parser.add_argument("--homer", required=True, help="Homer_1.txt文件路径（含CDS名称和起始位点）")
    parser.add_argument("--fasta", required=True, help="DATA_fasta.txt文件路径（含基因组序列）")
    parser.add_argument("--output", required=True, help="输出启动子文件路径（FASTA格式）")
    parser.add_argument("--promoter-len", type=int, default=100, help="启动子长度（默认100bp）")
    
    args = parser.parse_args()
    main(
        homer_path=args.homer,
        fasta_path=args.fasta,
        output_path=args.output,
        promoter_len=args.promoter_len
    )