# Imports the Google Cloud client library
from google.cloud import language_v1
from google.cloud import language
from google.oauth2 import service_account

# Key is saved in this folder and was uploaded to the cloud shell 
creds=service_account.Credentials.from_service_account_file('umc-dsa-8420-fs2021-82e06d434dd0.json')

# Instantiates a client
client = language_v1.LanguageServiceClient(credentials=creds,)

def sentiment_dict(text_list):
    
    text_vector = []
    sentiment_score = []
    sentiment_mag = []
    text_dict = {}
    
    for item in text_list:
        document = language_v1.Document(
            content=item, type_=language_v1.Document.Type.PLAIN_TEXT
            )

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(
            request={"document": document}
            ).document_sentiment

        #print("Text: {}".format(item))
        #print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
        
        text_vector.append(item)
        sentiment_score.append(sentiment.score)
        sentiment_mag.append(sentiment.magnitude)
    
    text_dict['text'] = text_vector
    text_dict['sentiment_score'] = sentiment_score
    text_dict['sentiment_magnitude'] = sentiment_mag
    
    return text_dict