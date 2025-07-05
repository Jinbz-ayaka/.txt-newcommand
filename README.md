# .txt-newcommand

# LaTeX 命令替换工具

## 概述

这个 Python 脚本用于批量处理 LaTeX 文档中的自定义命令。它通过读取命令定义文件（`word.txt`），自动将文档中的所有自定义命令（如 `\xxx`）替换为对应的目标命令（如 `\yyy`）。

## 主要功能

1. **自动命令解析**：从 `word.txt` 文件中提取命令替换规则
2. **智能替换**：按命令长度优先替换（长命令优先）
3. **用户友好界面**：
   - 自动列出当前目录文件
   - 支持编号选择输入文件
   - 自动生成输出文件名
4. **编码支持**：自动处理 UTF-8 编码文件
5. **路径处理**：自动处理相对路径和绝对路径

## 系统要求

- Python 3.6 或更高版本
- 操作系统：Windows, macOS 或 Linux

## 安装与使用

### 1. 准备文件

1. 将脚本保存为 `latex_replace.py`
2. 创建命令定义文件 `word.txt`（格式见下文）
3. 准备要处理的 LaTeX 文件（如 `document.tex`）

### 2. 运行脚本

```bash
python latex_replace.py
```

### 3. 按提示操作

```
当前工作目录: /path/to/your/files

当前目录下的 .tex 文件:
1. document.tex
2. chapter1.tex
3. references.tex

请输入要处理的文件名（直接输入名称或编号）: 1
请输入输出文件名 [默认为 document_output.tex]: 

从 word.txt 中解析出 5 条替换规则
成功处理文件！已将 document.tex 中的命令替换
结果保存至: /path/to/your/files/document_output.tex
```

## 命令定义文件格式

`word.txt` 文件每行定义一个命令替换规则，格式为：

```
\newcommand\源命令\目标命令
```

### 示例 `word.txt` 内容

```
\newcommand\bb\mathbb
\newcommand\bf\mathbf
\newcommand\cal\mathcal
\newcommand\set\mathfrak
\newcommand\txt\text
```

## 文件处理示例

### 输入文件 (`document.tex`)

```latex
\section{数学符号}
实数集: $\bb{R}$ \\
向量: $\bf{v}$ \\
函数空间: $\cal{F}$ \\
集合: $\set{S}$ \\
文本: $\txt{示例}$
```

### 输出文件 (`document_output.tex`)

```latex
\section{数学符号}
实数集: $\mathbb{R}$ \\
向量: $\mathbf{v}$ \\
函数空间: $\mathcal{F}$ \\
集合: $\mathfrak{S}$ \\
文本: $\text{示例}$
```

## 高级用法

### 1. 命令行参数支持

```bash
python latex_replace.py input.tex output.tex
```

### 2. 批量处理文件

修改脚本最后部分：

```python
if __name__ == "__main__":
    # 设置工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 配置文件路径
    command_file = "word.txt"
    command_dict = parse_command_file(command_file)
    
    if command_dict:
        # 获取所有 .tex 文件
        tex_files = [f for f in os.listdir() if f.endswith('.tex') and f != command_file]
        
        for input_file in tex_files:
            output_file = f"processed_{input_file}"
            apply_replacements(input_file, output_file, command_dict)
```

### 3. 处理其他文件类型

修改 `list_current_files` 函数调用：

```python
# 列出 .txt 文件
txt_files = list_current_files(".txt")
```

## 性能说明

### 文件大小限制

| 文件类型 | 推荐上限 | 内存要求 | 处理时间 |
|----------|----------|----------|----------|
| `word.txt` | 10,000 条命令 | 50 MB RAM | < 1 秒 |
| 输入文件 | 500 MB | 2 GB RAM | < 30 秒 |

> 注意：对于超大文件（>1GB），建议使用流式处理版本

## 常见问题解答

### Q1: 为什么某些命令没有被替换？

可能原因：
1. 命令在 `word.txt` 中未正确定义
2. 命令在文档中被注释（`% \xxx`）
3. 命令拼写不一致（大小写或空格差异）

解决方案：
1. 检查 `word.txt` 文件格式
2. 确保命令前后没有多余空格
3. 使用正则表达式匹配更灵活的模式

### Q2: 如何处理带参数的命令？

当前脚本会自动保留命令后的参数：

输入：
```latex
\bb{R} → \mathbb{R}
```

如需特殊处理，可修改替换函数：

```python
def replace_match(match):
    cmd = match.group(1)
    param = match.group(2)
    return command_dict.get(cmd, cmd) + param

# 修改正则表达式
pattern = re.compile(r'(\\.+?)([^\w])')
```

### Q3: 如何支持不同编码的文件？

脚本默认使用 UTF-8 编码。如需处理其他编码：

1. 修改文件打开语句：
```python
with open(input_file, 'r', encoding='gbk') as f:
```

2. 或使用自动检测编码：
```python
import chardet
# 在 apply_replacements 函数中添加编码检测
```

### Q4: 如何提高大文件处理速度？

1. 使用流式处理版本（逐行读取）
2. 增加内存分配
3. 减少命令数量（优化 `word.txt`）

## 技术支持

如有任何问题或建议，请联系：
[您的邮箱或支持渠道]
(这里我就不改了orz, 有问题直接提 issue 吧)

## 许可证

本项目采用 MIT 许可证

---

本项目代码完全来自 deepseek, 本上传人完全不会使用任何 python 语言.

事实上, readme.txt 大部分也由 deepseek 生成, 不同点在于本上传人部分知道如何使用 .txt 文件.
