import argparse
import textwrap
import warnings
from multiprocessing.dummy import Pool
import requests
import urllib3
from lxml import etree


def main():
    urllib3.disable_warnings()
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser(description="一个代码执行工具",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''示例：python 1111.py -u www.baidu.com / -f url.txt'''))
    parser.add_argument("-u", "--url", dest="url", help="请输入要检测的url地址")
    parser.add_argument("-f", "--file", dest="file", help="请输入要批量检测的文件")
    args = parser.parse_args()
    urls=[]
    if args.url:
        if "http" not in args.url:
            args.url = f"http://{args.url}"
        check(args.url)
    elif args.file:
        with open(f"{args.file}","r") as f:
            for i in f:
                u=i.strip()
                if "http" not in u:
                    u=f"http://{u}"
                    urls.append(u)
                else:
                    urls.append(u)
    pool=Pool(30)
    pool.map(check,urls)


def check(url):
    u = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
    }
    try:
        a=requests.get(url=u, headers=headers, timeout=3)
        a.encoding='utf-8'
        html = a.text
        tree = etree.HTML(html)
        title = tree.xpath('//title/text()')[0]
        b=a.status_code
        if b==200:
            print('网站存活，标题:', title,"网站:",u)
    except Exception as i:
        print("网站不存活",u)


if __name__=='__main__':
    banner='''
    $$\                                                                   
$$ |                                                                  
$$$$$$$\   $$$$$$\   $$$$$$\  $$\   $$\  $$$$$$\  $$$$$$$\   $$$$$$\  
$$  __$$\  \____$$\ $$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ 
$$ |  $$ | $$$$$$$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |
$$ |  $$ |$$  __$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |\$$$$$$$ |\$$$$$$  |\$$$$$$$ |\$$$$$$  |$$ |  $$ |\$$$$$$$ |
\__|  \__| \_______| \______/  \____$$ | \______/ \__|  \__| \____$$ |
                              $$\   $$ |                    $$\   $$ |
                              \$$$$$$  |                    \$$$$$$  |
                               \______/                      \______/ 
                                                                                                                                                                                                                                                               
    '''
    print(banner)
    main()

