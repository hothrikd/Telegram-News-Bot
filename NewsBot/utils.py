import os
import dialogflow_v2 as dialogflow
from gnewsclient import gnewsclient

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_news_bot.json"
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-qnnm"
client = gnewsclient.NewsClient()

def detect_intent_from_text(text,session_id,language_code = 'en'):
    session = dialogflow_session_client.session_path(PROJECT_ID,session_id)
    text_input = dialogflow.types.TextInput(text=text,language_code=language_code)
    query_input = dialogflow.types.QueryInput(text = text_input)
    response = dialogflow_session_client.detect_intent(session=session,query_input = query_input)
    return response.query_result


def get_reply(query,chat_id):
    response = detect_intent_from_text(query,chat_id)
    
    if response.intent.display_name=="get_news":
        return "get_news",dict(response.parameters)
    else:
        return "small_talk",response.fulfillment_text
    
def fetch_news(parameters):
    try:
        client.language = str(parameters.get('language').values[0].string_value)
    except:
        client.language="English"
    try:
        client.location = str(parameters.get('geo-country').values[0].string_value)
    except:
        client.location="India"
    try:
        client.topic = str(parameters.get('topic').values[0].string_value)
    except:
        client.language="Top Stories"
    return client.get_news()[:5]
topics_keyboard=[
    ['Top Stories','World','Nation'],
    ['Buisness','Technology','Entertainment'],
    ['Sports','Science','Health']
]