import json
import os


def process_file(file_name):
    with open(file_name) as f:
        data = json.loads(f.readline())

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
    

def percentage(x):
    return f'{int(round(x, 2)*100)}%'


def print_minute(minute):
    total = sum(minute)
    return f'Wins: {minute[0]} ({percentage(minute[0]/total)}). Draws: {minute[1]} ({percentage(minute[1]/total)}). Losses: {minute[2]} ({percentage(minute[2]/total)}). '


def print_stats(minutes):
    grand_total = sum(sum(minute) for minute in minutes)

    for i, minute in enumerate(minutes):
        print(f'Minute {i+1}: {print_minute(minute)} ({percentage(sum(minute)/grand_total)})')

    wins = sum(minute[0] for minute in minutes)
    draws = sum(minute[1] for minute in minutes)
    losses = sum(minute[2] for minute in minutes)

    print(f'Total: {print_minute([wins, draws, losses])}')

def main():
    minutes = [[0, 0, 0] for _ in range(20)]
    processed = set()

    for path, _, files in os.walk('seasons/'):
        for file in files:
            if file.endswith('.json'):
                if file in processed:
                    continue

                processed.add(file)
                succcess, result, lead_minute = process_file(os.path.join(path, file))

                if succcess:
                    minutes[lead_minute][result] += 1

    print_stats(minutes)


if __name__ == '__main__':
    main()