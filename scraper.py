import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.parse

def main():
    query = input("Enter product name to search: ")
    if not query:
        print("Please enter a valid product name.")
        return

if __name__ == "__main__":
    main()