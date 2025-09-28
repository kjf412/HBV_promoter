import os
import sys

def parse_fasta_entries(filename):
    """解析fasta文件，返回包含4个条目的列表，每个条目是(标题行, 序列)的元组"""
    entries = []
    current_title = None
    current_sequence = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n')  # 保留其他空白符，只移除换行
            if line.startswith('>'):
                # 如果已有正在处理的条目，先保存
                if current_title is not None:
                    entries.append((current_title, ''.join(current_sequence)))
                current_title = line
                current_sequence = []
            elif current_title is not None:
                current_sequence.append(line)
    
    # 添加最后一个条目
    if current_title is not None:
        entries.append((current_title, ''.join(current_sequence)))
    
    # 验证条目数量是否为4
    if len(entries) != 4:
        raise ValueError(f"文件 {filename} 包含 {len(entries)} 个条目，预期为4个")
    
    return entries

def process_fasta_files(output_files):
    """处理当前目录下所有fasta文件，按条目顺序合并到对应的输出文件"""
    # 获取当前目录下所有.fasta文件
    fasta_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.lower().endswith('.fasta')]
    
    if not fasta_files:
        print("错误：当前目录下没有找到任何.fasta文件")
        return
    
    print(f"找到 {len(fasta_files)} 个fasta文件，准备处理...")
    
    # 初始化4个输出文件的内容列表
    output_entries = [[], [], [], []]
    
    # 处理每个fasta文件
    for filename in fasta_files:
        try:
            print(f"正在处理: {filename}")
            entries = parse_fasta_entries(filename)
            
            # 将每个条目添加到对应的输出列表
            for i in range(4):
                title, sequence = entries[i]
                # 保留原有的格式，标题行后换行，序列保持原样
                output_entries[i].append(f"{title}\n{sequence}\n")
                
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")
            continue
    
    # 将内容写入对应的输出文件
    for i in range(4):
        with open(output_files[i], 'w') as f:
            f.write(''.join(output_entries[i]))
        print(f"已生成输出文件: {output_files[i]}")
    
    print("所有文件处理完成！")

if __name__ == "__main__":
    # 检查命令行参数是否正确
    if len(sys.argv) != 5:
        print("用法：python split_merge_fasta.py <输出文件1> <输出文件2> <输出文件3> <输出文件4>")
        print("示例：python split_merge_fasta.py group1.fasta group2.fasta group3.fasta group4.fasta")
        sys.exit(1)
    
    # 获取4个输出文件的名称
    output_files = sys.argv[1:5]
    
    # 执行处理
    process_fasta_files(output_files)
