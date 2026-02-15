# AI-Humanizer-ZH - 中文AI文本人类化工具

## ✅ 技能安装完成！

AI-Humanizer-ZH技能已成功安装到Clawdbot中。

## 📍 安装位置
```
C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw-cn\skills\ai-humanizer-zh
```

## 🚀 快速使用

### 在Clawdbot中使用
你可以直接通过消息指令使用该工具：

```
请帮我润色这段中文文本：
综上所述，人工智能技术在当今社会发挥着不可或缺的作用。
```

或

```
去除这段文本的AI味：
首先，它可以提高工作效率；其次，它能够处理大量数据。
```

### 命令行使用
```bash
# 基础用法
python scripts/humanize_zh.py "AI生成的中文文本"

# 自定义风格和变化程度
python scripts/humanize_zh.py "AI文本" --style creative --variability high

# 批量处理文件
python scripts/humanize_zh.py --input input.txt --output output.txt

# 保留专业术语
python scripts/humanize_zh.py "AI文本" --preserve "人工智能" "机器学习" "神经网络"

# 显示调试信息
python scripts/humanize_zh.py "AI文本" --debug
```

## 📝 功能特性

- ✅ 专门为中文AI文本优化，去除机械感和公式化表达
- ✅ 检测并修复24种AI写作痕迹
- ✅ 支持三种风格切换（口语化/正式/创意）
- ✅ 可调整文本变化程度（低/中/高）
- ✅ 批量处理和关键词保留功能
- ✅ 保留原始文本核心信息的同时增加自然变化
- ✅ 智能检测AI写作模式并自动调整处理策略

## 🎨 风格选项

### 口语化风格 (casual)
- 适合：社交媒体、日常对话、博客
- 特点：使用口语词汇、短句、轻松语气
- 示例："这个功能真的挺好用的，建议大家试试看。"

### 正式风格 (formal)
- 适合：商务文档、学术论文、官方报告
- 特点：保持专业性，但减少机械感
- 示例："该功能在实际应用中表现出色，建议用户尝试使用。"

### 创意风格 (creative)
- 适合：文学作品、广告文案、品牌故事
- 特点：富有想象力、情感丰富、个性鲜明
- 示例："这个功能就像魔法一样，轻轻一点，问题全解决！"

## 📊 变化程度

### 低变化 (low)
- 轻微调整，保留大部分原始结构和词汇
- 适用：技术文档、法律文件、学术论文
- 处理：基础替换，保留专业术语

### 中变化 (medium)
- 适度调整，平衡自然性和准确性
- 适用：大多数场景，包括商务沟通和一般文章
- 处理：适度替换，增加自然变化

### 高变化 (high)
- 大幅调整，增加个性化和创造性
- 适用：创意写作、营销文案、社交媒体内容
- 处理：深度优化，注入个人风格

## 🔧 高级功能

### 分阶段处理
```bash
# 第一阶段：基础润色
python scripts/humanize_zh.py "AI文本" --style casual --variability low

# 第二阶段：深度优化
python scripts/humanize_zh.py "已润色文本" --style creative --variability high
```

### 批量处理目录
```bash
# 处理整个目录
for file in *.txt; do
    python scripts/humanize_zh.py --input "$file" --outputai-humanized_$file"
done
```

### 自定义替换规则
修改 `scripts/humanize_zh.py` 中的 `ZH_REPLACEMENTS` 字典来添加自定义规则：

```python
ZH_REPLACEMENTS = {
    "你的关键词": ["替换词1", "替换词2", "替换词3"],
    # 更多自定义规则...
}
```

## 📚 相关文档

- **使用指南**：`references/guide_zh.md` - 详细使用说明和示例
- **AI模式检测**：`references/ai_patterns.md` - 24种AI写作痕迹详解
- **技能文档**：`SKILL.md` - Clawdbot集成说明
- **帮助文档**：运行 `python scripts/humanize_zh.py --help` 获取参数说明

## 🎯 检测的AI写作模式

### 📝 内容模式（6种）
- 过度强调意义、遗产和更广泛的趋势
- 过度强调知名度和媒体报道
- 以 -ing 结尾的肤浅分析
- 宣传和广告式语言
- 模糊归因和含糊措辞
- 提纲式的"挑战与未来展望"部分

### 🔤 语言和语法模式（6种）
- 过度使用的"AI词汇"
- 避免使用"是"（系动词回避）
- 否定式排比
- 三段式法则过度使用
- 刻意换词（同义词循环）
- 虚假范围

### 🎨 风格模式（6种）
- 破折号过度使用
- 粗体过度使用
- 内联标题垂直列表
- 标题中的标题大写
- 表情符号
- 弯引号

### 💬 交流模式和填充词（6种）
- 协作交流痕迹
- 知识截止日期免责声明
- 谄媚/卑躬屈膝的语气
- 填充短语
- 过度限定
- 通用积极结论

## 📝 使用示例

### 原始AI文本
"综上所述，人工智能技术在当今社会发挥着不可或缺的作用。首先，它可以提高工作效率；其次，它能够处理大量数据；最后，它有助于创新和发展。"

### 口语化风格输出
"总的来说，人工智能现在可牛了！首先，它能帮我们提高工作效率；其次，它还能处理海量数据；最后，它还能推动各种创新和发展！"

### 创意风格输出
"你猜怎么着？人工智能现在已经渗透到社会各个角落啦！它不仅能把工作效率拉满，还能轻松搞定海量数据，更厉害的是，它还能各种搞事情，推动创新和发展呢！"

### 正式风格输出
"总的来说，人工智能在当今社会中扮演着至关重要的角色。首先，它能够显著提升工作效率；其次，它能够处理大规模数据；最后，它有助于推动创新与发展。"

## 🎯 最佳实践

### 1. 结合人工编辑
- 工具处理后，人工检查逻辑一致性
- 添加个人观点和独特见解
- 调整语气以适应目标受众

### 2. 质量控制
- 检查关键信息是否被正确保留
- 确保文本自然流畅，不生硬
- 验证专业术语的准确性
- 阅读一遍，听感是否自然

### 3. 调整策略
- **长文本**：先分段处理，再整体优化
- **技术文档**：使用低变化程度，保留专业术语
- **创意内容**：使用高变化程度，增加个性化表达

## ⚠️ 注意事项

1. **不适用于代码或结构化数据**
2. **可能改变原文的精确含义**
3. **需要人工检查重要文档**
4. **文化差异可能影响处理效果**

## 🔧 技术支持

如有问题，请检查：
1. Python环境是否正确安装（需要Python 3.6+）
2. 文件路径是否正确
3. 输入文本格式是否正确
4. 查看脚本帮助文档：`python scripts/humanize_zh.py --help`

## 📖 项目说明

本项目基于以下资源优化开发：
- [Humanizer-zh](https://github.com/op7418/Humanizer-zh) - 中文版Humanizer项目
- [blader/humanizer](https://github.com/blader/humanizer) - 原始英文版项目
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) - 实用工具部分
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) - AI写作特征指南

## 📄 许可

本项目遵循原项目的许可协议。核心内容基于维基百科社区的观察和总结。

---

**AI-Humanizer-ZH** - 让AI文本更自然、更人性化！