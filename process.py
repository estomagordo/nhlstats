import json
import os

from collections import Counter, defaultdict


def process_file(file_name):
    with open(file_name) as f:
        data = json.loads(f.readline())

        if data['homeTeam']['abbrev'] > data['awayTeam']['abbrev']:
            return (False, -1, -1)

        home = 0
        away = 0
        lead_minute = -1
        was_one_nil = False
        home = False

        for play in data['plays']:
            if play['typeDescKey'] != 'goal':
                continue

            period = play['periodDescriptor']['number']

            if period > 3:
                continue

            minute = int(play['timeInPeriod'].split(':')[0])

            details = play['details']

            home = details['homeScore']
            away = details['awayScore']

            if period == 1:
                if home+away == 1:
                    lead_minute = minute
                    home = home == 1
                    was_one_nil = True
                else:
                    was_one_nil = False

        if was_one_nil:
            result = 1 if home == away else 0 if home else 2
            return (True, result, lead_minute)
        return (False, -1, -1)


def main():
    minutes = [[0, 0, 0] for _ in range(20)]

    def walk(root):
        for path, dirs, files in os.walk(root):
            for file in files:
                if file.endswith('.json'):
                    succcess, result, lead_minute = process_file(os.path.join(path, file))

                    if succcess:
                        minutes[lead_minute][result] += 1

            for directory in dirs:
                walk(os.path.join(path, directory))

    walk('seasons/')

    for i, minute in enumerate(minutes):
        print(i, minute)


if __name__ == '__main__':
    main()