from multiprocessing import  Pool,Manager
import time,re,os,pprint,csv



def levenshtein_distance(s1, s2)->float: #检查字符串距离
    if len(s1) < len(s2): 
        return levenshtein_distance(s2, s1) 
    if len(s2) == 0: 
        return len(s1) 
    
    previous_row = range(len(s2) + 1) 
    for i, c1 in enumerate(s1): 
        current_row = [i + 1] 
        for j, c2 in enumerate(s2): 
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1 
            substitutions = previous_row[j] + (c1 != c2) 
            current_row.append(min(insertions, deletions, substitutions)) 
        previous_row = current_row 
        
    return previous_row[-1] / max(len(s1), len(s2))

def similarity(s1,s2)->float:#返回相似度
    return 1. - levenshtein_distance(s1,s2)

def checkmod(folder_path)-> list:#获取本地mod列表

    # 获取文件夹内所有文件名
    file_names = os.listdir(folder_path)

    # pprint.pprint(file_names)
    # pattern = re.compile(r"(.disabled)|(jar)|[-_+\.][-]?((mc)|(fabric)|(Forge)|(build)|(pre)|(universal)|(release)|(all)|([\(\){a}{R,r}{V,v}{X,x}\.\d]))+|[-]",re.I)
    pattern = re.compile(r"\[.*?\]+|(.disabled)|(jar)|[-_+\.][-]?((mc)|(fabric)|(forge)|(build)|(pre)|(universal)|(release)|(all)|([\(\){a}{R,r}{V,v}{X,x}\.\d]))+|[-\s]+",re.I)
    res = []

    for i in file_names:
        new = re.sub(pattern,'',i)
        new = re.sub(r"[.\d]+","",new)
        res.append(new.lower().replace("forge",""))
    
    return res

def origin_mod(folder_path):
    return os.listdir(folder_path)

def get_lines(file_path)->list:#拆分数据库中的mod
    with open(file_path, 'r',encoding='utf-8') as file:
        # # 跳过开始行之前的内容
        # for _ in range(start_line - 1):
        #     next(file)
        # # 读取指定数量的行
        # return [next(file).rstrip().lower() for _ in range(num_lines)]
        lines = file.readlines()
        
        return [line.rstrip().lower().replace("forge","").replace("-forge","").replace("-fabric","") for line in lines]

def get_task(file_path):
    
    task = get_lines(file_path)

    for line in range(len(task)):
        if "@" in task[line]:
            if  "@" == task[line][0] :
                task[line] = task[line].split("@")[1]
                if "|" in task[line]:
                    task[line] = task[line].split("|")[0]
            else:
                task[line] = task[line].split("@")[0]
        elif "|" in task[line]:
            task[line] = task[line].split("|")[0]
        elif "¨" in task[line]:
            task[line] = task[line].split("¨")[0]
    
    return task

def worker(task,origin,mod_list,i,result):

    # if step*(i+1)>16810:
    #     task = get_middle_lines(file_path,step*i,16810-step*i)
    # else:
    #     task = get_middle_lines(file_path,step*i,step)

    task = task

    print(f"worker {i} : {len(task)} start")
            
    mod_list = mod_list
    origin = origin
    while mod_list.empty() == 0:
        found = False
        mod = mod_list.get()
        _mod = origin.get()
        print(f"left mods == {mod_list.qsize()}")
        for line in range(len(task)):
        # print(f"founding {mod}:")
            if task[line] != "":
                if similarity(mod,task[line]) >= 0.75:
                    found = True
                    print(f"{_mod}: {task[line]},index where is {line+1},found from {i} worker",end="\n")
                    result.append([line+1,_mod,task[line]])
                    break
        if not found:
                print(f"{_mod} cant find!")
                result.append(["None",_mod,"None"])
    print(f"the worker {i} ended.")


if __name__ == "__main__":

    # 指定你要读取的文件夹路径
    folder_path = r"G:\PCL\.minecraft\versions\tinker journey\mods"
    file_path = 'ModData.txt'
    mod_list = checkmod(folder_path)
    origin = origin_mod(folder_path)

    start_time = time.time()
    workers = 4

    # mod入队
    q = Manager().Queue()
    for mod in mod_list:
        q.put(mod)
    # 原始mod队列
    _q = Manager().Queue()
    for mod in origin:
        _q.put(mod)
    # 结果队
    result = Manager().list()
    result.append(["index","real-mod","which-found","client","server"])

    # mod数据库
    task = get_task(file_path)

    # 创建进程池
    with Pool(workers) as pool:
        # 向进程池添加任务
        for i in range(workers):
            pool.apply_async(worker, (task,_q,q,i,result))

        # 等待所有进程完成
        pool.close()
        pool.join()

    # print("All processes are done.")
    end_time = time.time()
    print(f"用时: {end_time-start_time}s")
    # pprint.pprint(list(result))

    # 保存为CSV文件
    with open('result.csv', 'w+', newline='',encoding="utf-8") as file:
        writer = csv.writer(file,lineterminator="\n")
        writer.writerows(result)
