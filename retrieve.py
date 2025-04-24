import json
import os
import re
import requests

from argparse import ArgumentParser

from consts import TEAMS


def play_by_play_url(game_id):
    return f'https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play'


def club_schedule_season(team, season):
    return f'https://api-web.nhle.com/v1/club-schedule-season/{team}/{season}'


def validate_season_format(season):
    EIGHT_DIGITS = '\d{8}'

    return re.match(EIGHT_DIGITS, season) is not None

def main():
    ap = ArgumentParser()
    ap.add_argument('-s', '--season')

    season = ap.parse_args().season

    if not validate_season_format(season):
        print('Invalid season format')
        return
    
    if not os.path.isdir('seasons'):
        print('No seasons directory. Creating it now.')
        os.makedirs('seasons')

    if not os.path.isdir(f'seasons/{season}'):
        print(f'No season directory for season {season}. Creating it now.')
        os.makedirs(f'seasons/{season}')

    for team in TEAMS:
        if not os.path.isdir(f'seasons/{season}/{team}'):
            print(f'No {season} season directory found for {team}. Creating it now.')
            os.makedirs(f'seasons/{season}/{team}')

        if not os.path.isfile(f'seasons/{season}/{team}/.done'):
            for game in games_for_season_team(season, team):
                # should keep track of game ids already downloaded. Easy peasy.


if __name__ == '__main__':
    main()