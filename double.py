import re
import os
import sys
import glob

def parse_command_file(command_file):
    """解析 word.txt 中的 LaTeX 自定义命令"""
    command_dict = {}
    try:
        with open(command_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or not line.startswith(r'\newcommand'):
                    continue
                
                # 使用安全的分割方法
                parts = line.split('\\')
                if len(parts) >= 4:
                    command = '\\' + parts[2]  # 获取 \xxx
                    replacement = '\\' + parts[3]  # 获取 \yyy
                    command_dict[command] = replacement
                
        print(f"从 {os.path.basename(command_file)} 中解析出 {len(command_dict)} 条替换规则")
        return command_dict
    
    except Exception as e:
        print(f"解析命令文件时出错: {str(e)}")
        return {}

def apply_latex_replacements(content, command_dict):
    """应用 LaTeX 命令替换"""
    if not command_dict:
        return content
    
    # 按命令长度降序排序
    sorted_commands = sorted(command_dict.keys(), key=len, reverse=True)
    
    # 构建正则表达式模式
    pattern = re.compile('|'.join(re.escape(cmd) for cmd in sorted_commands))
    
    # 替换函数
    def replace_match(match):
        matched_str = match.group(0)
        return command_dict.get(matched_str, matched_str)
    
    # 应用所有替换
    return pattern.sub(replace_match, content)

def escape_formulas(text):
    """处理 LaTeX 公式中的特殊字符转义"""
    # 匹配 $...$ 公式块（支持多行）
    pattern = re.compile(r'\$(.*?)\$', re.DOTALL)
    
    def replace_in_formula(match):
        formula = match.group(1)
        # 替换下划线（保留转义的下划线）
        formula = re.sub(r'(?<!\\)_', r'\\_', formula)
        # 替换星号（保留转义的星号）
        formula = re.sub(r'(?<!\\)\*', r'\\ast ', formula)
        return f'${formula}$'
    
    return pattern.sub(replace_in_formula, text)

def process_text_file(input_file, output_file, command_dict):
    """主处理函数：按顺序执行两个处理步骤"""
    try:
        # 步骤1：读取输入文件
        with open(input_file, 'r', encoding='utf-8') as fin:
            content = fin.read()
        
        print(f"正在处理文件: {os.path.basename(input_file)}")
        print(f"原始文件大小: {len(content)} 字符")
        
        # 步骤2：应用 LaTeX 命令替换
        content_step1 = apply_latex_replacements(content, command_dict)
        print(f"步骤1完成: 已应用 {len(command_dict)} 条命令替换")
        
        # 步骤3：进行公式转义处理
        content_final = escape_formulas(content_step1)
        print(f"步骤2完成: 已处理公式中的特殊字符转义")
        
        # 步骤4：写入输出文件
        with open(output_file, 'w', encoding='utf-8') as fout:
            fout.write(content_final)
        
        print(f"处理完成!")
        print(f"最终文件大小: {len(content_final)} 字符")
        print(f"结果保存至: {os.path.abspath(output_file)}")
        return True
    
    except FileNotFoundError:
        print(f"错误：找不到文件 '{input_file}'")
        return False
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return False

def list_current_files(extension=".txt"):
    """列出当前目录下的指定扩展名文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files = [f for f in os.listdir(script_dir) 
             if os.path.isfile(os.path.join(script_dir, f)) and f.endswith(extension)]
    
    return files

def show_processing_summary():
    """显示处理流程摘要"""
    print("=" * 70)
    print("LaTeX 文本处理工具 - 集成版")
    print("=" * 70)
    print("处理流程:")
    print("  1. 从 word.txt 读取 LaTeX 自定义命令定义")
    print("  2. 将输入文件中的所有自定义命令替换为完整形式")
    print("  3. 处理行内公式 $...$ 中的特殊字符:")
    print("      - 将公式中的 _ 替换为 \\_")
    print("      - 将公式中的 * 替换为 \\ast")
    print("=" * 70)

def backup_original_file(file_path):
    """创建原始文件的备份"""
    backup_path = file_path + '.bak'
    try:
        with open(file_path, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(content)
        print(f"原始文件已备份为: {os.path.basename(backup_path)}")
        return True
    except Exception as e:
        print(f"备份文件时出错: {str(e)}")
        return False

def main():
    """主函数"""
    # 设置工作目录为脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"当前工作目录: {os.getcwd()}")
    
    # 显示处理摘要
    show_processing_summary()
    
    # 配置文件路径
    command_file = "word.txt"
    
    # 检查命令文件是否存在
    if not os.path.exists(command_file):
        print(f"错误：找不到命令文件 '{command_file}'")
        print("请确保 word.txt 文件与脚本在同一目录下")
        input("按 Enter 键退出...")
        sys.exit(1)
    
    # 列出当前目录下的 .txt 文件
    txt_files = list_current_files()
    
    if txt_files:
        print(f"\n当前目录下的 .txt 文件:")
        for i, file in enumerate(txt_files, 1):
            print(f"  {i}. {file}")
    else:
        print("\n当前目录下没有 .txt 文件")
    
    try:
        # 获取用户输入
        input_file = input("\n请输入要处理的文件名（输入名称或编号）: ").strip()
        
        # 如果输入的是数字，选择对应的文件
        if input_file.isdigit():
            index = int(input_file) - 1
            if 0 <= index < len(txt_files):
                input_file = txt_files[index]
            else:
                print("错误：无效的文件编号")
                sys.exit(1)
        
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            print(f"错误：文件 '{input_file}' 不存在")
            sys.exit(1)
        
        # 询问输出文件名
        default_output = os.path.splitext(input_file)[0] + "_processed.txt"
        output_prompt = f"请输入输出文件名 (回车使用默认: {default_output}): "
        output_file = input(output_prompt).strip()
        
        if not output_file:
            output_file = default_output
            print(f"使用默认输出文件名: {output_file}")
        
        # 检查输出文件是否已存在
        if os.path.exists(output_file):
            overwrite = input(f"警告: 文件 '{output_file}' 已存在，是否覆盖? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("操作已取消")
                sys.exit(0)
        
        # 如果输出文件与输入文件相同，创建备份
        if os.path.abspath(input_file) == os.path.abspath(output_file):
            backup_original_file(input_file)
        
        # 解析命令文件
        print("\n正在解析命令文件...")
        command_dict = parse_command_file(command_file)
        
        if not command_dict:
            print("警告：未找到可用的替换规则，将只进行公式转义处理")
        
        # 处理文件
        print("\n开始处理文件...")
        success = process_text_file(input_file, output_file, command_dict)
        
        if success:
            print("\n✅ 文件处理完成!")
        else:
            print("\n❌ 文件处理失败")
        
    except KeyboardInterrupt:
        print("\n程序已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生未预期的错误: {str(e)}")
    
    # 结束提示
    print("\n按 Enter 键退出...")
    try:
        input()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()