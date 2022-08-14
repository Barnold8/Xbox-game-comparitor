import requests
import sys
from bs4 import BeautifulSoup


#Note: program only works with the preview of a search on xbox games. Using "see all" may provide
#undefined behaviour

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
        print("It's rating: "+self.rating)
        print("The price: "+self.price)


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
        x = "https://www.cdkeys.com/catalogsearch/result/?q={}&platforms=Xbox%20Live".format(game.replace(" ","%20"))
        print(x)



def soupGet(tag_,class_):

    soup = BeautifulSoup(requests.get(sys.argv[1]).text,"html.parser")
    
    if class_ == None:
        return soup.findAll(tag_)
    else:
        return soup.findAll(tag_,{"class":class_})


def xbx_games():
    
    xbox_games = []

    xbx = soupGet("section","m-product-placement-item f-size-medium context-movie") # could easily break
    game = ' '.join(sys.argv[1].split("=")[1].split("+"))                           # if microsoft change
                                                                                    # site data
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

def main():

    if(len(sys.argv) != 2):
        uses()                 

    xbox_games = xbx_games()
    linkMaker(0,"Hello neighbour")

main()
