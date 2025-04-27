CURRENT_TEAMS = [
    'ANA',
    'BOS',
    'BUF',
    'CAR',
    'CBJ',
    'CGY',
    'CHI',
    'COL',
    'DAL',
    'DET',
    'EDM',
    'FLA',
    'LAK',
    'MIN',
    'MTL',
    'NJD',
    'NSH',
    'NYI',
    'NYR',
    'OTT',
    'PHI',
    'PIT',
    'SEA',
    'SJS',
    'STL',
    'TBL',
    'TOR',
    'UTA',
    'VAN',
    'VGK',
    'WPG',
    'WSH',
]

GAMES_IN_SEASON_PER_TEAM = 82


def teams_for_season(season):
    if season == '20242025':
        return CURRENT_TEAMS
    elif season in ('20232024', '20222023', '20212022'):
        utaind = CURRENT_TEAMS.find('UTA')
        return sorted(CURRENT_TEAMS[:utaind] + CURRENT_TEAMS[utaind+1:] + ['ARI'])
    else:
        raise ValueError('Unknown or unsupported season!')