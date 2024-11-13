import requests
from lxml import etree
import csv
import time

def get_env(moddata):

    result = []
    result.append(["index","real-mod","which-found","clinet","server"])
    # 请求头设置
    header = {
        "Cookie": "1111111111111111",
        "User-Agent": "1111111111"
    }

    url_head = f"https://www.mcmod.cn/class/"
    xpath = "/html/body/div[3]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/ul/li[3]//text()"


    with open(moddata,"r+",encoding="utf-8") as file:
        content = csv.reader(file)
        for mod in content:
            if mod[0] == "index":
                continue
            elif mod[0] == "None":
                result.append(mod)
            else:
                response = requests.request("get", url=url_head+mod[0]+".html", headers=header)
                xhtml = etree.HTML(response.text)
                result.append(mod+[v for v in str(str(xhtml.xpath(xpath)[0]).split(":")[1]).split(",")])
                print(f"{mod[0]} 已添加！")
                time.sleep(1)
    return result

if __name__ =="__main__":

    moddata = "result.csv"
    result = get_env(moddata)

    with open("final.csv","w",encoding="utf-8") as f:
        writer = csv.writer(f,lineterminator="\n")
        writer.writerows(result)

    print("task finished!")
