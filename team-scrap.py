# Fonte: https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
#
# Desenvolvedor: Amor
#
# Agradecimentos: 
# Polez
# Sader
#
# Run in cmd:
#   
#   pip install selenium
#   pip install beautifulsoup4

import re
import json
import sys
import urllib.parse\

from urllib.request import urlopen
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def extractJson(teamName):

    #extract the player nicks in json into a list
    playerList = []
    with open ('data.json','r') as f:
        data = json.load(f)
    
    totalPlayers = len(data[teamName])
    for c in range(totalPlayers):
        playerList.append(data[teamName][c]["battlenet"])
        #substituindo o '#' por '-'
        playerList[c] = playerList[c].replace("#","-")

        #corrigindo problemas se nome tiver 'ç' ou '~'
        #sei que isso so vai funcionar em dois casos....
        playerList[c] = playerList[c].replace("Ã§","ç")
        playerList[c] = playerList[c].replace("Ã£","ã")
        
    return playerList

def getStats(nick):
    #acessa o perfil da pessoa
    url = 'https://playoverwatch.com/pt-br/career/pc/' + urllib.parse.quote_plus(nick)
    #pegando o html
    page = urlopen(url)
    
    #passando para um fomrato legivel
    soup = BeautifulSoup(page, 'html.parser')
    #print (soup)
   
    #informações que eu vou achar
    bestHero = ''
    timeHero = ''
    rank = ''

    #verificando se é perfil publico ou privado
    if soup.find('div', attrs={'class': 'ProgressBar-title'}) is not None:
        #PERFIL PBULICO
        
        while bestHero == '':
            #pegando o melhor heroi do jogador
            heroBox = soup.find('div', attrs={'class': 'ProgressBar-title'})
            bestHero  = heroBox.text.strip()

        while timeHero == '':
            #pegando o tempo de jogo do melhor heroi
            timeBox = soup.find('div', attrs={'class': 'ProgressBar-description'})
            timeHero = timeBox.text.strip() 

        #verificando se a pessoa joga ranked
        if soup.find('div', attrs={'class': 'competitive-rank'})is not None:
            #JOGA RANKED

            while rank == '':
                #pegando o ranking do jogador
                name_box = soup.find('div', attrs={'class': 'competitive-rank'})
                rank = int(name_box.text.strip())

        else: 
            #NAO JOGA RANKED
            rank = "0000"
    else:  
        #PERFIL PRIVADO
        bestHero = 'Perfil Privado'
        timeHero = '00:00:00'
        rank = "0000"
        
    nick = nick.replace("-","#")
    print (rank ,"-", nick  , '-', bestHero, '-', timeHero)

def main():
        
    print()

    teamName = 'tritons'
    playerList = extractJson(teamName)

    print (teamName,len(playerList),"jogadores encontrados" )

    print ('Rank - Nickname#12312 - Melhor Herói - Tempo jogado ')
    for c in range (len(playerList)):
        getStats(playerList[c])

#https://docs.python.org/3/howto/unicode.html

while True:
    main()
    nick = input('Nick: ')
    getStats(nick.replace('#','-'))

