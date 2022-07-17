#from config.settings import webpage
from src.dateResearcher import run
from tools.io import get_keys

def main():
    WEBPAGE, USER, PWD = get_keys()
    run(WEBPAGE, USER, PWD)


if __name__== "__main__":
    main()