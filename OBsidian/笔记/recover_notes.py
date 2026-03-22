import subprocess
import os

root = r'D:\Note'
commit = '5a43d32' # 确认包含原始笔记的 commit
target_dir = r'D:\Note\OBsidian\笔记\02_深度学习'
os.makedirs(target_dir, exist_ok=True)

print('--- Python Physical Recovery Drive (v2) ---')

# 1. 强制获取 5a43d32 历史快照中的物理树
cmd = ['git', 'ls-tree', '-r', commit]
result = subprocess.run(cmd, cwd=root, capture_output=True)

count = 0
for line in result.stdout.splitlines():
    # 格式: 100644 blob <hash>   <path>
    parts = line.split()
    if len(parts) < 4: continue
    
    blob_hash = parts[2].decode('utf-8')
    full_path_bytes = line.split(b'\t')[1]
    
    # 我们搜索转义编码：\346 是中文字符开头的常见编码，\350 是“论”字开头
    # 同时搜索文件编号 10. 11. 等
    if b'\\346' in full_path_bytes or b'\\350' in full_path_bytes or b'10.' in full_path_bytes:
        count += 1
        print(f'Recovering Blob {blob_hash}')
        
        # 强制抓取内容
        show_cmd = ['git', 'cat-file', '-p', blob_hash]
        content = subprocess.run(show_cmd, cwd=root, capture_output=True).stdout
        if content:
            # 物理还原：使用编号命名，防止文件名乱码导致写入失败
            filename = f'recovered_note_{count}.md'
            dest_path = os.path.join(target_dir, filename)
            with open(dest_path, 'wb') as f:
                f.write(content)
            
            # 尝试通过内容的第一行来给文件重命名
            try:
                first_line = content.splitlines()[0].decode('utf-8').strip('# ')
                new_name = ''.join(c for c in first_line if c.isalnum() or c in ' ._-')[:30] + '.md'
                if new_name:
                    new_path = os.path.join(target_dir, new_name)
                    os.rename(dest_path, new_path)
                    print(f'  SUCCESS: {new_name}')
                else:
                    print(f'  SUCCESS (Numbered): {filename}')
            except:
                print(f'  SUCCESS (Numbered): {filename}')

if count == 0:
    print('No targets found in this commit history.')
else:
    print(f'Done! Successfully recovered {count} files.')
