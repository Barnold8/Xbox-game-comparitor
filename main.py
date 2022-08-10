import requests
import sys
from bs4 import BeautifulSoup


def uses():

    print("TODO")
    exit()


def soupGet(tag):

    soup = BeautifulSoup(requests.get(sys.argv[1]).text,"html.parser")
    return soup.findAll(tag)


def main():

    if(len(sys.argv) != 2):
        uses()
    
    xbx = soupGet("picture")
    game = ' '.join(sys.argv[1].split("=")[1].split("+"))
      


main()
