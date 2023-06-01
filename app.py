import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

import preprocessor,helper


main_df = pd.read_csv('F:/Praxis Project/Data analysis_olympic dataset/athlete_events.csv')
region_noc = pd.read_csv('F:/Praxis Project/Data analysis_olympic dataset/noc_regions.csv')


st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal-Tally','Overall Analysis','Country wise Analysis','Athlete wise Analysis'))

main_df = preprocessor.preprocess(main_df,region_noc)


if user_menu == 'Medal-Tally':
    st.sidebar.header('Medal Tally')
    Year,Country = helper.country_year_list(main_df)

    selected_year = st.sidebar.selectbox('Select Year',Year)
    selected_country = st.sidebar.selectbox('Select Country', Country)

    medal_tally = helper.fetch_medal_tally(main_df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country =='Overall':
        st.title('Overall Tally')
    if selected_year == 'Overall' and selected_country !='Overall':
        st.title(selected_country + "'s" + "Overall Performance")
    if selected_year != 'Overall' and selected_country =='Overall':
        st.title("Medal Tally In " + str(selected_year) + " Olympics")
    if selected_year != 'Overall' and selected_country !='Overall':
        st.title(selected_country + " performance" + " in " + str(selected_year)+ " Olympics")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    Editions = main_df['Year'].unique().shape[0] - 1
    Host_Cities = main_df['City'].unique().shape[0]
    No_of_Events = main_df['Event'].unique().shape[0]
    No_Of_Sports = main_df['Sport'].unique().shape[0]
    No_Of_Athletes = main_df['Name'].unique().shape[0]
    No_Of_Participating_Nations = main_df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(Editions)
    with col2:
        st.header('Host_Cities')
        st.title(Host_Cities)
    with col3:
        st.header('No_of_Events')
        st.title(No_of_Events)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('No_Of_Sports')
        st.title(No_Of_Sports)
    with col2:
        st.header('No_Of_Athletes')
        st.title(No_Of_Athletes)
    with col3:
        st.header('No_Of_Participating_Nations')
        st.title(No_Of_Participating_Nations)


    nations_over_time = helper.participating_nations_over_time(main_df)  ## plotting chart
    fig = px.line(nations_over_time, x='Year', y='count')
    st.title("Participating Nations Over The Years")
    st.plotly_chart(fig)

    events_over_time = helper.number_of_events__over_time(main_df)  ## plotting chart
    fig = px.line(events_over_time, x='Year', y='count')
    st.title("Number Of Events Over The Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.participating_athletes_over_time(main_df)
    fig = px.line(athletes_over_time, x='Year', y='count')
    st.title("Number Of Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(25,25))
    x = main_df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

if user_menu == 'Country wise Analysis':

    st.sidebar.title("Country-wise Analysis")
    country_list = main_df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('select a country',country_list)

    country_df = helper.yearwise_medal_tally(main_df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(main_df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(main_df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = main_df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = main_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(main_df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df, x = 'Weight',y = 'Height', hue='Medal', style='Sex',s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(main_df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



