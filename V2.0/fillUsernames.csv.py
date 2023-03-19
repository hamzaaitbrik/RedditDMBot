from modules import requests,json,csv,datetime,log
from variables import *
from CONSTANTS import *


log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [fillUsernames] Collecting usernames...')

for keyword in keywords:
    scrape_urls.append(str(API_URL + keyword + '&size=100'))

def getUsernames():
    for scrape_url in scrape_urls:
        response = requests.get(scrape_url)
        data.append(json.loads(response.content.decode()))
    for dict in data:
        for i in range(99):
            if(dict['data'][i]['author'] not in list_usernames and dict['data'][i]['author'] != 'AutoModerator'):
                list_usernames.append(dict['data'][i]['author'])
    for i in range(len(list_usernames)):
        dict_usernames[f'{i}'] = list_usernames[i]
    write2UsernamesCsv()
    log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [fillUsernames] Collected {len(list_usernames)} usernames.')

def write2UsernamesCsv():
    dbUsernames = open('usernames.csv','a',newline='',encoding='utf-8')
    writer = csv.writer(dbUsernames)
    for username in list_usernames:
        writer.writerow(
            [
                str(username)
            ]
        )


def main():
    getUsernames()



if __name__ == '__main__':
    main()
