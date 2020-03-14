import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup
import pandas as pd

def get_html(url, data = None):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'Cookie': 'bid="hsM53yRAjQ8"; __utma=30149280.907110929.1386117661.1398322932.1398335444.20; __utmz=30149280.1398167843.17.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=urllib2%20403; ll="118281"; __utma=223695111.1156190174.1396328833.1398322932.1398335444.11; __utmz=223695111.1396588375.4.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=30149280.1.10.1398335444; __utmc=30149280; __utmb=223695111.1.10.1398335444; __utmc=223695111'
                  }

    timeout = random.choice(range(80, 100))
    while True:
        try:
            response = requests.get(url, headers = header, timeout = timeout)

            response.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print(e)
            time.sleep(random.choice(range(20, 60)))
        except socket.error as e:
            print(e)
            time.sleep(random.choice(range(0, 60)))
        except http.client.BadStatusLine as e:
            print(e)
            time.sleep(random.choice(range(30, 60)))
        except http.client.IncompleteRead as e:
            print(e)
            time.sleep(random.choice(range(20, 60)))
    return response.text
    
def get_data(html_text, rank):
    book_info = {'year': [], 'tags': [], 'book_name': []}
    bs = BeautifulSoup(html_text, "html.parser")
    content = bs.find_all('div', {'class': 'title'})
    for book in content:
        try:
            hbook_link = book.find('a').get('href')
            book_html = get_html(hbook_link)
            book_html = BeautifulSoup(book_html, "html.parser")
            book_name = book_html.find('title').text
            print(book_name)
            inf = book_html.find('div', {'id': 'info'})
            for inf_item in inf.find_all('span', {'class': 'pl'}):
                key = inf_item.next_element
                if key=='出版年:':
                    year = key.next_element
                    break
            tags = []
            for tag in book_html.find_all('a', {'class': ' tag'}):
                tags.append(tag.text)
            book_info['year'].append(year)
            book_info['tags'].append(tags)
            book_info['book_name'].append(book_name)
        except:
            pass
    return book_info


        
if __name__ == '__main__':
    print("Starting Spider \t {}".format(time.ctime(time.time())))
    # book_list = pd.read_csv('result.csv').to_dict()
    book_list = {'year': [], 'tags': [], 'book_name': []}
    for page in range(0, 648, 25):
        url = "https://www.douban.com/doulist/1264675/?start={}".format(page)
        html = get_html(url)
        result = get_data(html, page+1)

        book_list['year'] += result['year']
        book_list['tags'] += result['tags']
        book_list['book_name'] += result['book_name']
        df = pd.DataFrame.from_dict(book_list)
        df.to_csv('result.csv')
        # break

        