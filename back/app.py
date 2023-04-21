import requests, json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, render_template
from flask_cors import CORS,cross_origin 

# def search_by_list(name):
#     url = f"https://www.imdb.com/find/?q={name.replace(' ', '%20')}&s=tt&exact=true&ref_=fn_tt_ex"
#     res = requests.get(url, headers=headers)
#     html = BeautifulSoup(res.text, 'html.parser')
#     script = html.find("script", {"id": "__NEXT_DATA__"})
#     data = [ i["id"] for i in json.loads(script.text)["props"]["pageProps"]["titleResults"]["results"] ]
#     result = []
#     with ThreadPoolExecutor(max_workers=len(data) if len(data)>0 else 1) as executor:
#         for i in executor.map(search_by_id, data):
#             result.append(i)
#     return result

app=Flask(__name__)

app.config['CORS_ORIGINS'] = ["http://localhost:5173"]
app.config['CORS_METHODS'] = ['GET', 'POST', 'PUT', 'DELETE']
app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']

CORS(app)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def search_by_list(name):
    url = f"https://www.imdb.com/find/?q={name.replace(' ', '%20')}&s=tt&exact=true&ref_=fn_tt_ex"
    res = requests.get(url, headers=headers)
    html = BeautifulSoup(res.text, 'html.parser')
    script = html.find("script", {"id": "__NEXT_DATA__"})
    data = [i["id"] for i in json.loads(script.text)["props"]["pageProps"]["titleResults"]["results"]]
    if data:  # check if data is not empty
        imdb_id = data[0]  # get the first IMDb ID from the list
        result = search_by_id(imdb_id)  # call search_by_id function with the first IMDb ID
        return result
    else:
        return None  # or return an appropriate value when data is empty

