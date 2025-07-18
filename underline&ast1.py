import re
import os
import glob
import sys

def escape_formulas(text):
    """
    处理文本中的行内 LaTeX 公式（$...$）：
    1. 将公式内的下划线 _ 替换为 \_
    2. 将公式内的星号 * 替换为 \ast 
    """
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

def process_text_file(input_file):
    """处理单个文本文件"""
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理公式转义
    processed = escape_formulas(content)
    
    # 创建备份文件（原文件名.bak）
    backup_file = input_file + '.bak'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 写入处理后的内容
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(processed)
    
    print(f"✅ 处理完成: {os.path.basename(input_file)}")
    print(f"🔒 备份保存为: {os.path.basename(backup_file)}")
    print("---")

def process_script_directory():
    """处理脚本所在目录下所有.txt文件"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 查找所有.txt文件
    txt_files = glob.glob(os.path.join(script_dir, '*.txt'))
    
    if not txt_files:
        print(f"❌ 在脚本目录 {script_dir} 中未找到 .txt 文件")
        return
    
    print(f"🔍 在脚本目录 {script_dir} 中找到 {len(txt_files)} 个 .txt 文件:")
    for i, file_path in enumerate(txt_files, 1):
        print(f"{i}. {os.path.basename(file_path)}")
    
    proceed = input("\n是否处理所有文件? (y/n): ").strip().lower()
    if proceed != 'y':
        print("操作已取消")
        return
    
    print("\n开始处理文件...")
    for file_path in txt_files:
        process_text_file(file_path)
    
    print("\n✅ 所有文件处理完成!")

if __name__ == "__main__":
    # 获取脚本名称
    script_name = os.path.basename(__file__)
    
    print("=" * 60)
    print(f"LaTeX 公式转义工具 - {script_name}")
    print("功能: 处理 .txt 文件中的行内公式 $...$")
    print("     1. 将公式内的 _ 替换为 \\_")
    print("     2. 将公式内的 * 替换为 \\ast ")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        # 处理单个指定文件
        input_file = sys.argv[1]
        
        # 检查文件是否存在
        if not os.path.exists(input_file):
            print(f"❌ 错误: 文件不存在 - {input_file}")
            sys.exit(1)
        
        # 检查文件扩展名
        if not input_file.lower().endswith('.txt'):
            print(f"⚠️ 警告: 此脚本专为 .txt 文件设计")
            print(f"      您指定的文件: {os.path.basename(input_file)}")
            proceed = input("是否继续处理? (y/n): ").strip().lower()
            if proceed != 'y':
                print("操作已取消")
                sys.exit(0)
        
        process_text_file(input_file)
    else:
        # 没有指定文件，处理脚本所在目录下所有.txt文件
        process_script_directory()
    
    # 添加结束提示
    print("\n按 Enter 键退出...")
    try:
        input()
    except KeyboardInterrupt:
        pass