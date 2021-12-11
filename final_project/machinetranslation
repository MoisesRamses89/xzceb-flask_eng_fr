import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from dotenv import load_dotenv

load_dotenv()

apikey = os.environ['apikey']
url = os.environ['url']

authenticator = IAMAuthenticator(apikey)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

def english_to_french(text1):
    """
    This function translates english to french
    """
    frenchtranslation = language_translator.translate(
                                text=text1,
                                model_id='en-fr'
                            ).get_result()

    return frenchtranslation.get("translations")[0].get("translation")

def french_to_english(text1):
    """
    This function translates french to english
    """
    englishtranslation = language_translator.translate(
                                text=text1, 
                                model_id='fr-en'
                            ).get_result()

    return englishtranslation.get("translations")[0].get("translation")
