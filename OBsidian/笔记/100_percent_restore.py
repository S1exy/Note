import subprocess
import os

root = r'D:\Note'
vault_root = r'D:\Note\OBsidian\笔记'
target_code = b'DotProductAttention'

print('--- Python 100% RESTORE DRIVE (THE FINAL) ---')

# 1. 获取 Git 中所有对象的列表 (不带任何转义)
cmd = ['git', 'rev-list', '--all', '--objects']
result = subprocess.run(cmd, cwd=root, capture_output=True)

count = 0
for line in result.stdout.splitlines():
    # 格式: <hash> <path>
    if len(line) < 41: continue
    
    blob_hash = line[:40].decode()
    path_bytes = line[41:]
    
    # 查找特定内容
    if b'\\346' in path_bytes or b'10.' in path_bytes:
        # 强制获取内容检查指纹
        content = subprocess.run(['git', 'cat-file', '-p', blob_hash], cwd=root, capture_output=True).stdout
        if target_code in content:
            # 命中！解析原名
            filename_bytes = path_bytes.split(b'/')[-1].strip(b'\"')
            try:
                # 这一步是解开 Git 的八进制转义，变回中文字符
                filename_str = filename_bytes.decode('unicode_escape').encode('latin-1').decode('utf-8')
                
                dest_dir = os.path.join(vault_root, '02_深度学习')
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, filename_str)
                
                with open(dest_path, 'wb') as f:
                    f.write(content)
                print(f'SUCCESSFULLY RESTORED: {filename_str}')
                count += 1
            except: pass

if count == 0:
    print('No matching content found in Git history.')
else:
    print(f'Done! Successfully recovered {count} files with original names.')
