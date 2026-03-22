import subprocess
import os

root = r'D:\Note'
commit = '5a43d32'
vault_root = r'D:\Note\OBsidian\笔记'

print('--- Python Brute Force Recovery (ASCII Only Script) ---')

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
    
    # 我们全量打捞：只要路径里包含 \346 (中文字符编码) 或者 10. 11. 等
    if b'\\346' in path_bytes or b'\\350' in path_bytes or b'10.' in path_bytes:
        # 获取文件名
        filename_bytes = path_bytes.split(b'/')[-1].strip(b'\"')
        
        try:
            # 八进制转义串 -> 物理字节 -> UTF-8 字符串
            filename_str = filename_bytes.decode('unicode_escape').encode('latin-1').decode('utf-8')
            
            # 这里的魔法：根据原始路径中的转义字节判断归属
            # \346\235\216 是“李沐”的常见开头
            folder = '02_深度学习' if b'\\346\\235\\216' in path_bytes or b'10.' in path_bytes else '03_科研调研'
            
            dest_dir = os.path.join(vault_root, folder)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename_str)
            
            # 物理还原内容
            content = subprocess.run(['git', 'cat-file', '-p', blob_hash], cwd=root, capture_output=True).stdout
            if content:
                with open(dest_path, 'wb') as f:
                    f.write(content)
                print(f'Restored: {filename_str}')
                count += 1
        except:
            pass

print(f'--- Done. Recovered {count} files. ---')
