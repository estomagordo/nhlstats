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


class Season:
    def __init__(self, name):
        self.GAMES_IN_SEASON_PER_TEAM = 56 if name == '20202021' else 82
        self.name = name
        self.teams = self.teams_for_season()
    
    def __repr__(self):
        return self.name
        
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