from nltk.sentiment import SentimentIntensityAnalyzer
import bs4
import requests
import re
import streamlit as st
import nltk
import pandas as pd
import pickle
import os.path

def web_scraper_critics(movie):
    critic_url = 'http://www.rottentomatoes.com/m/'+movie + '/reviews?type=top_critics'
    #audience_url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews?type=user'
    response = requests.get(critic_url)
    soup = bs4.BeautifulSoup(response.text)
    reviews = soup.find_all('div', {'class': 'the_review'})
    if len(reviews) == 0:
        return []
    cleaned_reviews = [
        re.findall('[^\r\n]+', i.text) if len(re.findall('[^\r\n]+', i.text)) == 0 else re.findall('[^\r\n]+', i.text)[
            0].strip() for i in reviews]
    df = pd.DataFrame({'review': [cleaned_reviews]}, index = [0])
    df.to_csv('cleaned_reviews_critics.csv')
    return

def web_scraper_audience(movie):

    audience_url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews?type=user'
    response = requests.get(audience_url)
    soup = bs4.BeautifulSoup(response.text)
    reviews = soup.find_all('div', {'class': 'audience-reviews__review-wrap'})
    if len(reviews) == 0:
        return []
    cleaned_reviews = [i.find('p', {'data-qa': 'review-text'}).text for i in reviews]
    df = pd.DataFrame({'review': [cleaned_reviews]}, index= [0])
    df.to_csv('cleaned_reviews_audience.csv')
    return


def sentiment_analysis(review_list):
    # Sentiment analyzer (VADER)
    nltk.download('vader_lexicon')
    sa = SentimentIntensityAnalyzer()

    sa_dict = sa.polarity_scores("I see says the blind man")
    print(sa_dict)

    # All of the audience reviews
    #df = pd.read_csv("audience_reviews.csv")

    reviews = review_list.split("', ")
    #reviews = review_list
    # Iterate through all of the reviews and calculate average sentiment
    #for index, row in df.iterrows():
    sent_score_comp = []
    sent_score_neu = []
    sent_score_pos = []
    sent_score_neg = []

    for i in reviews:


        sent_score_comp.append(sa.polarity_scores(i)['compound'])
        sent_score_neu.append(sa.polarity_scores(i)['neu'])
        sent_score_pos.append(sa.polarity_scores(i)['pos'])
        sent_score_neg.append(sa.polarity_scores(i)['neg'])

    compound_score = sum(sent_score_comp) / len(sent_score_comp)
    positive_score = sum(sent_score_pos) / len(sent_score_pos)
    neutral_score = sum(sent_score_neu) / len(sent_score_neu)
    negative_score = sum(sent_score_neg) / len(sent_score_neg)



    # Add average sentiment as a new column to the dataframe
    return [compound_score, positive_score, neutral_score, negative_score]

def main():
    st.title("Rotten Tomatoes Audience Score Prediction")
    movie = st.text_input('Insert movie name here:')
    if st.button('Scrape Critic Reviews'):
        web_scraper_critics(movie)
    if st.button('Scrape Audience Reviews'):
        web_scraper_audience(movie)
    if os.path.exists('cleaned_reviews_audience.csv'):
        audience_reviews = pd.read_csv('cleaned_reviews_audience.csv')['review'].iloc[0]
        if len(audience_reviews) == 0:
            st.success('There are no audience reviews for this movie')
            return
    if os.path.exists('cleaned_reviews_critics.csv'):
        critic_reviews = pd.read_csv('cleaned_reviews_critics.csv')['review'].iloc[0]

        if len(critic_reviews) == 0:
            st.success('There are no critic reviews for this movie')
            return
    #critic_reviews = st.text_input('Paste Critic Reviews Here:')
    # if st.button('Calculate Critic Sentiment Scores'):
    #     critics = sentiment_analysis(critic_reviews)
    #     st.markdown('Compound Score:')
    #     st.markdown(critics[0])
    #     st.markdown('Positive Score')
    #     st.markdown(critics[1])
    #     st.markdown('Neutral Score')
    #     st.markdown(critics[2])
    #     st.markdown('Negative Score')
    #     st.markdown(critics[3])
    #audience_reviews = st.text_input('Paste Audience Reviews Here:')
    # if st.button('Calculate Audience Sentiment Scores'):
    #     audience = sentiment_analysis(audience_reviews)
    #     st.markdown('Compound Score:')
    #     st.markdown(audience[0])
    #     st.markdown('Positive Score')
    #     st.markdown(audience[1])
    #     st.markdown('Neutral Score')
    #     st.markdown(audience[2])
    #     st.markdown('Negative Score')
    #     st.markdown(audience[3])

    model = pickle.load(open('model.pkl', 'rb'))
    if st.button('Predict Audience Score'):
        critics = sentiment_analysis(critic_reviews)
        st.markdown('Compound Score Critics:')
        st.markdown(critics[0])
        st.markdown('Positive Score Critics:')
        st.markdown(critics[1])
        st.markdown('Neutral Score Critics:')
        st.markdown(critics[2])
        st.markdown('Negative Score Critics:')
        st.markdown(critics[3])
        audience = sentiment_analysis(audience_reviews)
        st.markdown('Compound Score Audience:')
        st.markdown(audience[0])
        st.markdown('Positive Score Audience:')
        st.markdown(audience[1])
        st.markdown('Neutral Score Audience:')
        st.markdown(audience[2])
        st.markdown('Negative Score')
        st.markdown(audience[3])

        prediction = model.predict(pd.DataFrame({'compound_audience':audience[0], 'neutral_audience':audience[2], 'positive_audience':audience[1], 'negative_audience':audience[3], 'positive':critics[1], 'negative':critics[3], 'neutral':critics[2], 'compound':critics[0]}, index = [0]))
        st.success(prediction)


if __name__ == "__main__":
    main()
