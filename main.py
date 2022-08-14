import requests
import sys
from bs4 import BeautifulSoup


class XBX_GME: # a struct for compiling game items from the xbox store

    def __init__(self):

        self.name = ""
        self.rating = 0
        self.price = 0.0
    

def uses():

    print("TODO")
    exit()


def soupGet(tag_,class_):

    soup = BeautifulSoup(requests.get(sys.argv[1]).text,"html.parser")
    
    if class_ == None:
        return soup.findAll(tag_)
    else:
        return soup.findAll(tag_,{"class":class_})

def main():


    xbox_games = []

    if(len(sys.argv) != 2):
        uses()
    
    xbx = soupGet("section","m-product-placement-item f-size-medium context-movie")
    game = ' '.join(sys.argv[1].split("=")[1].split("+"))
    for i in range(len(xbx)):
        if "Game" in xbx[i].text:
            x = xbx[i].text.split("\n")
            x = [x for x in x if x]
            print(x)

main()
