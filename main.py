import requests
import sys
from bs4 import BeautifulSoup


#Note: program only works with the preview of a search on xbox games. Using "see all" may provide
#undefined behaviour

#side Note: I know it would be better for the code base if the classes derived from one parent class but
            # im not entirely bothered for this simple program

class XBX_GME: # a struct for compiling game items from the xbox store

    def __init__(self):

        self.name = ""
        self.rating = ""
        self.price = ""
   
    def setData(self,arr):
        #print(arr)
        self.name = arr[1]
        self.rating = arr[3]
        self.price = arr[5]
    
    def printDAT(self):

        print("Game is: "+self.name)
        print("The price: "+self.price)

class ENEBA:
    

    def __init__(self):
        self.name = ""
        self.price = ""

    def setData(self,string,w_count):
        
        self.price = string.split(" ")[len(string.split(" "))-1]
        for i in range(w_count):
            self.name += string.split(" ")[i] 

    def printDAT(self):

        print("Name of the game: "+self.name)
        print("Price of the game: "+self.price)

def uses():

    print("USE: main.py [URL]")
    print("Example: main.py https://www.xbox.com/en-gb/Search?q=forza+horizon+5")
    exit()



def linkMaker(site,game): # site will be type int to determine what site we get games from
                          # function returns type str, the link needed to process games
    # 0 = cdkeys
    # 1 = eneba
    # 2 = G2A

    #https://www.cdkeys.com/catalogsearch/result/?q=house%20flipper&platforms=Xbox%20Live
    if site == 0: 
        return "https://www.cdkeys.com/catalogsearch/result/?q={}&platforms=Xbox%20Live".format(game.replace(" ","%20"))
    
    #https://www.eneba.com/gb/store/xbox-games?page=1&platforms[]=XBOX&text=mortal%20shell&typ&types[]=game
    elif site == 1:
        return "https://www.eneba.com/gb/store/xbox-games?page=1&platforms[]=XBOX&text={}&typ&types[]=game".format(game.replace(" ","%20"))

    #https://www.g2a.com/category/gaming-c1?f[drm][0]=273&query=mortal%20shell
    

def soupGet(tag_,class_,link_ = None):
    
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    
    if link_ == None:
        cookies = requests.head(sys.argv[1])
        soup = BeautifulSoup(requests.get(sys.argv[1],cookies=cookies,headers=headers).text,"html.parser")
    else:
        cookies = requests.head(link_)
        soup = BeautifulSoup(requests.get(link_,cookies=cookies,headers=headers).text,"html.parser")

    if class_ == None:
        return soup.findAll(tag_)
    else:
        return soup.findAll(tag_,{"class":class_})


def xbx_games():
    
    xbox_games = []

    xbx = soupGet("section","m-product-placement-item f-size-medium context-movie") # could easily break
    game = ' '.join(sys.argv[1].split("=")[1].split("+"))                           # if microsoft change
                                                                                    # site data
    if len(xbx) <= 0:
        print("No games were found in the xbox search query")
        uses() 

    for i in range(len(xbx)):
        if "Game" in xbx[i].text:
            x = xbx[i].text.split("\n")
            x = [x for x in x if x]
            if len(x) < 6:
                continue
            f = XBX_GME()
            f.setData(x)
            xbox_games.append(f)
    
    return xbox_games

def enebaGames():

    eneba = []

    chars = "$ £ €".split(' ')
    
    game = ' '.join(sys.argv[1].split("=")[1].split("+")) 
    
    word_count = len(game.split(" "))
    
    x = soupGet("div",None,linkMaker(1,game))
    
    for f in x:
        if game.lower() in f.text.lower():
            for c in chars :
                if c in f.text and len(f.text) < 100: # used to filter out spammy results
                    a = ENEBA()
                    a.setData(f.text,word_count)
                    eneba.append(a)
    return eneba

def cdKeys_games(): # Current bug: returns home page instead of query

    games = []

    chars = "$ £ €".split(' ')
    
    game = ' '.join(sys.argv[1].split("=")[1].split("+")) 
 
    word_count = len(game.split(" "))
    
    x = soupGet("div",None,linkMaker(0,game))
    #for elem in x:
     #   print(elem.text)
      #  input("Press Enter")

    return

def mon_conv(price): 

    sign = price[0]
    mon = float(price.split(sign)[1])
    
    eur = 1.18554
    doll = 1.19950  

    #print(type(mon))

    if sign == "$":
        return  "£" + "{0:.2f}".format((mon / doll))
    elif sign == "€":
        return "£"+"{0:.2f}".format((mon / eur))
    else:
        return

def lowest(arr1,arr2): # if 0, arr1 has lower price, else arr2 has lowest

    for elem in arr1:
        print(elem.price)
        lowest =  float(elem.price.split("£")[1])
    print("="*40)
    for elem in arr2:
        print(elem.price)
        if float(elem.price.split("£")[1]) < lowest:
            return 1
    return 0

def main():

    if(len(sys.argv) != 2):
        uses()                 

    xbox_games = xbx_games()
   # cd_keys = cdKeys_games()
    eneba_games = enebaGames()
    
    for elem in eneba_games:
        elem.price = mon_conv(elem.price)
    print(lowest(xbox_games,eneba_games))


main()
