import streamlit as st

import pandas as pd

import plotly.express as px

st.title('Homepage of the Sentiment Analysis of the Bachelorette 2022')

dates = ['09_06', '09_07']

candidates = ['tino', 'erich', 'aven','rachel', 'gabby', 'johnny', 'jason', 'zach']

df_sentiments = pd.DataFrame(columns=candidates, index=dates)
df_numbers = pd.DataFrame(columns=candidates, index=dates)

for date in dates:
    temp_df = pd.read_csv(f'./data/{date}.csv')
    for candidate in candidates:
        nbr_positive = 0
        nbr_negative = 0
        nbr_neutral = 0
        count = 0
        for i in range(len(temp_df['sentiment'])):
            if temp_df['text'][i].lower().find(candidate) != -1:
                if temp_df['sentiment'][i] == 'Negative':
                    nbr_negative += 1
                elif temp_df['sentiment'][i] == 'Positive':
                    nbr_positive += 1
                else:
                    nbr_neutral += 1
                count += 1
        df_sentiments[candidate][date] = nbr_negative /( nbr_negative + nbr_positive + nbr_neutral)
        df_numbers[candidate][date] = count




rachel_contestants = ['rachel', 'tino', 'aven', 'zach']
rachel_df = df_sentiments[rachel_contestants]
gabby_contestants = ['gabby', 'erich', 'johnny', 'jason']
gabby_df = df_sentiments[gabby_contestants]


st.markdown('Let us first look at the evolution of the sentiment of the tweets about rachel\'s contestants thruogh the show:')
fig_rachel = px.line(rachel_df, x=rachel_df.index, y=rachel_df.columns, markers = True, title = 'Proportion of negative tweets about rachel\'s contestants', labels = {'index':'Date', 'value':'Proportion of negative tweets', 'variable':'Candidate'})
st.plotly_chart(fig_rachel)

st.markdown('Now we look at the evolution of the sentiment of the tweets about gabby\'s contestants thruogh the show:')
fig_gabby = px.line(gabby_df, x=gabby_df.index, y=gabby_df.columns, markers = True, title = 'Proportion of negative tweets about gabby\'s contestants', labels = {'index':'Date', 'value':'Proportion of negative tweets', 'variable':'Candidate'})
st.plotly_chart(fig_gabby)
