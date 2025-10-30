import os
import zipfile
import tarfile

def extract_cds_from_zip(zip_path, output_dir):
    """从ZIP压缩包中提取cds.fna文件"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # 查找ncbi_dataset/data/cds.fna文件
            target_file = None
            for file in zf.namelist():
                if file.endswith('ncbi_dataset/data/cds.fna'):
                    target_file = file
                    break
            
            if target_file:
                # 读取文件内容
                with zf.open(target_file) as f:
                    content = f.read()
                
                # 获取输出文件名
                zip_name = os.path.splitext(os.path.basename(zip_path))[0]
                output_file = os.path.join(output_dir, f"{zip_name}.fasta")
                
                # 写入输出文件
                with open(output_file, 'wb') as f_out:
                    f_out.write(content)
                return True
            else:
                print(f"在ZIP文件 {zip_path} 中未找到ncbi_dataset/data/cds.fna")
                return False
    except Exception as e:
        print(f"处理ZIP文件 {zip_path} 时出错: {str(e)}")
        return False

def extract_cds_from_tar(tar_path, output_dir, mode):
    """从TAR压缩包中提取cds.fna文件"""
    try:
        with tarfile.open(tar_path, mode) as tf:
            # 查找ncbi_dataset/data/cds.fna文件
            target_file = None
            for member in tf.getmembers():
                if member.name.endswith('ncbi_dataset/data/cds.fna'):
                    target_file = member
                    break
            
            if target_file:
                # 读取文件内容
                with tf.extractfile(target_file) as f:
                    content = f.read()
                
                # 获取输出文件名
                tar_name = os.path.splitext(os.path.basename(tar_path))[0]
                # 处理.tar.gz等双重扩展名
                if tar_name.endswith('.tar'):
                    tar_name = os.path.splitext(tar_name)[0]
                output_file = os.path.join(output_dir, f"{tar_name}.fasta")
                
                # 写入输出文件
                with open(output_file, 'wb') as f_out:
                    f_out.write(content)
                return True
            else:
                print(f"在TAR文件 {tar_path} 中未找到ncbi_dataset/data/cds.fna")
                return False
    except Exception as e:
        print(f"处理TAR文件 {tar_path} 时出错: {str(e)}")
        return False

def process_compressed_files(input_dir, output_dir=None):
    """
    批量处理文件夹下的所有压缩文件
    
    参数:
        input_dir: 包含压缩文件的文件夹路径
        output_dir: 输出文件的保存路径，默认为input_dir下的output文件夹
    """
    # 设置默认输出目录
    if output_dir is None:
        output_dir = os.path.join(input_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的压缩文件扩展名及对应的处理方式
    compression_formats = {
        '.zip': ('zip', None),
        '.tar': ('tar', 'r'),
        '.tar.gz': ('tar', 'r:gz'),
        '.tgz': ('tar', 'r:gz'),
        '.tar.bz2': ('tar', 'r:bz2'),
        '.tbz2': ('tar', 'r:bz2'),
        '.tar.xz': ('tar', 'r:xz'),
        '.txz': ('tar', 'r:xz')
    }
    
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        # 跳过目录，只处理文件
        if not os.path.isfile(file_path):
            continue
        
        # 检查文件是否为支持的压缩格式
        processed = False
        for ext, (type_, mode) in compression_formats.items():
            if filename.lower().endswith(ext):
                print(f"处理文件: {filename}")
                if type_ == 'zip':
                    extract_cds_from_zip(file_path, output_dir)
                elif type_ == 'tar':
                    extract_cds_from_tar(file_path, output_dir, mode)
                processed = True
                break
        
        if not processed:
            print(f"不支持的文件格式: {filename}，跳过处理")
    
    print("处理完成！")

if __name__ == "__main__":
    # 在这里设置包含压缩文件的文件夹路径
    input_directory = "./"  # 替换为你的压缩文件所在目录
    
    # 可选：设置输出文件夹路径，不设置则默认在input_directory下创建output文件夹
    output_directory = "./output_files"
    
    # 执行处理
    process_compressed_files(input_directory)
    # 如果设置了output_directory，请使用下面这行
    # process_compressed_files(input_directory, output_directory)
