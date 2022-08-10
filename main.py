import requests
import sys
from bs4 import BeautifulSoup


def uses():

    print("TODO")
    exit()


def main():

    game = ""

    if(len(sys.argv) != 2):
        uses()
    
    soup = BeautifulSoup(requests.get(sys.argv[1]).text,"html.parser")
    game = ' '.join(sys.argv[1].split("=")[1].split("+"))
  


main()
