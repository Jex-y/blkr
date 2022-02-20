import nltk
import pandas as pd
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download languages
nltk.download('punkt')

# Download stopwords
nltk.download('stopwords')


def remove_stopwords(text: str) -> str:
    parsed_text = []
    words = set(stopwords.words('english'))

    for word in word_tokenize(text):
        if word not in words:
            parsed_text.append(word)

    return " ".join(parsed_text)


def get_random_tweets():
    df = pd.DataFrame()

    bearer_token = "AAAAAAAAAAAAAAAAAAAAAK2lZQEAAAAATa2oQQD1HR3lsCjBt0zDQSF%2BRNU%3D6Wlrd5UzD6WA2NaLsQHbRuA76jbySg1cKKgFRWuJBcE3LWZEFz"
    words = pd.read_csv('./4000-most-common-english-words-csv.csv')

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    # num_words is the number of words to search for.
    num_words = 1000
    for i in range(1, num_words):
        print(f'\r{i}/{num_words} done', end="")
        word = words.iloc[i][0]
        num_tweets = 100

        response = requests.get(
            f"https://api.twitter.com/1.1/search/tweets.json?q=%23{word}&lang=en&count={num_tweets}",
            headers=headers)

        if response.status_code == 200:
            response_json_data = response.json()['statuses']

            new_df = pd.DataFrame(
                {
                    'Tweet' : [data['text'] for data in response_json_data],
                    'Topic' : ['none'] * len(response_json_data)
                })

            df = pd.concat([df, new_df])

            df.to_csv('./random-tweets.csv')

            # for data in response_json_data:
            #     tweet = data['text']
            #     df = pd.concat([df, pd.DataFrame({"Tweet": tweet, "Topic": "none"})], ignore_index=True)
            #     # df = df.append({"Tweet": tweet, "Topic": "random"}, ignore_index=True)
            #     df.to_csv('./random-tweets.csv')
        else:
            break

    df.drop_duplicates().to_csv('./random-tweets.csv')


def get_classified_tweets():
    hashtags = {
        'politics': ['politics', 'political', 'trump', 'war', 'government', 'parliament', 'republican', 'conservative',
                     'election', 'MAGA', 'congress', 'liberal', 'biden', 'GOP'],
        'covid': ['covid', 'covid19', 'covid-19']
    }

    hashtag_data = {hashtag: [] for hashtag in hashtags}

    df = pd.DataFrame()

    # Number of api-calls
    num_api_calls = 100

    for i in range(num_api_calls):
        for key in hashtags.keys():
            for hashtag in hashtags[key]:
                # Get recent tweets with given hashtag
                bearer_token = 'AAAAAAAAAAAAAAAAAAAAAK2lZQEAAAAATa2oQQD1HR3lsCjBt0zDQSF%2BRNU%3D6Wlrd5UzD6WA2NaLsQHbRuA76jbySg1cKKgFRWuJBcE3LWZEFz'
                num_tweets = 100

                headers = {
                    "Authorization": f"Bearer {bearer_token}"
                }

                # Response data
                response = requests.get(
                    f"https://api.twitter.com/1.1/search/tweets.json?q=%23{hashtag}&lang=en&count={num_tweets}",
                    headers=headers)

                if response.status_code == 200:
                    response = response.json()

                    # Extract text
                    for data in response['statuses']:
                        hashtag_data[key].append(data['text'])

                    for key in hashtag_data.keys():
                        for text in hashtag_data[key]:
                            df = df.append({"Tweet": text, "Topic": key}, ignore_index=True)

                    df.to_csv('./classified-data.csv')

                else:
                    print(response.status_code)
                    break

    df.drop_duplicates().to_csv('./classified-data.csv')