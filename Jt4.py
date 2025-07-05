import re
import os
import sys

def parse_command_file(command_file):
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

def apply_replacements(input_file, output_file, command_dict):
    try:
        # 按命令长度降序排序
        sorted_commands = sorted(command_dict.keys(), key=len, reverse=True)
        
        # 构建正则表达式模式
        pattern = re.compile('|'.join(re.escape(cmd) for cmd in sorted_commands))
        
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as fin:
            content = fin.read()
        
        # 替换函数
        def replace_match(match):
            matched_str = match.group(0)
            return command_dict.get(matched_str, matched_str)
        
        # 应用所有替换
        modified_content = pattern.sub(replace_match, content)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as fout:
            fout.write(modified_content)
        
        print(f"成功处理文件！已将 {os.path.basename(input_file)} 中的命令替换")
        print(f"结果保存至: {os.path.abspath(output_file)}")
        return True
    
    except FileNotFoundError:
        print(f"错误：找不到文件 '{input_file}'")
        return False
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return False

def get_absolute_path(input_path):
    """将相对路径转换为绝对路径"""
    if not os.path.isabs(input_path):
        # 如果不是绝对路径，则基于脚本所在目录创建绝对路径
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), input_path)
    return input_path

def list_current_files(extension=".txt"):
    """列出当前目录下的指定扩展名文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files = [f for f in os.listdir(script_dir) 
             if os.path.isfile(os.path.join(script_dir, f)) and f.endswith(extension)]
    
    if files:
        print(f"\n当前目录下的 {extension} 文件:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
    else:
        print(f"\n当前目录下没有 {extension} 文件")
    
    return files

if __name__ == "__main__":
    # 设置工作目录为脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"当前工作目录: {os.getcwd()}")
    
    # 配置文件路径 - 使用相对路径
    command_file = "word.txt"
    
    # 列出当前目录下的文件
    txt_files = list_current_files()
    
    # 获取用户输入
    try:
        input_file = input("\n请输入要处理的文件名（直接输入名称或编号）: ").strip()
        output_file = input("请输入输出文件名: ").strip()
        
        # 如果输入的是数字，选择对应的文件
        if input_file.isdigit():
            index = int(input_file) - 1
            if 0 <= index < len(txt_files):
                input_file = txt_files[index]
            else:
                print("错误：无效的文件编号")
                sys.exit(1)
        
        # 如果输出文件名为空，则自动生成
        if not output_file:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_output.txt"
            print(f"自动生成输出文件名: {output_file}")
        
        # 确保文件路径正确
        input_file = get_absolute_path(input_file)
        output_file = get_absolute_path(output_file)
        
        # 解析命令文件
        command_dict = parse_command_file(command_file)
        
        if command_dict:
            # 应用替换规则
            apply_replacements(input_file, output_file, command_dict)
        
    except KeyboardInterrupt:
        print("\n程序已取消")
        sys.exit(0)