def search_by_id(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/"
    res = requests.get(url, headers=headers)
    html = BeautifulSoup(res.text, 'html.parser')
    script = html.find("script", {"id": "__NEXT_DATA__"})
    data = json.loads(script.text)["props"]["pageProps"]["aboveTheFoldData"]
   
    result = {}
    
    result['id']= data['id']
    
    try:
        result["titleText"] = data["titleText"]["text"]
        result["imdb"] = url
        result["productionStatus"] = data["productionStatus"]["currentProductionStage"]["text"] if data["productionStatus"] else ""
        result["titleType"] = data["titleType"]["text"]
        result["releaseDate"] = data["releaseDate"]["year"] if data["releaseDate"] else ""
        result["ratingsSummary"] = data["ratingsSummary"]["aggregateRating"]
        result["primaryImage"] = data["primaryImage"]["url"] if data["primaryImage"] else ""
        result["primaryVideos"] = [i["node"]["playbackURLs"][0]["url"] for i in data["primaryVideos"]["edges"]]
        result["genres"] = [i["text"] for i in data["genres"]["genres"]]
        result["plot"] = data["plot"]["plotText"]["plainText"] if data["plot"] else ""
        result["castPageTitle"] = [i["node"]["name"]["nameText"]["text"] for i in data["castPageTitle"]["edges"]]
        result["directorsPageTitle"] = [i["name"]["nameText"]["text"] for i in data["directorsPageTitle"][0]["credits"]] if data["directorsPageTitle"] else []
        result["countriesOfOrigin"] =  [i["id"] for i in data["countriesOfOrigin"]["countries"]] if data["countriesOfOrigin"] else []
    except Exception as ex:
        result["error"] = str(ex)
    
    return result

# movies=[]
# tv_shows=['Planet+Earth+II', 'Breaking+Bad', 'Planet+Earth', 'Band+of+Brothers', 'Chernobyl', 'The+Wire', 'Avatar:+The+Last+Airbender', 'Blue+Planet+II', 'The+Sopranos', 'Cosmos:+A+Spacetime+Odyssey', 'Cosmos', 'Our+Planet', 'Game+of+Thrones', 'The+World+at+War', 'Rick+and+Morty', 'Hagane+no+renkinjutsushi', 'The+Last+Dance', 'Life', 'The+Twilight+Zone', 'Sherlock', 'Bluey', 'The+Vietnam+War', 'Batman:+The+Animated+Series', 'Scam+1992:+The+Harshad+Mehta+Story', 'Shingeki+no+Kyojin', 'Arcane:+League+of+Legends', 'The+Blue+Planet', 'The+Office', 'Human+Planet', 'Firefly', 'Frozen+Planet', 'Better+Call+Saul', 'Death+Note:+Desu+nôto', "Clarkson's+Farm", 'Only+Fools+and+Horses....', 'The+Civil+War', 'Hunter+x+Hunter', 'True+Detective', 'Seinfeld', 'Dekalog', 'Sahsiyet', 'The+Beatles:+Get+Back', 'Fargo', 'Kaubôi+bibappu:+Cowboy+Bebop', 'Nathan+for+You', 'Gravity+Falls', 'When+They+See+Us', 'Last+Week+Tonight+with+John+Oliver', 'Friends', 'Apocalypse:+La+2ème+guerre+mondiale', 'Africa', 'TVF+Pitchers', "It's+Always+Sunny+in+Philadelphia", "Monty+Python's+Flying+Circus", 'Taskmaster', 'The+Last+of+Us', 'Das+Boot', 'Gibi', 'The+West+Wing', 'Curb+Your+Enthusiasm', 'Leyla+ile+Mecnun', 'Fawlty+Towers', 'Succession', 'Pride+and+Prejudice', 'Freaks+and+Geeks', 'Blackadder+Goes+Forth', 'Twin+Peaks', 'BoJack+Horseman', 'Black+Mirror', 'Narcos', 'Dragon+Ball+Z', "Chappelle's+Show", 'One+Piece:+Wan+pîsu', 'Dragon+Ball+Z:+Doragon+bôru+zetto', 'I,+Claudius', 'South+Park', 'Over+the+Garden+Wall', 'Rome', 'Six+Feet+Under', 'Kota+Factory', 'Peaky+Blinders', 'Ted+Lasso', 'Oz', 'Dark', 'Steins;Gate', 'The+Boys', 'Arrested+Development', 'Fleabag', 'Gullak', 'The+Simpsons', 'The+Mandalorian', 'One+Punch+Man:+Wanpanman', 'The+Shield', 'Battlestar+Galactica', 'House+M.D.', 'Panchayat', 'Downton+Abbey', 'Vinland+Saga', 'Severance', 'Invincible', 'Stranger+Things', 'Mad+Men', 'Peep+Show', 'Sarabhai+V/S+Sarabhai', 'Star+Trek:+The+Next+Generation', 'The+Adventures+of+Sherlock+Holmes', 'The+Marvelous+Mrs.+Maisel', 'Kenpuu+Denki+Berserk', 'Friday+Night+Lights', 'The+Grand+Tour', 'House+of+Cards', 'Top+Gear', 'Justice+League+Unlimited', '1883', 'The+Thick+of+It', 'Line+of+Duty', 'The+Crown', 'Mahabharat', 'Aspirants', 'Behzat+Ç.:+Bir+Ankara+Polisiyesi', 
# 'Father+Ted', 'Deadwood', 'This+Is+Us', 'Parks+and+Recreation', 'The+X+Files', 'Dexter', 'Atlanta', 'Naruto:+Shippûden']
# movies_data=[]
# tv_shows_data=[]
# print('here')
# for movie in tv_shows:
#     tv_shows_data.append(search_by_list(movie))
#     print(tv_shows_data)
    
# with open('movie_data.json','w') as file:
#     json.dump(tv_shows_data, file,indent=4)

@app.route("/api/")
@cross_origin()

def api_page():
    return {"msg":"Welcome to this api", "url": ["/api/", "/api/search/", "/api/search/?q=john+wick"]}
    
@app.route("/api/test")
@cross_origin()

def api_test():
    return json.load(open("data.json", "r", encoding="utf8"))
    
@app.route("/api/search/")
@cross_origin()
def api_search():
    if request.args.get('q'):
        
        result = search_by_list(request.args.get('q'))
        return {"msg": result}
    else:
        return {"msg":"are you looking for something?"}

if __name__ == "__main__":
    app.run(debug=True)