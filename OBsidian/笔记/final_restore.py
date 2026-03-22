import subprocess
import os

root = r'D:\Note'
commit = '5a43d32'
vault_root = r'D:\Note\OBsidian\笔记'

print('--- FINAL GLOBAL RESTORATION DRIVE (BRUTE FORCE) ---')

# 1. 物理获取 5a43d32 历史快照中的全量树
cmd = ['git', 'ls-tree', '-r', commit]
result = subprocess.run(cmd, cwd=root, capture_output=True)

count = 0
for line in result.stdout.splitlines():
    # 格式: 100644 blob <hash>   <path>
    parts = line.split(b'\t')
    if len(parts) < 2: continue
    
    blob_hash = parts[0].split()[2].decode()
    path_bytes = parts[1]
    
    # 彻底剥离文件名两端的引号
    filename_bytes = path_bytes.split(b'/')[-1].strip(b'\"')
    
    try:
        # 将 Git 的八进制转义串反序列化为正常的 UTF-8
        filename_str = filename_bytes.decode('unicode_escape').encode('latin-1').decode('utf-8')
    except:
        filename_str = filename_bytes.decode('utf-8', errors='ignore')

    # 我们现在全量打捞：只要是原先在“李沐”或“论文”文件夹下的
    target_folder = ''
    if b'\\346\\235\\216' in path_bytes or b'10.' in path_bytes:
        target_folder = '02_深度学习'
    elif b'\\350\\256\\272' in path_bytes:
        target_folder = '03_科研调研'
    
    if target_folder:
        count += 1
        dest_dir = os.path.join(vault_root, target_folder)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, filename_str)
        
        # 强制抓取内容
        content = subprocess.run(['git', 'cat-file', '-p', blob_hash], cwd=root, capture_output=True).stdout
        if content:
            with open(dest_path, 'wb') as f:
                f.write(content)
            print(f'Restored: {filename_str} -> {target_folder}')

print(f'--- Restoration Complete. Recovered {count} files. ---')
