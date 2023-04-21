import requests
from bs4 import BeautifulSoup


url="https://www.imdb.com/chart/toptv/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
response = requests.get(url,headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

body = soup.find_all("td",class_="titleColumn")
list=[]
for b in body:
    data=b.find('a')   
    list.append(data.text)

new_list=[] 

for item in list:
    new_item=item.replace(' ','+')
    new_list.append(new_item)
print(new_list)