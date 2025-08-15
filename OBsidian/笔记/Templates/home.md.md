---
title: Home
---

# 📚 目录（自动更新）

```dataviewjs
// 读取当前笔记的所有标题，并生成可跳转的目录（跳过 H1）
const file = app.workspace.getActiveFile();
const cache = app.metadataCache.getFileCache(file);
const heads = (cache?.headings ?? []).filter(h => h.level > 1);   // 只要 H2+
if (heads.length === 0) {
  dv.paragraph("_（本页暂无可生成的目录）_");
} else {
  const md = heads
    .map(h => `${'  '.repeat(h.level - 2)}- [[#${h.heading}|${h.heading}]]`)
    .join('\n');
  dv.paragraph(md);
}
