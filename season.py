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

FIRST_PANDEMIC_GAMES = {
    'BOS': 70,
    'TBL': 70,
    'WSH': 69,
    'PHI': 69,
    'PIT': 69,
    'CAR': 68,
    'NYI': 68,
    'TOR': 70,
    'CBJ': 70,
    'FLA': 69,
    'NYR': 70,
    'MTL': 71,
    'BUF': 69,
    'NJD': 69,
    'OTT': 71,
    'DET': 71,
    'STL': 71,
    'COL': 70,
    'VGK': 71,
    'DAL': 69,
    'EDM': 71,
    'NSH': 69,
    'VAN': 69,
    'CGY': 70,
    'WPG': 71,
    'MIN': 69,
    'ARI': 70,
    'CHI': 70,
    'ANA': 71,
    'LAK': 70,
    'SJS': 70
}


class Season:
    def __init__(self, name):
        self.GAMES_IN_SEASON_PER_TEAM = 56 if name == '20202021' else 82
        self.name = name
        self.teams = self.teams_for_season()
    
    def __repr__(self):
        return self.name
    
    def games_for_team(self, team):
        if self.name == '20202021':
            return 56
        if self.name == '20192020':
            return FIRST_PANDEMIC_GAMES[team]
        return 82
        
    def teams_for_season(self):
        if self.name == '20242025':
            return CURRENT_TEAMS
        elif self.name > '20202021':
            utaind = CURRENT_TEAMS.index('UTA')
            return sorted(CURRENT_TEAMS[:utaind] + CURRENT_TEAMS[utaind+1:] + ['ARI'])
        elif self.name > '20162017':
            utaind = CURRENT_TEAMS.index('UTA')
            seaind = CURRENT_TEAMS.index('SEA')
            return sorted([name for i, name in enumerate(CURRENT_TEAMS) if i not in (utaind, seaind)] + ['ARI'])
        else:
            raise ValueError('Unknown or unsupported season!')