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
        self.rating = 0.0
        self.price = 0.0
   
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
    elif site == 2:
        return "https://www.g2a.com/category/gaming-c1?f[drm][0]=273&query={}".format(game.replace(" ","%20"))


def soupGet(tag_,class_,link_ = None):

    if link_ == None:
        soup = BeautifulSoup(requests.get(sys.argv[1]).text,"html.parser")
    else:
        soup = BeautifulSoup(requests.get(link_).text,"html.parser")

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

def cdKeys_games():

    games = []

    chars = "$ £ €".split(' ')
    
    game = ' '.join(sys.argv[1].split("=")[1].split("+")) 
    
    word_count = len(game.split(" "))
    
    x = soupGet("div",None,linkMaker(0,game))
    
    
    return

   

def g2a_games():
    
    pass

def main():

    if(len(sys.argv) != 2):
        uses()                 

    xbox_games = xbx_games()
    cd_keys = cdKeys_games()
    eneba_games = enebaGames()
    g2a = g2a_games()
    for elem in eneba_games:
        elem.printDAT()

main()
