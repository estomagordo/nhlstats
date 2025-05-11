import json
import os

from statter import print_stats


def process_file(file_name):
    with open(file_name) as f:
        outcomes = [
            [-1, -1, -1, False, -1],
            [-1, -1, -1, False, -1]
        ]
        data = json.loads(f.readline())

        home = 0
        away = 0
        last_minute_scored = -1

        for play in data['plays']:
            play_type = play['typeDescKey']
            period = play['periodDescriptor']['number']

            if period > 3:
                break

            if play_type == 'period-start':
                outcomes[period-1][0] = home
                outcomes[period-1][1] = away
            elif play_type == 'period-end':
                started_tie = outcomes[period-1][0] == outcomes[period-1][1]
                tie_broken = (home+away) - sum(outcomes[period-1][:2]) == 1

                if started_tie and tie_broken:
                    outcomes[period-1][2] = last_minute_scored
                    outcomes[period-1][3] = home > away
            elif play_type != 'goal':
                continue

            last_minute_scored = int(play['timeInPeriod'].split(':')[0])

            details = play['details']

            home = details['homeScore']
            away = details['awayScore']
        
        for i in range(len(outcomes)):
            result = 1

            if home != away:
                homewon = home > away
                homeled = outcomes[i][0] > outcomes[i][1]
                result = 2 if homewon^homeled else 0

            outcomes[i][4] = result
        
        return outcomes


def main():
    stats = [
        ['tie broken in 1st period', [[0, 0, 0] for _ in range(20)]],
        ['tie broken in 2nd period', [[0, 0, 0] for _ in range(20)]]
    ]

    processed = set()

    for path, _, files in os.walk('seasons/'):
        for file in files:
            if file.endswith('.json'):
                if file in processed:
                    continue

                processed.add(file)
                outcomes = process_file(os.path.join(path, file))

                for i, outcome in enumerate(outcomes):
                    success, minute, result = outcome
                    if success:
                        stats[i][minute][result] += 1

    for name, minutes in stats:
        print_stats(minutes, name, True)


if __name__ == '__main__':
    main()