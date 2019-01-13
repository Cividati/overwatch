import json
import requests
import sys

from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)
from dateutil import parser

team_name = sys.argv[1]
day = sys.argv[2]

def get_day_matches(day):
    matches_url = f'https://dtmwra1jsgyb0.cloudfront.net/stages/5b74a81a17592003cbe8a20a/rounds/{day}/matches'
    match_request = requests.get(matches_url)
    match_text = match_request.text
    match_json = json.loads(match_text)
    return match_json

def find_team(match_json, team_name):
    for match in match_json:
        team_name = team_name.lower()

        if 'name' in match['top']:
            team_1_name = match['top']['name'].lower()
        if 'name' in match['bottom']:
            team_2_name = match['bottom']['name'].lower()

        if team_name in team_1_name or team_name in team_2_name:
            return match['_id']
    return None

def get_match_details(match_id):
    matches_url = f'https://dtmwra1jsgyb0.cloudfront.net/matches/{match_id}?extend[top.team][players][user]=true&extend[bottom.team][players][user]=true'
    match_request = requests.get(matches_url)
    match_text = match_request.text
    match_json = json.loads(match_text)
    return match_json

def get_match_players(match_json):
    teams_data = {
        "team_1" : [],
        "team_2" : []
    }

    team_1_players = match_json[0]['top']['team']['players']
    team_2_players = match_json[0]['bottom']['team']['players']

    for player in team_1_players:
        btag = player['inGameName']
        captain = player['beCaptain']

        if 'geoLocation' in player['user']:
            country = player['user']['geoLocation']['country_code']
        else:
            country = "--"
        
        player_data = {
            "battleTag": btag,
            "isCaptain": captain,
            "countryCode": country
        }

        teams_data['team_1'].append(player_data)
    
    for player in team_2_players:
        btag = player['inGameName']
        captain = player['beCaptain']

        if 'geoLocation' in player['user']:
            country = player['user']['geoLocation']['country_code']
        else:
            country = "--"
        
        player_data = {
            "battleTag": btag,
            "isCaptain": captain,
            "countryCode": country
        }

        teams_data['team_2'].append(player_data)

    return teams_data

def get_single_rank(btag):
    formatted_btag = btag.replace("#", "-")
    rank_url = f'http://playoverwatch.com/en-us/career/pc/{formatted_btag}'

    rank_req = requests.get(rank_url)
    rank_txt = rank_req.text
    

    soup = BeautifulSoup(rank_txt, 'html.parser')
    
    private_selector = '.masthead-permission-level-text'
    rank_selector = '.competitive-rank'

    profile_type = soup.select_one(private_selector)
    rank_elem = soup.select_one(rank_selector)

    if rank_elem is None:
        rank = "----"
    else:
        rank = rank_elem.text
    return rank


def get_player_ranks(player_data):
    for player in player_data['team_1']:
        player['rank'] = get_single_rank(player['battleTag'])
    for player in player_data['team_2']:
        player['rank'] = get_single_rank(player['battleTag'])
    return player_data

def print_data(match_data, player_data):
    column_size = 30
    spacing = 5
    total_size = 2 * column_size + spacing
    separator = Back.RED + " " + Back.BLACK + "   " + Back.BLUE + " "

    if 'schedule' in match_data[0]:
        dt = parser.parse(match_data[0]['schedule']['startTime'])
        date_str = f" - {dt.day}/{dt.month}/{dt.year} - {dt.hour}h"
    else:
        date_str = ""

    team_name_1_justified = Back.RED + Fore.WHITE + match_data[0]['top']['name'].rjust(column_size - spacing) + Style.RESET_ALL
    team_name_2_justified = Back.BLUE + Fore.WHITE + match_data[0]['bottom']['name'].ljust(column_size) + Style.RESET_ALL

    print(Fore.BLACK + Back.YELLOW + "Open Division 2018".ljust(total_size - 5))
    print(Fore.BLACK + Back.YELLOW + (f"Partida {match_data[0]['matchNumber']}" + date_str).ljust(total_size - 5))
    print(team_name_1_justified + separator +team_name_2_justified)

    l1 = len(player_data['team_1'])
    l2 = len(player_data['team_2'])
    x = min(l1, l2)

    for i in range(x):
        data_p1 = player_data['team_1'][i]['battleTag'] + " " + Back.RED +player_data['team_1'][i]['rank']
        data_p2 = player_data['team_2'][i]['rank'] + Style.RESET_ALL + " " + player_data['team_2'][i]['battleTag']

        print(data_p1.rjust(column_size) + separator + data_p2.ljust(column_size))

def main():
    day_matches = get_day_matches(day)
    match_id = find_team(day_matches, team_name)
    match_details = get_match_details(match_id)
    players = get_match_players(match_details)
    ranks = get_player_ranks(players)
    print_data(match_details, ranks)

if __name__ == '__main__':
    main()
