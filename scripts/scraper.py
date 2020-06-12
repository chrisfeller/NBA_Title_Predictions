# Project: NBA Title Predictions
# Description: Scrape league standings, season/team statistics, and NBA champions
# Data Sources: Basketball-Reference
# Last Updated: 6/5/20

import numpy as np
import pandas as pd
import requests
from time import sleep
from bs4 import BeautifulSoup as BS

def scrape_nba_champions(save=False):
    """
    Scrape NBA Championship table from Basketball-Reference.com.
    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.
    Returns:
        nba_champs_df (DataFrame): NBA Championship table
    """
    nba_champs_df = pd.read_html("https://www.basketball-reference.com/playoffs/#champions_index::none")[0]
    nba_champs_df.columns = nba_champs_df.columns.get_level_values(1)
    nba_champs_df = nba_champs_df.query("Year.notnull()", engine='python')\
                                 .assign(Lead_Year = nba_champs_df['Year']-1)\
                                 .astype({'Year': int, "Lead_Year": int})\
                                 .assign(SEASON = lambda x: x['Lead_Year'].astype(str) + '-' + x['Year'].astype(str))\
                                 .iloc[:, [-1, 2, 3]]
    nba_champs_df.columns = ['SEASON', 'CHAMPION', 'RUNNER_UP']
    if save:
        parent_directory = '../data/'
        nba_champs_df.to_csv(parent_directory +
                                        'nba_champions.csv',
                                        index=False)
    else:
        pass
    return nba_champs_df

def scrape_miscellaneous_stats(save=False):
    """
    Scrape Miscellaneous Stats table within NBA Season Summary Page on
    Basketball-Reference.com.
    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.
    Returns:
        historical_misc_stats_df (DataFrame): Miscellaneous Stats table between
        2004-2005 and 2018-2019 NBA seasons.
        league_average_misc_stats_df  (DataFrame): League Average Miscellaneous
        Stats between 2004-2005 and 2019-2020 season.
    """
    historical_misc_stats_df = pd.DataFrame()
    for season in np.arange(2005, 2021):
        sleep(np.random.randint(10, 15))
        season_misc_stats_df = pd.DataFrame()
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}.html#misc_stats::none'.format(season)
        html = requests.get(url).text
        soup = BS(html, 'html.parser')
        placeholders = soup.find_all('div', {'class': 'placeholder'})
        for x in placeholders:
            comment = ''.join(x.next_siblings)
            soup_comment = BS(comment, 'html.parser')
            tables = soup_comment.find_all('table', attrs={"id":"misc_stats"})
            for tag in tables:
                df = pd.read_html(tag.prettify())[0]
                season_misc_stats_df = season_misc_stats_df.append(df).reset_index()
                season_misc_stats_df.columns = season_misc_stats_df.columns.get_level_values(1)
                season_misc_stats_df.drop('', axis=1, inplace=True)
                season_misc_stats_df.columns = ['RANK', 'TEAM', 'AVERAGE_AGE',
                                                'W', 'L', 'PW', 'PL', 'MOV',
                                                'SOS', 'SRS', 'ORTG', 'DRTG',
                                                'NRTG', 'PACE', 'FT_RATE',
                                                '3PA_RATE', 'TS%', 'OFFENSIVE_EFG%',
                                                'OFFENSIVE_TOV%', 'OFFENSIVE_ORB%',
                                                'OFFENSIVE_FT/FGA', 'DEFENSIVE_eFG%',
                                                'DEFENSIVE_TOV%', 'DEFENSIVE_DRB%',
                                                'DEFENSIVE_FT/FGA', 'ARENA',
                                                'TOTAL_ATTENDANCE', 'ATTENDANCE/G']
        season_misc_stats_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        season_misc_stats_df['PLAYOFF_TEAM'] = np.where(season_misc_stats_df['TEAM'].str.find('*') > -1, 1, 0)
        season_misc_stats_df['TEAM'] = season_misc_stats_df['TEAM'].str.strip(' * ')
        season_misc_stats_df['W/L%'] = season_misc_stats_df['W']/(season_misc_stats_df['W'] + season_misc_stats_df['L'])
        season_misc_stats_df = season_misc_stats_df[season_misc_stats_df['TEAM']!='League Average']
        historical_misc_stats_df = historical_misc_stats_df.append(season_misc_stats_df,
                                                                    sort=False)
    column_order = ['RANK', 'SEASON', 'TEAM', 'PLAYOFF_TEAM', 'AVERAGE_AGE',
                    'W', 'L', 'W/L%', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORTG',
                    'DRTG', 'NRTG', 'PACE', 'FT_RATE', '3PA_RATE', 'TS%',
                    'OFFENSIVE_EFG%', 'OFFENSIVE_TOV%', 'OFFENSIVE_ORB%',
                    'OFFENSIVE_FT/FGA', 'DEFENSIVE_eFG%', 'DEFENSIVE_TOV%',
                    'DEFENSIVE_DRB%', 'DEFENSIVE_FT/FGA', 'ARENA',
                    'TOTAL_ATTENDANCE', 'ATTENDANCE/G']
    historical_misc_stats_df = historical_misc_stats_df.reindex(columns=column_order)
    if save:
        parent_directory = '../data/'
        historical_misc_stats_df.to_csv(parent_directory +
                                        'miscellaneous_stats.csv',
                                        index=False)
    else:
        pass
    return historical_misc_stats_df

if __name__=='__main__':
    misc_df = scrape_miscellaneous_stats(save=True)
    nba_champs_df = scrape_nba_champions(save=True)
