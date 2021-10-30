from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd


# nltk.download()


def audience_sentiment():
    # Sentiment analyzer (VADER)
    sa = SentimentIntensityAnalyzer()
    sa_dict = sa.polarity_scores("I see says the blind man")
    print(sa_dict)

    # All of the audience reviews
    df = pd.read_csv("audience_reviews.csv")
    all_sentiments_comp = []
    all_sentiments_neu = []
    all_sentiments_pos = []
    all_sentiments_neg = []

    # Iterate through all of the reviews and calculate average sentiment
    for index, row in df.iterrows():
        sent_score_comp = []
        sent_score_neu = []
        sent_score_pos = []
        sent_score_neg = []
        reviews = row['Reviews']
        reviews = reviews.split("', ")
        for review in reviews:
            sent_score_comp.append(sa.polarity_scores(review)['compound'])
            sent_score_neu.append(sa.polarity_scores(review)['neu'])
            sent_score_pos.append(sa.polarity_scores(review)['pos'])
            sent_score_neg.append(sa.polarity_scores(review)['neg'])
        all_sentiments_comp.append(sum(sent_score_comp) / len(sent_score_comp))
        all_sentiments_neu.append(sum(sent_score_neu) / len(sent_score_neu))
        all_sentiments_pos.append(sum(sent_score_pos) / len(sent_score_pos))
        all_sentiments_neg.append(sum(sent_score_neg) / len(sent_score_neg))

    print(all_sentiments_comp)
    # Add average sentiment as a new column to the dataframe
    df2 = df.assign(compound_sentiment=all_sentiments_comp,
                    neutral_sentiment=all_sentiments_neu,
                    positive_sentiments=all_sentiments_pos,
                    negative_sentiments=all_sentiments_neg)
    df2.to_csv("audience_reviews_sentiment.csv")


def main():
    audience_sentiment()


if __name__ == "__main__":
    main()
