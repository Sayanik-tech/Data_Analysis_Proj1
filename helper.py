import numpy as np
def medal_tally(main_df):
    medal_tally = main_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally

def country_year_list(main_df):
    Year = main_df['Year'].unique().tolist()
    Year.sort()
    Year.insert(0, 'Overall')

    Country = np.unique(main_df['region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0, 'Overall')

    return Year,Country

def fetch_medal_tally(main_df,year, country):
    medal_df = main_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')

    return x

def participating_nations_over_time(main_df):
    nations_over_time = main_df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    return nations_over_time
def number_of_events__over_time(main_df):
    events_over_time = main_df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year')
    return events_over_time

def participating_athletes_over_time(main_df):
    athletes_over_time = main_df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('Year')
    return athletes_over_time

def yearwise_medal_tally(main_df,country):
    temp_df = main_df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(main_df,country):  #a particular country is good at which sports
    temp_df = main_df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(main_df, country):  ## Most successful top 10 athletes
    temp_df = main_df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(main_df, left_on='Name', right_on='Name', how='left')[
        ['Name']].drop_duplicates('Name')
    #x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def weight_v_height(main_df,sport):
    athlete_df = main_df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(main_df):
    athlete_df = main_df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final






