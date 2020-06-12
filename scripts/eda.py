# Project: NBA Title Predictions
# Description: Explore predictions and trends over time
# Data Sources: Basketball-Reference
# Last Updated: 6/8/20

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import imgkit

plt.style.use('fivethirtyeight')


if __name__=='__main__':
    # Read in historical stats and predicted probabilities
    base_df = pd.read_csv('../data/historical_predictions.csv')
    # Read in 2019-2020 stats and predicted probabilities
    current_season_df = pd.read_csv('../data/2020_predictions.csv')

    # Post-process predictions
    # Aggregate predicted probabilities since 2004-2005 season
    title_preds_df = base_df.groupby('TEAM')[['CHAMPIONSHIPS_PREDICTED', 'CHAMPION_FLAG']]\
                            .sum()\
                            .reset_index()\
                            .sort_values('CHAMPIONSHIPS_PREDICTED', ascending=False)\
                            .rename(columns={'CHAMPION_FLAG': 'CHAMPIONSHIPS_WON'})\
                            .assign(CHAMPIONSHIPS_DELTA = lambda x: x['CHAMPIONSHIPS_WON'] - x['CHAMPIONSHIPS_PREDICTED'])
    # Aggregate predicted probabilities since 2009-2019
    title_preds_last10_df = base_df.query("SEASON in {0}".format(['{0}-{1}'.format(i, e) for i, e in zip(range(2009, 2020), range(2010, 2021))]))\
                            .groupby('TEAM')[['CHAMPIONSHIPS_PREDICTED', 'CHAMPION_FLAG']]\
                            .sum()\
                            .reset_index()\
                            .sort_values('CHAMPIONSHIPS_PREDICTED', ascending=False)\
                            .rename(columns={'CHAMPION_FLAG': 'CHAMPIONSHIPS_WON'})\
                            .assign(CHAMPIONSHIPS_DELTA = lambda x: x['CHAMPIONSHIPS_WON'] - x['CHAMPIONSHIPS_PREDICTED'])
    # Create table with season of maximum championship probabilitiy for each team
    max_probs_df = base_df[base_df['CHAMPIONSHIPS_PREDICTED'] == base_df.groupby(['TEAM'])['CHAMPIONSHIPS_PREDICTED']
                                                                        .transform(max)]\
                                                                        .sort_values('TEAM')\
                                                                        [['TEAM',
                                                                        'SEASON',
                                                                        'CHAMPIONSHIPS_PREDICTED']]\
                                                                        .rename(columns={'CHAMPIONSHIPS_PREDICTED': 'MAX_CHAMPIONSHIP_PROBABILITY',
                                                                                        'SEASON': 'MAX_CHAMPIONSHIP_PROBABILITY_SEASON'})\
                                                                        .assign(MAX_CHAMPIONSHIP_PROBABILITY= lambda x: round(100 * x['MAX_CHAMPIONSHIP_PROBABILITY'], 2))


    # Create table of aggregated historical probabilities since 2004-2005
    styled_table_1 = (title_preds_df[['TEAM', 'CHAMPIONSHIPS_PREDICTED',
                                'CHAMPIONSHIPS_WON', 'CHAMPIONSHIPS_DELTA']]
                              .rename(columns={'TEAM': 'Team',
                                       'CHAMPIONSHIPS_PREDICTED': 'Championships Predicted',
                                       'CHAMPIONSHIPS_WON': 'Championships Won',
                                       'CHAMPIONSHIPS_DELTA': 'Championships   Above/Below Expectation'})
                              .round(2)
                              .style
                              .set_table_styles(
                             [{'selector': 'tr:nth-of-type(odd)',
                               'props': [('background', '#eee')]},
                              {'selector': 'tbody td', 'props': [('font-family', 'futura')]},
                              {'selector': 'thead', 'props': [('font-family', 'futura')]},
                              {'selector': 'tr:nth-of-type(even)',
                               'props': [('background', 'white')]},
                              {'selector':'th, td', 'props':[('text-align', 'center')]},
                              {'selector': 'caption', 'props':[("font-size", "130%"),
                              ('font-family', 'futura')]}])
                              .set_properties(subset=['Team'], **{'text-align': 'left'})
                              .set_caption('Since 2004-2005 Season')
                              .hide_index())
    html = styled_table_1.render()
    imgkit.from_string(html, '../plots/table_1.png',
                            options={'width': 2825,
                                    'disable-smart-width': '',
                                    'zoom':3.3})

    # Create table of aggregated historical probabilities since 2009-2010
    styled_table_2 = (title_preds_last10_df[['TEAM', 'CHAMPIONSHIPS_PREDICTED',
                                'CHAMPIONSHIPS_WON', 'CHAMPIONSHIPS_DELTA']]
                              .rename(columns={'TEAM': 'Team',
                                       'CHAMPIONSHIPS_PREDICTED': 'Championships Predicted',
                                       'CHAMPIONSHIPS_WON': 'Championships Won',
                                       'CHAMPIONSHIPS_DELTA': 'Championships   Above/Below Expectation'})
                              .round(2)
                              .style
                              .set_table_styles(
                             [{'selector': 'tr:nth-of-type(odd)',
                               'props': [('background', '#eee')]},
                              {'selector': 'tbody td', 'props': [('font-family', 'futura')]},
                              {'selector': 'thead', 'props': [('font-family', 'futura')]},
                              {'selector': 'tr:nth-of-type(even)',
                               'props': [('background', 'white')]},
                              {'selector':'th, td', 'props':[('text-align', 'center')]},
                              {'selector': 'caption', 'props':[("font-size", "130%"),
                              ('font-family', 'futura')]}])
                              .set_properties(subset=['Team'], **{'text-align': 'left'})
                              .set_caption('Since 2009-2010 Season')
                              .hide_index())
    html = styled_table_2.render()
    imgkit.from_string(html, '../plots/table_2.png',
                            options={'width': 2825,
                                    'disable-smart-width': '',
                                    'zoom':3.3})

    # Create table of maximum historical chamionship probabilities for each team
    styled_table_3 = (max_probs_df.rename(columns={'TEAM': 'Team',
                                       'MAX_CHAMPIONSHIP_PROBABILITY_SEASON': 'Season',
                                       'MAX_CHAMPIONSHIP_PROBABILITY': 'Championship Probability'})
                              .round(2)
                              .style
                              .set_table_styles(
                             [{'selector': 'tr:nth-of-type(odd)',
                               'props': [('background', '#eee')]},
                              {'selector': 'tbody td', 'props': [('font-family', 'futura')]},
                              {'selector': 'thead', 'props': [('font-family', 'futura')]},
                              {'selector': 'tr:nth-of-type(even)',
                               'props': [('background', 'white')]},
                              {'selector':'th, td', 'props':[('text-align', 'center')]},
                              {'selector': 'caption', 'props':[("font-size", "110%"),
                              ('font-family', 'futura')]}])
                              .set_properties(subset=['Team'], **{'text-align': 'left'})
                              .set_caption('Maximum Championship Probability Since 2004-2005')
                              .hide_index())
    html = styled_table_3.render()
    imgkit.from_string(html, '../plots/table_3.png',
                            options={'width': 1595,
                                    'disable-smart-width': '',
                                    'zoom':3.3})

    # Create table with championship probabilities for 2019-2020 season
    styled_table_5 = (current_season_df.sort_values('CHAMPIONSHIP_PROBABILITY', ascending=False)\
                                      .assign(CHAMPIONSHIP_PROBABILITY= lambda x: round(100 * x['CHAMPIONSHIP_PROBABILITY'], 2))\
                                      .rename(columns={'TEAM': 'Team',
                                                        'CHAMPIONSHIP_PROBABILITY': 'Championship Probability'})\
                                      [['Team', 'Championship Probability']]\
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
                                        .set_properties(subset=['Team'], **{'text-align': 'left'})
                                        .set_caption('2019-2020 NBA Championship Probabilities')
                                        .hide_index())
    html = styled_table_5.render()
    imgkit.from_string(html, '../plots/table_5.png',
                          options={'width': 1300,
                                  'disable-smart-width': '',
                                  'zoom':3.3})

    # Create plots for championship probabilities for each team historically
    for team in base_df['TEAM'].unique():
        fig, ax = plt.subplots(figsize=(12,5))
        sns.lineplot(x='SEASON',
                     y='CHAMPIONSHIPS_PREDICTED',
                     data=base_df.assign(CHAMPIONSHIPS_PREDICTED= lambda x: round(100 * x['CHAMPIONSHIPS_PREDICTED'], 2))\
                                 .query("TEAM == '{0}'".format(team)),
                     color='#8b8b8b')
        sns.pointplot(x='SEASON',
                      y='CHAMPIONSHIP',
                      data=base_df.assign(CHAMPIONSHIPS_PREDICTED= lambda x: round(100 * x['CHAMPIONSHIPS_PREDICTED'], 2))\
                      .assign(CHAMPIONSHIP = lambda x: np.where(x['CHAMPION_FLAG']==1, x['CHAMPIONSHIPS_PREDICTED'], None))\
                      .query("TEAM == '{0}'".format(team)),
                      scale=.5,
                      color='#e5ae38',
                      markers='D')
        ax.set_ylabel('Championship Probability', fontsize=12)
        ax.set_xlabel('Season', fontsize=12)
        ax.set_title('{0}'.format(team), fontsize=18)
        plt.xticks(rotation=45, size=8)
        plt.yticks(size=8)
        plt.tight_layout()
        plt.savefig('../plots/teams/{0}'.format(team), dpi=300)

    # Create plot of championship probability for all nba champions historically
    fig, ax = plt.subplots(figsize=(12,5))
    sns.lineplot(x='SEASON',
                 y='CHAMPIONSHIPS_PREDICTED',
                 data=base_df.assign(CHAMPIONSHIPS_PREDICTED= lambda x: round(100 * x['CHAMPIONSHIPS_PREDICTED'], 2))\
                             .query("CHAMPION_FLAG == 1"),
                 color='#8b8b8b')
    ax.set_ylabel('Championship Probability', fontsize=12)
    ax.set_xlabel('Season', fontsize=12)
    ax.set_title('Championship Probability for NBA Champion', fontsize=18)
    plt.xticks(rotation=45, size=8)
    plt.yticks(size=8)
    plt.tight_layout()
    plt.savefig('../plots/champion_probability', dpi=300)

    # Create plots for ORTG/DRTG and Four Factors for all teams historically
    for team in base_df['TEAM'].unique():
        fig = plt.figure(figsize=(15,7.5))
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(223)
        ax3 = plt.subplot(224)
        [sns.lineplot(x='SEASON',
                      y='{0}'.format(k),
                      data=base_df.query("TEAM == '{0}'".format(team)),
                      label='{0}'.format(v),
                      ax=ax1,
                      **{'linewidth': 2.5})
                      for k, v in {'ORTG_RANK': 'ORTG',
                                   'DRTG_RANK': 'DRTG'}.items()]
        [sns.lineplot(x='SEASON',
                      y='{0}'.format(k),
                      data=base_df.query("TEAM == '{0}'".format(team)),
                      label='{0}'.format(v),
                      ax=ax2,
                      **{'linewidth': 2.5})
                      for k, v in {'OFFENSIVE_EFG%_RANK':
                          'eFG%', 'OFFENSIVE_TOV%_RANK':
                          'TOV%', 'OFFENSIVE_ORB%_RANK':
                          'ORB%', 'OFFENSIVE_FT/FGA_RANK':
                          'FT Rate'}.items()]
        [sns.lineplot(x='SEASON',
                      y='{0}'.format(k),
                      data=base_df.query("TEAM == '{0}'".format(team)),
                      label='{0}'.format(v),
                      ax=ax3,
                      **{'linewidth': 2.5})
                      for k, v in {'DEFENSIVE_eFG%_RANK': 'eFG%',
                      'DEFENSIVE_TOV%_RANK': 'TOV%',
                      'DEFENSIVE_DRB%_RANK': 'DRB%',
                      'DEFENSIVE_FT/FGA_RANK': 'FT Rate'}.items()]
        for ax in [ax1, ax2, ax3]:
            ax.set_ylim((31, -1))
            ax.set_yticks([1, 5, 10, 15, 20, 25, 30])
            ax.set_ylabel('League Rank', fontsize=12)
            ax.set_xlabel('', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.xaxis.set_tick_params(labelsize=8)
            ax.yaxis.set_tick_params(labelsize=8)
            ax.legend(prop={'size': 8})
        ax2.set_title('Offensive Four Factors', fontsize=10)
        ax3.set_title('Defensive Four Factors', fontsize=10)
        champ_dict = dict(zip(base_df['SEASON'].unique(), range(-15, 0, 1)))
        champs_list = base_df.query("TEAM == '{0}' & CHAMPION_FLAG == 1".format(team))['SEASON'].values
        for i in champs_list:
            ax1.get_xticklabels()[champ_dict[i]].set_weight("bold")
            ax1.get_xticklabels()[champ_dict[i]].set_fontsize(9)
            ax2.get_xticklabels()[champ_dict[i]].set_weight("bold")
            ax3.get_xticklabels()[champ_dict[i]].set_weight("bold")

        plt.suptitle('{0}'.format('{0}'.format(team)), fontsize=18)
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.savefig('../plots/four_factors/{0}'.format(team), dpi=300)

    # Create plot of ORTG/DRTG and Four Factors for all NBA Champions historically
    fig = plt.figure(figsize=(15,7.5))
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(223)
    ax3 = plt.subplot(224)
    [sns.lineplot(x='SEASON',
                  y='{0}'.format(k),
                  data=base_df.query("CHAMPION_FLAG == 1"),
                  label='{0}'.format(v),
                  ax=ax1,
                  **{'linewidth': 2.5})
                  for k, v in {'ORTG_RANK': 'ORTG',
                               'DRTG_RANK': 'DRTG'}.items()]
    [sns.lineplot(x='SEASON',
                  y='{0}'.format(k),
                  data=base_df.query("CHAMPION_FLAG == 1"),
                  label='{0}'.format(v),
                  ax=ax2,
                  **{'linewidth': 2.5})
                  for k, v in {'OFFENSIVE_EFG%_RANK': 'eFG%',
                               'OFFENSIVE_TOV%_RANK': 'TOV%',
                               'OFFENSIVE_ORB%_RANK': 'ORB%',
                               'OFFENSIVE_FT/FGA_RANK': 'FT Rate'}.items()]
    [sns.lineplot(x='SEASON',
                  y='{0}'.format(k),
                  data=base_df.query("CHAMPION_FLAG == 1"),
                  label='{0}'.format(v),
                  ax=ax3,
                  **{'linewidth': 2.5})
                  for k, v in {'DEFENSIVE_eFG%_RANK': 'eFG%',
                               'DEFENSIVE_TOV%_RANK': 'TOV%',
                               'DEFENSIVE_DRB%_RANK': 'DRB%',
                               'DEFENSIVE_FT/FGA_RANK': 'FT Rate'}.items()]
    for ax in [ax1, ax2, ax3]:
        ax.set_ylim((31, -1))
        ax.set_yticks([1, 5, 10, 15, 20, 25, 30])
        ax.set_ylabel('League Rank', fontsize=12)
        ax.set_xlabel('', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.xaxis.set_tick_params(labelsize=8)
        ax.yaxis.set_tick_params(labelsize=8)
        ax.legend(prop={'size': 8})
    ax2.set_title('Offensive Four Factors', fontsize=10)
    ax3.set_title('Defensive Four Factors', fontsize=10)
    plt.suptitle('League Rank of NBA Champion', fontsize=18)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('../plots/champion_league_rank_overtime', dpi=300)

    # Create correlation of features used in the model
    corr = base_df[['CHAMPION_FLAG','ORTG_RANK', 'DRTG_RANK',
       'OFFENSIVE_EFG%_RANK', 'OFFENSIVE_TOV%_RANK', 'OFFENSIVE_ORB%_RANK',
       'OFFENSIVE_FT/FGA_RANK', 'DEFENSIVE_eFG%_RANK', 'DEFENSIVE_TOV%_RANK',
       'DEFENSIVE_DRB%_RANK', 'DEFENSIVE_FT/FGA_RANK']].corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(10,8))
    cmap = sns.color_palette('coolwarm')
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True, linewidths=.5,
                yticklabels=True, annot=True, fmt='.2f', cbar_kws={'shrink':.5},
                annot_kws={"size": 7})
    plt.title('Correlation Matrix')
    plt.xticks(rotation=90, fontsize=7)
    plt.yticks(rotation=0, fontsize=7)
    plt.tight_layout()
    plt.savefig('../plots/correlation_matrix', dpi=300)

    # Create plot of the average league rank for all NBA Champions historically
    fig, ax = plt.subplots(figsize=(12,5))
    sns.barplot(x='Variable',
                y='Value',
                data = (base_df.query("CHAMPION_FLAG == 1")
                                [['TEAM','ORTG_RANK', 'DRTG_RANK',
                                'OFFENSIVE_EFG%_RANK', 'OFFENSIVE_TOV%_RANK',
                                'OFFENSIVE_ORB%_RANK', 'OFFENSIVE_FT/FGA_RANK',
                                'DEFENSIVE_eFG%_RANK', 'DEFENSIVE_TOV%_RANK',
                                'DEFENSIVE_DRB%_RANK', 'DEFENSIVE_FT/FGA_RANK']]
                                .melt(id_vars='TEAM')
                                .rename(columns=str.title)),
                color='#30a2da')
    ax.set_xticklabels(['ORTG', 'DRTG', 'Offensive eFG%', 'Offensive TOV%',
                        'Offensive Rebound %', 'Offensive FT Rate', 'Defensive eFG%',
                        'Defensive TOV%', 'Defensive Rebound %', 'Defensive FT Rate'])
    ax.set_ylabel('League Rank', fontsize=12)
    ax.set_xlabel('')
    ax.set_title('Average League Rank of NBA Champions\n2005-2019', fontsize=18)
    plt.xticks(rotation=55, fontsize=8)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig('../plots/average_champion_league_rank', dpi=300)

    # Create plot of league rank for all NBA Champions historically
    fig, ax = plt.subplots(figsize=(12,5))
    sns.swarmplot(x='Variable',
                  y='Value',
                  size=8,
                  data = (base_df.query("CHAMPION_FLAG == 1")
                                [['TEAM','ORTG_RANK', 'DRTG_RANK',
                                'OFFENSIVE_EFG%_RANK', 'OFFENSIVE_TOV%_RANK',
                                'OFFENSIVE_ORB%_RANK', 'OFFENSIVE_FT/FGA_RANK',
                                'DEFENSIVE_eFG%_RANK', 'DEFENSIVE_TOV%_RANK',
                                'DEFENSIVE_DRB%_RANK', 'DEFENSIVE_FT/FGA_RANK']]
                                .melt(id_vars='TEAM')
                                .rename(columns=str.title)),
                  color='#30a2da')
    ax.set_xticklabels(['ORTG', 'DRTG', 'Offensive eFG%', 'Offensive TOV%',
                        'Offensive Rebound %', 'Offensive FT Rate', 'Defensive eFG%',
                        'Defensive TOV%', 'Defensive Rebound %', 'Defensive FT Rate'])
    ax.set_ylabel('League Rank', fontsize=12)
    ax.set_xlabel('')
    ax.set_title('League Rank of NBA Champions\n2005-2019', fontsize=18)
    plt.xticks(rotation=55, fontsize=8)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig('../plots/champion_league_rank', dpi=300)
