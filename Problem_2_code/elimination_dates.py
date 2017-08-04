import pandas as pd
import numpy as np
import sys
'''
Program that generates two csv files of elimination dates,
both of which are exactly the same (sans formatting).

Usage:
python elimination_dates.py [filename.xlsx]

note that the filename is optional, if not used, then it
automatically opens Analytics_Attachement.xlsx

The input should be formatted exactly like Analytics_Attachment.xlsx
'''

class Team(object):
    def __init__(self, num):
        '''
        Some useful fields for calculating elimination
        '''
        self.team_id = num
        self.wins=0
        self.possible_wins = 82
        self.conf_wins = 0
        self.poss_conf_wins = 52 #calculated from above data
        self.winning_margin = 0
        self.elim_day = -1
        self.eliminated = False
   
    #functions for winning and losing a game 
    def lose_game(self, frame):
        self.possible_wins -= 1
        if frame['Conference']:
            self.poss_conf_wins -= 1
        #if frame['Division']:
            #self.possible_division_wins -= 1
    
    def win_game(self, frame):
        self.wins += 1
        if frame['Conference']:
            self.conf_wins += 1
    
    def check_elimination(self, eighth_place_team, day):
        '''
        method for checking elimination based on the current
        eighth place team
        '''    
        if (self.possible_wins < eighth_place_team.wins 
            and not self.eliminated):
            self.eliminated = True
            self.elim_day = day
        elif (eighth_place_team.wins == self.possible_wins):
            if (self.poss_conf_wins < eighth_place_team.conf_wins 
                and not self.eliminated):
                self.eliminated = True
                self.elim_day = day
            
    #sorting methods
    def __lt__(self, other):
        if self.wins < other.wins:
            return True
        elif self.wins == other.wins:
            if self.conf_wins < other.conf_wins:
                return True
        return False
    
    def __gt__(self, other):
        return not self.__lt__(other)
    
    def __eq__(self, other):
        return self.team_id == other.team_id
    
    def __neq__(self, other):
        return not self.__eq__(other)

def check_confs_elimination(conf1, conf2, day):
    '''
    check both eliminations
    '''
    check_conf_elimination(conf1, day)
    check_conf_elimination(conf2, day)

def check_conf_elimination(conf, day):
    '''
    check every team in a single conference
    '''
    eighth_place = sorted(conf)[-8]
    for team in conf:
        team.check_elimination(eighth_place, day)

def simulate_season_updates(results):
    '''
    for both conferences, run through every team, and 
    check both conferences for elimination
    '''
    eastern = [Team(i) for i in range(15)]
    western = [Team(i+15) for i in range(15)]

    for i in range(results.shape[0]):
        if results.iloc[i]['Winning_team_id'] < 15:
            winning_team = eastern[results.iloc[i]['Winning_team_id']]
        else:
            winning_team = western[results.iloc[i]['Winning_team_id']-15]
        winning_team.win_game(results.iloc[i])

        if results.iloc[i]['Losing_team_id'] < 15:
            losing_team = eastern[results.iloc[i]['Losing_team_id']]
        else:
            losing_team = western[results.iloc[i]['Losing_team_id']-15]
        losing_team.lose_game(results.iloc[i])

        check_confs_elimination(eastern, western, 
            results.iloc[i]['Day Number'])    
    
    check_confs_elimination(eastern, western, 
        results.iloc[-1]['Day Number'])
    return eastern, western

