import streamlit as st

import pandas as pd

import plotly.express as px


from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt

st.title('zach Sentiment Analysis')

dates = ['09_06', '09_07', '09_13']


candidates = ['zach']

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



st.markdown('Let us first look at the evolution of the sentiment of the tweets about zach thruogh the show:')



fig_zach = px.line(df_sentiments, x=df_sentiments.index, y=df_sentiments.columns, markers = True, title = 'Proportion of negative tweets about zach', labels = {'index':'Date', 'value':'Proportion of negative tweets', 'variable':'Candidate'})
st.plotly_chart(fig_zach)

fig_zach_numbers = px.line(df_numbers, x=df_numbers.index, y=df_numbers.columns, markers = True, title = 'Number of tweets about zach', labels = {'value': 'Number of tweets', 'index': 'Date', 'variable': 'Candidate'})
st.plotly_chart(fig_zach_numbers)


st.markdown('### Let us now look at the most frequent words used in the tweets about zach:')

option = st.selectbox(
     'Which type of keywords would you like to look at?',
     ('Positive', 'Negative', 'Neutral'))
# Wordcloud with positive tweets
for date in dates:
    temp_df = pd.read_csv(f'./data/{date}.csv')
    positive_tweets = temp_df['text'][temp_df["sentiment"] == option]
    stop_words = ["https", "co", "RT"] + list(STOPWORDS)
    positive_wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", stopwords = stop_words).generate(str(positive_tweets))

    st.write(f'Wordcloud for {option} tweets on {date}')
    fig, ax = plt.subplots(figsize=(10, 10))
    # ax.title("Positive Tweets - Wordcloud")
    ax.imshow(positive_wordcloud, interpolation="bilinear")
    # ax.axis("off")
    st.pyplot(fig)