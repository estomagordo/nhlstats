import json
import os
import re
import requests

from argparse import ArgumentParser
from pathlib import Path

from consts import GAMES_IN_SEASON_PER_TEAM, TEAMS


DONE = '.done'
GAMES = 'games'

def play_by_play_url(game_id):
    return f'https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play'


def club_schedule_season(team, season):
    return f'https://api-web.nhle.com/v1/club-schedule-season/{team}/{season}'


def get(url):
    print(f'Making a GET request to {url}')
    request = requests.get(url)
    print(f'Status code is {request.status_code}')

    return request.content


def validate_season_format(season):
    EIGHT_DIGITS = '\d{8}'

    return re.match(EIGHT_DIGITS, season) is not None


def get_play_by_play(id):
    content = get(play_by_play_url(id))

    return json.loads(content)


def games_for_season_team(season, team):
    content = get(club_schedule_season(team, season))

    data = json.loads(content)
    games = []

    for game in data['games']:
        home = game['homeTeam']['abbrev']
        away = game['awayTeam']['abbrev']
        id = game['id']
        game_type = game['gameType']

        if game_type == 2:
            games.append((id, home if home != team else away))

    return games


def file_count(path):
    count = 0

    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            count += 1

    return count


def main():
    ap = ArgumentParser()
    ap.add_argument('-s', '--season')
    ap.add_argument('-t', '--team')

    season = ap.parse_args().season
    team = ap.parse_args().team

    if not validate_season_format(season):
        print('Invalid season format')
        return
    
    if not team in TEAMS:
        print('Unknown team')
        return
    
    if not os.path.isdir('seasons'):
        print('No seasons directory. Creating it now.')
        os.makedirs('seasons')

    if not os.path.isdir(f'seasons/{season}'):
        print(f'No season directory for season {season}. Creating it now.')
        os.makedirs(f'seasons/{season}')

    if os.path.isfile(f'seasons/{season}/{DONE}'):
        print('Season already done. Exiting.')
        return
    
    if not os.path.isfile(f'seasons/{season}/{GAMES}'):
        print(f'No games log for season {season}. Creating.')
        Path.touch(f'seasons/{season}/{GAMES}')

    games_saved = set()

    with open(f'seasons/{season}/{GAMES}') as f:
        for line in f:
            games_saved.add(line.rstrip())
    
    retrieved = []

    if not os.path.isdir(f'seasons/{season}/{team}'):
        print(f'No {season} season directory found for {team}. Creating it now.')
        os.makedirs(f'seasons/{season}/{team}')

    if not os.path.isfile(f'seasons/{season}/{team}/{DONE}'):
        for id, opponent in games_for_season_team(season, team):
            if id in games_saved:
                continue

            play_by_play = get_play_by_play(id)
            retrieved.append((team, opponent, id, play_by_play))

    for a, b, id, play_by_play in retrieved:
        with open(f'seasons/{season}/{a}/{id}.json', 'w') as g:
            g.write(json.dumps(play_by_play))

        if not os.path.isdir(f'seasons/{season}/{b}'):
            print(f'No {season} season directory found for {b}. Creating it now.')
            os.makedirs(f'seasons/{season}/{b}')

        with open(f'seasons/{season}/{b}/{id}.json', 'w') as g:
            g.write(json.dumps(play_by_play))

        if file_count(f'seasons/{season}/{b}/') == GAMES_IN_SEASON_PER_TEAM:
            Path.touch(f'seasons/{season}/{b}/{DONE}')

        games_saved.add(id)

    if file_count(f'seasons/{season}/{team}/') == GAMES_IN_SEASON_PER_TEAM:
        Path.touch(f'seasons/{season}/{team}/{DONE}')

    if all(os.path.isfile(f'seasons/{season}/{team_name}/{DONE}') for team_name in TEAMS):
        Path.touch(f'seasons/{season}/{DONE}')

    with open(f'seasons/{season}/{GAMES}', 'w') as g:
        g.write('\n'.join(str(id) for id in games_saved))


if __name__ == '__main__':
    main()