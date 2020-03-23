import re
import json
import sys
import urllib.parse\

from urllib.request import urlopen
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_stats(nick):
    formatted_nick = nick.replace('#','-')
    #acessa o perfil da pessoa
    url = 'https://playoverwatch.com/pt-br/career/pc/'+formatted_nick
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
                rank = str(name_box.text.strip())
                
                rank_1 = rank[:4]
                rank_2 = rank[4:8]
                rank_3 = rank[8:12]

                rank = 0

                if rank_1 != '' and int(rank) < int(rank_1):
                    rank = rank_1
                if rank_2 != '' and int(rank) < int(rank_2) :
                    rank = rank_2
                if rank_3 != '' and int(rank) < int(rank_3):
                    rank = rank_3
        else: 
            #NAO JOGA RANKED
            rank = "xxxx"
    else:  
        #PERFIL PRIVADO
        bestHero = 'Perfil Privado'
        timeHero = '00:00:00'
        rank = "----"
        
    nick = nick.replace("-","#")
    print (rank ,"|", nick)

f = open("file.txt", "r")
nicks = [None] * 10
i = 0
for x in f:
    if len(x) > 4:
        x = x.replace('\n','')
        get_stats(x)
