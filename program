#fonte: https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
#
#agradecimentos: Polez
#
#Run in cmd:
#   
#   pip install selenium
#   pip install beautifulsoup4

import re

from urllib.request import urlopen
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_bnet():
    bnet = input ("Digite sua b.net, ex: Example#4213: ")
    bnet = bnet.replace('#', '-', 1)
    return bnet

def get_rankName(rank):
    rank = rank

    if rank < 1499:
        rank_name = 'Bronze'
    elif rank < 2499:
        rank_name = "Ouro"
    elif rank < 2999:
        rank_name = "Platina"
    elif rank < 3499:
        rank_name = "Diamante"
    elif rank < 3999:
        rank_name = "Mestre"
    else: rank_name = "GM"

    return rank_name

nick = get_bnet()
url = 'https://playoverwatch.com/pt-br/career/pc/'+nick

# url do site
quote_page = url
#pegando o html
page = urlopen(quote_page)
#passando para um fomrato leginvel
soup = BeautifulSoup(page, 'html.parser')
#pegando a <div> do nome e pegando o seu valor
name_box = soup.find('div', attrs={'class': 'competitive-rank'})
#pegando o ranking do jogador
rank = int(name_box.text.strip())

rank_name = get_rankName(rank)

#pegando a <div> do nome e pegando o seu valor
name_box = soup.find('h1', attrs={'class': 'header-masthead'})
#pegando o ranking do jogador
name = name_box.text.strip()
print ("Nick: ", name," | Rank: " , rank, " | ", rank_name)

