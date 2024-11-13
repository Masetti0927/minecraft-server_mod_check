import re
import os
import pprint
import StringCheck as sc

# 指定你要读取的文件夹路径
folder_path = r"G:\PCL\.minecraft\versions\tinker journey\mods"

# 获取文件夹内所有文件名
file_names = os.listdir(folder_path)

# pprint.pprint(file_names)

pattern = re.compile(r"(.disabled)|(jar)|[-_+\.][-]?((mc)|(fabric)|(Forge)|(build)|(pre)|(universal)|(release)|(all)|([\(\){a}{R,r}{V,v}{X,x}\.\d]))+|[-]",re.I)

res = []

for i in file_names:

    todel = re.findall(pattern,i)
    new = re.sub(pattern,'',i)
    res.append(new)

print("mod列表获取完毕")
# pprint.pprint(res)

def read_file_line_by_line(file_path):
    with open(file_path, 'r',encoding="utf-8") as file:
        for line in file:
            yield line.strip()  # 使用 yield 返回每一行，strip() 用于去除行尾的换行符
 
# 使用例子
file_path = 'ModData.txt'

for mod in res:
    for line in read_file_line_by_line(file_path):
        if sc.similarity(mod,line) >= 0.85:
            print(f"{mod}: {line}",end="\n")

def read_file_line_by_line(file):
        for line in file:
            yield line.strip()


def get_middle_lines(file_path, start_line, num_lines):
    with open(file_path, 'r',encoding='utf-8') as file:
        # 跳过开始行之前的内容
        for _ in range(start_line - 1):
            next(file)
        # 读取指定数量的行
        return [next(file).rstrip() for _ in range(num_lines)]
 

start_line = 500  # 从第500行开始
num_lines = 1000  # 读取1000行
 
lines = get_middle_lines(file_path, start_line, num_lines)
for line in lines:
    print(line,lines.index(line)+start_line)