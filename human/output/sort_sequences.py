import argparse
import sys
from pathlib import Path
from Bio import SeqIO  # 导入BioPython的SeqIO模块

def sort_sequences_by_keyword(input_folder, out_files):
    """
    遍历输入文件夹中的所有FASTA文件，并根据标题中的关键字
    将序列分类写入不同的输出文件。

    :param input_folder: 包含.fasta文件的输入文件夹路径
    :param out_files: 一个字典，映射关键字和输出文件名
    """
    
    # 定义关键字映射。使用.lower()确保匹配不区分大小写
    keyword_map = {
        "polymerase": out_files['poly'],
        "surface protein": out_files['surf'],
        "x protein": out_files['x'],
        "core protein": out_files['core']
    }
    
    # 统计每个类别写入的序列数
    sequence_counts = {key: 0 for key in keyword_map}
    
    file_handles = {}
    
    try:
        # 1. 一次性打开所有的输出文件
        for key, filepath in keyword_map.items():
            file_handles[key] = open(filepath, 'w', encoding='utf-8')
        
        # 2. 检查输入文件夹是否存在
        input_dir = Path(input_folder)
        if not input_dir.is_dir():
            print(f"错误: 路径 '{input_folder}' 不是一个有效的文件夹。", file=sys.stderr)
            return

        print(f"--- 正在扫描文件夹: {input_dir.resolve()} ---")
        
        processed_file_count = 0
        
        # 3. 遍历文件夹中的所有文件
        # 我们假设文件以 .fasta, .fa, 或 .fna 结尾
        valid_extensions = {'.fasta', '.fa', '.fna'}
        
        for fasta_file in input_dir.iterdir():
            # 确保只处理文件，并且是fasta文件
            if fasta_file.is_file() and fasta_file.suffix.lower() in valid_extensions:
                processed_file_count += 1
                print(f"  正在处理: {fasta_file.name}")
                
                # 4. 使用 BioPython 解析 FASTA 文件
                with open(fasta_file, 'r', encoding='utf-8') as f_in:
                    # SeqIO.parse 会自动处理多行序列
                    for record in SeqIO.parse(f_in, "fasta"):
                        # record.description 包含'>'之后的所有信息
                        header_text = record.description.lower()
                        
                        # 5. 检查关键字并写入相应的文件
                        for keyword, out_handle in file_handles.items():
                            if keyword in header_text:
                                # 以FASTA格式将整个记录(标题+序列)写入
                                SeqIO.write(record, out_handle, "fasta")
                                sequence_counts[keyword] += 1
                                # 假设一个序列只属于一个类别，找到后即跳出
                                break 
        
        print(f"\n--- 处理完毕 ---")
        print(f"总共处理了 {processed_file_count} 个 FASTA 文件。")
        for key, count in sequence_counts.items():
            print(f"  提取了 {count} 条 '{key}' 序列到 {keyword_map[key]}")

    except FileNotFoundError:
        print(f"错误: 无法找到输入文件夹 '{input_folder}'", file=sys.stderr)
    except Exception as e:
        print(f"发生了一个错误: {e}", file=sys.stderr)
    finally:
        # 6. 无论成功与否，都确保关闭所有打开的文件
        for handle in file_handles.values():
            if handle:
                handle.close()
        print("所有输出文件均已关闭。")

def main():
    """
    主函数，用于解析命令行参数并调用排序功能。
    """
    parser = argparse.ArgumentParser(
        description="从一个文件夹中的所有FASTA文件里提取特定蛋白质序列。"
    )
    
    # 1. 输入文件夹参数 (位置参数)
    parser.add_argument(
        "input_folder",
        type=str,
        help="包含所有FASTA文件的输入文件夹路径。"
    )
    
    # 2. 输出文件参数 (命名参数，设为必需)
    parser.add_argument(
        "--out_poly",
        type=str,
        required=True,
        help="用于保存 'polymerase' 序列的输出文件名。"
    )
    parser.add_argument(
        "--out_surf",
        type=str,
        required=True,
        help="用于保存 'surface protein' 序列的输出文件名。"
    )
    parser.add_argument(
        "--out_x",
        type=str,
        required=True,
        help="用于保存 'X protein' 序列的输出文件名。"
    )
    parser.add_argument(
        "--out_core",
        type=str,
        required=True,
        help="用于保存 'core protein' 序列的输出文件名。"
    )
    
    args = parser.parse_args()
    
    # 将输出参数打包成一个字典
    output_files = {
        'poly': args.out_poly,
        'surf': args.out_surf,
        'x': args.out_x,
        'core': args.out_core
    }
    
    # 调用核心功能
    sort_sequences_by_keyword(args.input_folder, output_files)

if __name__ == "__main__":
    main()