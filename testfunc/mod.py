import os
import re
import time
 
import requests
from lxml import etree
 
 
def iterate_path(path):
    '''
    遍历我的世界mod文件夹，将可能的mod列表返回（因为现在的mod名称识别是机器识别，后面我想加入语言识别，单词通顺才加入mod列表并返回）
    :param path:mod路径
    :return:mod名称列表，供爬虫搜索
    '''
 
    # 遍历目录
    List_dir = os.listdir(path)
    # 处理前缀问题，如果前缀相同，先把前缀删去
    re_mod = re.compile(r'[^_\-(（]+')
    mod_List = []
    mod_List2 = []
    chongfu = []
    # 首先全部遍历一次
    for i in List_dir:
        tmp1 = re_mod.search(i)
        if tmp1:
            mod_List2.append(tmp1.group())
        else:
            mod_List2.append(i[:-4])
    # 统计每个元素的个数，如果大于1，就加入重复前缀列表
    for i in range(len(mod_List2)):
        tmp = mod_List2.count(mod_List2[i])
        if tmp > 1 and mod_List2[i] not in chongfu:
            chongfu.append(mod_List2[i])
    # 再次遍历，将最后的mod名称列表返回
    for i in List_dir:
        tmp1 = re_mod.findall(i)
        if tmp1[0] not in chongfu and tmp1 != None:
            mod_List.append(tmp1[0])
        elif tmp1[0] in chongfu:
            mod_List.append("".join(tmp1[:2]))
        else:
            mod_List.append(i[:-4])
    # print(mod_List)
    return mod_List
 
 
def crawl(List_mod):
    '''
    通过mod列表进行网站检索，并把运行环境写入result.txt文件，供用户使用
    :param List_mod: mod名称列表
    :return:
    '''
 
    # 请求头设置
    header = {
        "Cookie": "1111111111111111",
        "User-Agent": "1111111111"
    }
 
    # 遍历mod名称列表，进行爬取
    for key in List_mod:
        # xpath路径  外层搜索xpath
        xpath1 = "/html/body/div[2]/div/div[2]/div/div[4]/div/div[1]/div[1]/a//@href"
        # 确定url
        url = f"https://search.mcmod.cn/s?key={key}&site=&filter=1&mold=0"
        # 进行尝试，并设置重试次数
        ci = 1
        while True:
            res = requests.request("get", url=url, headers=header)
            xhtml = etree.HTML(res.text)
            mod_href = xhtml.xpath(xpath1)
            if mod_href == []:
                if ci > 5:
                    with open("result.txt", "a+", encoding='utf-8') as file:
                        file.write(key + " 获取失败\n")
                    print(key + " 获取失败\n")
                    break
                print(f'获取失败了，正在重试这个链接{ci}/5:' + url)
                ci += 1
                time.sleep(2)
                continue
            else:
                break
        if ci > 5:
            continue
        print('获取链接成功 ' + str(mod_href) + " ", end='')
        # 内层xpath
        xpath2 = "/html/body/div[3]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/ul/li[3]//text()"
        # xpath2 = "/html/body/div[3]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/ul/li[3]
        xpath3 = "/html/body/div[3]/div/div[2]/div[2]/div[1]/div[1]//text()"
        #查找环境设置并写入文件
        res = requests.request("get", url=mod_href[0], headers=header)
        xhtml = etree.HTML(res.text)
        ispel_txt = key + " 搜索到的MOD：" + str("|".join(xhtml.xpath(xpath3))) + " " + str(xhtml.xpath(xpath2)[0])
        with open("result.txt", "a+", encoding='utf-8') as file:
            file.write(ispel_txt + "\n")
        print(ispel_txt)
 
        time.sleep(3)
 
 
if __name__ == "__main__":
    # 获取mod列表
    path = r"G:\PCL\.minecraft\versions\tinker journey\mods"
    List_mod = iterate_path(path)
    # 进行mod检索  用的是https://www.mcmod.cn/
    List_Unavailable_mod = crawl(List_mod)

    