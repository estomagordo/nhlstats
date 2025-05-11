from matplotlib import pyplot

NHL_WIN_POINTS = 2
SHL_WIN_POINTS = 3
NHL_DRAW_VALUE = 0.75
SHL_DRAW_VALUE = 0.5


def percentage(x):
    return f'{int(round(x, 2)*100)}%'


def print_minute(minute):
    total = sum(minute)
    return f'Wins: {minute[0]} ({percentage(minute[0]/total)}). Draws: {minute[1]} ({percentage(minute[1]/total)}). Losses: {minute[2]} ({percentage(minute[2]/total)}). '


def print_stats(minutes, save_to_file=False):
    grand_total = sum(sum(minute) for minute in minutes)

    for i, minute in enumerate(minutes):
        print(f'Minute {i+1}: {print_minute(minute)} ({percentage(sum(minute)/grand_total)})')

    wins = sum(minute[0] for minute in minutes)
    draws = sum(minute[1] for minute in minutes)
    losses = sum(minute[2] for minute in minutes)

    print(f'Total: {print_minute([wins, draws, losses])}')

    totals = [sum(minute) for minute in minutes]
    times = [m for m in range(1, 21)]
    win_percentages = [minutes[i][0]/totals[i] for i in range(20)]
    draw_percentages = [minutes[i][1]/totals[i] for i in range(20)]
    loss_percentages = [minutes[i][2]/totals[i] for i in range(20)]
    nhl_weighted_point_percentages = [NHL_WIN_POINTS * (minutes[i][0] + minutes[i][1] * NHL_DRAW_VALUE) /totals[i] for i in range(20)]
    shl_weighted_point_percentages = [SHL_WIN_POINTS * (minutes[i][0] + minutes[i][1] * SHL_DRAW_VALUE) /totals[i] for i in range(20)]

    pyplot.plot(times, win_percentages, label='Likelihood of winning')
    pyplot.plot(times, draw_percentages, label='Likelihood of regulation drawing')
    pyplot.plot(times, loss_percentages, label='Likelihood of losing')
    pyplot.plot(times, nhl_weighted_point_percentages, label='Weighted points NHL')
    pyplot.plot(times, shl_weighted_point_percentages, label='Weighted points SHL')
    pyplot.xticks(times)
    pyplot.legend()
    pyplot.show()