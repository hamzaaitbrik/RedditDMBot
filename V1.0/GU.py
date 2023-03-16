import requests
import json

data = []
keywords = ['Reddit', 'Karma', 'Free', 'Karma4Karma', 'Free Karma']
api_url = r'https://api.pushshift.io/reddit/search/comment/?q='
scrape_urls = []
lu = []
du = {}
for keyword in keywords:
    scrape_urls.append(str(api_url + keyword + '&size=100'))




def main(lu):
    get_usernames(scrape_urls)
    write2json()
    print(f'Collected {len(lu)} users')


def get_usernames(scrape_urls):
    for scrape_url in scrape_urls:
        response = requests.get(scrape_url)
        data.append(json.loads(response.content.decode()))
    for dict in data:
        for i in range(100):
            #print(i)
            #print(dict['data'][i]['author'])
            if(dict['data'][i]['author'] not in lu and dict['data'][i]['author'] != 'AutoModerator'):
                lu.append(dict['data'][i]['author'])
                #print(f'length is: {len(usernames)}')
    #print(f'Sending messages to {len(usernames)} users...')
    for i in range(len(lu)):
        du[f'{i}'] = lu[i]

def write2json():
    json_data = json.dumps(du, indent = 4)
    with open('usernames.json', 'w') as outfile:
        outfile.write(json_data)



if __name__ == '__main__':
    main(lu)
