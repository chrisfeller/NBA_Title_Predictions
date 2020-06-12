# Project: NBA Title Predictions
# Description: Build model to predict probability of finals apperance and championship
# Data Sources: Basketball-Reference
# Last Updated: 6/5/20

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import imgkit


if __name__=='__main__':
    # Read in miscellaneous stats table containing four factors and ORTG/DRTG
    misc_df = pd.read_csv('../data/miscellaneous_stats.csv')\
                .query("SEASON != '2019-2020'")
    # Read in table of nba champions
    nba_champs_df = pd.read_csv('../data/nBA_champions.csv')
    # Join two tables and create `CHAMPION` and `RUNNER_UP` flags
    base_df = misc_df.merge(nba_champs_df, on='SEASON', how='left')\
                     .assign(FINALS_FLAG = lambda x: np.where((x['TEAM'] == x['CHAMPION']) |
                                                              (x['TEAM'] == x['RUNNER_UP']), 1, 0))\
                     .assign(CHAMPION_FLAG = lambda x: np.where(x['TEAM'] == x['CHAMPION'], 1, 0))\
                     .replace({'Charlotte Bobcats': 'Charlotte Hornets',
                               'New Orleans/Oklahoma City Hornets': 'New Orleans Pelicans',
                               'New Orleans Hornets': 'New Orleans Pelicans',
                               'Seattle SuperSonics': 'Oklahoma City Thunder',
                               'New Jersey Nets': 'Brooklyn Nets'})\
                     [['SEASON', 'TEAM', 'FINALS_FLAG', 'CHAMPION_FLAG', 'ORTG',
                     'DRTG', 'OFFENSIVE_EFG%', 'OFFENSIVE_TOV%',
                     'OFFENSIVE_ORB%', 'OFFENSIVE_FT/FGA', 'DEFENSIVE_eFG%',
                     'DEFENSIVE_TOV%', 'DEFENSIVE_DRB%', 'DEFENSIVE_FT/FGA']]
    # Create rank columns for all stats
    rank_dict = {'ORTG': False,
                'DRTG': True,
                'OFFENSIVE_EFG%': False,
                'OFFENSIVE_TOV%': True,
                'OFFENSIVE_ORB%': False,
                'OFFENSIVE_FT/FGA': False,
                'DEFENSIVE_eFG%': True,
                'DEFENSIVE_TOV%': False,
                'DEFENSIVE_DRB%': False,
                'DEFENSIVE_FT/FGA': True}
    for k, v in rank_dict.items():
        base_df['{0}_RANK'.format(k)] = base_df.groupby(['SEASON'])[k].rank(ascending=v)

    # Model: Logistic Regression w/ Rank Predictors
    y = base_df['CHAMPION_FLAG']
    X = base_df[['ORTG_RANK', 'DRTG_RANK', 'OFFENSIVE_EFG%_RANK',
                'OFFENSIVE_TOV%_RANK', 'OFFENSIVE_ORB%_RANK',
                'OFFENSIVE_FT/FGA_RANK', 'DEFENSIVE_eFG%_RANK',
                'DEFENSIVE_TOV%_RANK', 'DEFENSIVE_DRB%_RANK',
                'DEFENSIVE_FT/FGA_RANK']]

    lr = LogisticRegression()
    lr.fit(X, y)
    # Assign predicted probabilities for historical championships
    base_df['CHAMPIONSHIPS_PREDICTED'] = lr.predict_proba(X)[:, 1]
    # Write out historical predictions
    base_df.to_csv('../data/historical_predictions.csv', index=False)

    # Make predictions for 2020 Season
    # Read in statistics from 2019-2020
    current_season_df = pd.read_csv('../data/miscellaneous_stats.csv')\
                          .query("SEASON == '2019-2020'")
    # Create Rank columns for all stats
    for k, v in rank_dict.items():
      current_season_df['{0}_RANK'.format(k)] = current_season_df.groupby(['SEASON'])[k].rank(ascending=v)
    X2 =  current_season_df[['ORTG_RANK', 'DRTG_RANK', 'OFFENSIVE_EFG%_RANK',
                                      'OFFENSIVE_TOV%_RANK', 'OFFENSIVE_ORB%_RANK',
                                      'OFFENSIVE_FT/FGA_RANK', 'DEFENSIVE_eFG%_RANK',
                                      'DEFENSIVE_TOV%_RANK', 'DEFENSIVE_DRB%_RANK',
                                      'DEFENSIVE_FT/FGA_RANK']]
    # Assign predicted probabilities for 2019-2020 NBA champions
    current_season_df['CHAMPIONSHIP_PROBABILITY'] = lr.predict_proba(X2)[:, 1]
    # Write out 2019-2020 predictions
    current_season_df.to_csv('../data/2020_predictions.csv', index=False)

    # Extract coefficients from model
    coefs = lr.coef_[0]
    features = list(X.columns)
    importances = [[x, y] for x, y in zip(features, coefs)]
    importances.sort(key=lambda row: abs(row[1]), reverse=True)
    feature_importances = pd.DataFrame(importances)
    feature_importances.columns = ['Feature', 'Coefficient']
    feature_importances = feature_importances.sort_values('Coefficient')\
                                             .assign(Odds = np.exp(-feature_importances['Coefficient']))\
                                             .assign(Probability = lambda x: x['Odds'] / (1 + x['Odds']))\
                                             .assign(Odds = lambda x : 1/x['Odds'])\
                                             .round(3)
    # Style and write out coefficients table
    table_4_styled = (feature_importances
                    [['Feature', 'Coefficient', 'Probability']]
                     .style
                     .set_table_styles(
                     [{'selector': 'tr:nth-of-type(odd)',
                       'props': [('background', '#eee')]},
                      {'selector': 'tbody td', 'props': [('font-family', 'futura')]},
                      {'selector': 'thead', 'props': [('font-family', 'futura')]},
                      {'selector': 'tr:nth-of-type(even)',
                       'props': [('background', 'white')]},
                      {'selector':'th, td', 'props':[('text-align', 'center')]},
                      {'selector': 'caption', 'props':[("font-size", "120%"),
                      ('font-family', 'futura')]}])
                     .set_properties(subset=['Feature'], **{'text-align': 'left'})
                     .set_caption('Feature Importance')
                     .hide_index()
                     .background_gradient(subset=['Probability'], cmap='Reds'))
    html = table_4_styled.render()
    imgkit.from_string(html, '../plots/table_4.png',
                            options={'width': 1300,
                                    'disable-smart-width': '',
                                    'zoom':3.3})