def read_data(file_name="Analytics_Attachment.xlsx"):
    '''
    Clean the data, in order to help with indexing, and 
    the margins.
    '''
    teams_divisions=pd.read_excel(file_name, sheetname=0)
    teams_divisions['team_id'] = np.array([i for i in range(30)])

    results=pd.read_excel(file_name, sheetname=1)

    # store the start date, store dates by integers representing days after the start_date 
    start_date = results['Date'][0]
    results['Day Number']=((results['Date']-start_date)/np.timedelta64(1, 'D')).astype(int)
    results = results.drop('Date', axis=1)

    # Associate (home and away) teams with their index
    results = results.merge(teams_divisions, left_on='Home Team', right_on='Team_Name', how='left')
    results=results.rename(columns = {'Division_id':'Home_Division_id', 'team_id':'Home_team_id','Conference_id':'Home_Conference_id'})
    del results['Team_Name']
    results = results.merge(teams_divisions, left_on='Away Team', right_on='Team_Name', how='left')
    results=results.rename(columns = {'Division_id':'Away_Division_id', 'team_id':'Away_team_id','Conference_id':'Away_Conference_id'})
    del results['Team_Name']

    # Since home and away is irrelevant in this question, store teams by win/loss/margin of victory
    results.loc[results['Winner'] == 'Home','Winning_team_id'] = results['Home_team_id']
    results.loc[results['Winner'] == 'Home','Losing_team_id'] = results['Away_team_id']
    results.loc[results['Winner'] == 'Home','Margin'] = (results['Home Score'] - results['Away Score']).astype(int)
    results.loc[results['Winner'] == 'Away','Winning_team_id'] = results['Away_team_id']
    results.loc[results['Winner'] == 'Away','Losing_team_id'] = results['Home_team_id']
    results.loc[results['Winner'] == 'Away','Margin'] = (results['Away Score'] - results['Home Score']).astype(int)
    results['Winning_team_id'] = results['Winning_team_id'].astype(int)
    results['Losing_team_id'] = results['Losing_team_id'].astype(int)
    results['Margin'] = results['Margin'].astype(int)

    #drop irrelevant columns
    results=results.drop(['Home_team_id','Away_team_id','Home Team', 'Away Team','Home Score', 'Away Score', 'Winner', 'Home Team', 'Away Team'], axis=1)

    # Associate conference and division games with conference title, if not division (or conference) game, put `None`
    results.loc[results['Away_Conference_id']==results['Home_Conference_id'], 'Conference'] = results['Home_Conference_id']
    results.loc[results['Home_Conference_id']!=results['Away_Conference_id'], 'Conference'] = None
    results.loc[results['Home_Division_id']==results['Away_Division_id'], 'Division'] = results['Home_Division_id']
    results.loc[results['Home_Division_id']!=results['Away_Division_id'], 'Division'] = None

    results=results.drop(['Home_Conference_id','Home_Division_id','Away_Conference_id','Away_Division_id'], axis=1)

    return results, teams_divisions, start_date

def output_elim_dates(teams_divisions, start_date, eastern, western, output_file_names):
    '''
    takes in the conference arrays, and prints the 
    date of elimination or `playoffs` for each team
    '''
    r = [0 for i in range(30)]
    for team in eastern:
        r[team.team_id] = team.elim_day

    for team in western:
        r[team.team_id] = team.elim_day
    elim = pd.DataFrame(r, columns=["elim"])
    elim['team_id'] = np.array([i for i in range(30)])
    elim = elim.merge(teams_divisions, on='team_id', how='left')
    elim2 = elim.copy()
    elim.loc[elim['elim']!=-1, 'Date Eliminated'] = '=\"'+(start_date + pd.to_timedelta(elim['elim'], unit='D')).dt.strftime("%m/%d/%Y").astype(str)+'\"'
    elim.loc[elim['elim']==-1, 'Date Eliminated'] = "Playoffs"
    elim = elim.sort_values(by=['Team_Name']).drop(['elim','team_id','Division_id','Conference_id'], axis=1).rename(columns={'Team_Name':"Team"})
    elim2.loc[elim2['elim']!=-1, 'Date Eliminated'] = (start_date + pd.to_timedelta(elim2['elim'], unit='D')).dt.strftime("%m/%d/%Y").astype(str)
    elim2.loc[elim2['elim']==-1, 'Date Eliminated'] = "Playoffs"
    elim2 = elim2.sort_values(by=['Team_Name']).drop(['elim','team_id','Division_id','Conference_id'], axis=1).rename(columns={'Team_Name':"Team"})
    
    elim.to_csv("./"+output_file_names+"_for_excel.csv", index=False)
    elim2.to_csv("./"+output_file_names+".csv", index=False)

    return elim2

def main():
    if len(sys.argv) == 1:
        results, teams_divisions, start_date = read_data()
        out_file = "playoffs"
    else:
        if len(sys.argv):
            print("please put 2 inputs: input filename, output filename (without \'.csv\')")
            return
        results, teams_divisions, start_date = read_data(sys.argv[1])
        out_file = sys.argv[2]
    eastern, western = simulate_season_updates(results)
    output_elim_dates(teams_divisions, start_date, eastern, western, out_file)

if __name__=="__main__":
    main()
