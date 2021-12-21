from bs4 import BeautifulSoup
import pandas as pd
import requests

address_homepage = "https://hopamchuan.com/genre/v/2?offset="

def get_lyrics_from_url(url):
    cont = requests.get(url).content
    soup = BeautifulSoup(cont , "html.parser")
    # Decompose intro 
    for div in soup.find_all("div", {'class':'song-lyric-note'}): 
        div.decompose()
    lyrics = ""
    line = soup.findAll("div" , {"class" : "chord_lyric_line"})
    for l in line:
        li = l.findAll("span" , {"class" : "hopamchuan_lyric"})
        for lii in li:
            lyrics +=(lii.text.strip() + " ")
    print("Done Lyrics - " + url)
    return lyrics


def list_per_offset(id):
    # {
    #     "href"
    #     "name" 
    #     "singer"
    # }
    cont = requests.get(address_homepage + str(id)).content
    soup = BeautifulSoup(cont, "html.parser")
    e_songlist = soup.find("div" , {"class" : "song-list"})
    e_songlist_child = e_songlist.findChildren("div" ,{"class" : "song-item"})
    data = []
    for c in e_songlist_child:
        c_data = {}
        e_find = c.find("a")
        c_data['href'] = e_find['href']
        c_data['name'] = e_find.text.strip()
        print(c_data['name'])
        list_singer = c.findAll("a" , {"class" : "author-item"})
        l_singer = []
        img_singer = []
        for singer in list_singer:
            l_singer.append(singer.text.strip())
            t_url = singer['href']
            t_req = requests.get(t_url)
            t_soup = BeautifulSoup(t_req.text , "html.parser")
            f = t_soup.find("div" , {"id" : "artist-info"}).find('img')
            img_singer.append(f['src'])
        c_data['singer'] = l_singer
        c_data['image'] = img_singer
        c_data['lyrics'] = get_lyrics_from_url(c_data['href'])
        data.append(c_data)
    print("Finished Page  " , id)
    return data



max_v2_offset = 11420 # V2 = nhac_tre

href = []
name = []
singer = []
image = []
lyrics = []

count_csv = 1
for i in range(0, max_v2_offset , 10):
    
    lpp = list_per_offset(i)
    for j in lpp:
        href.append(j['href'])
        name.append(j['name'])
        singer.append(j['singer'])
        image.append(j['image'])
        lyrics.append(j['lyrics'])

    if(len(href) >= 571):
        dict_tocsv = {
            "href" : href ,
            "name" : name ,
            "singer" : singer,
            "image" : image,
            "lyrics" : lyrics, 
        }
        df = pd.DataFrame(dict_tocsv)
        df.to_csv(("test"  + str(count_csv) + ".csv") , encoding='utf-8-sig')
        count_csv += 1
        print("------------------Finished Crawl ---------------")
        href = []
        name = []
        singer = []
        image = []
        lyrics = []
if(len(href) > 0 ):
    dict_tocsv = {
        "href" : href ,
        "name" : name ,
        "singer" : singer,
        "image" : image,
        "lyrics" : lyrics, 
    }
    df = pd.DataFrame(dict_tocsv)
    df.to_csv(("test"  + str(count_csv) + ".csv") , encoding='utf-8-sig')
    count_csv += 1
    print("------------------Finished Crawl ---------------")
    href = []
    name = []
    singer = []
    image = []
    lyrics = []
print("FINISHED !!!!")