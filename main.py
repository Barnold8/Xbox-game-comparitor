import requests
import sys


def uses():

    print("TODO")
    exit()


def main():

    game = ""

    if(len(sys.argv) != 2):
        uses()
    
    r = requests.get(sys.argv[1])
    game = ' '.join(sys.argv[1].split("=")[1].split("+"))
  


main()
