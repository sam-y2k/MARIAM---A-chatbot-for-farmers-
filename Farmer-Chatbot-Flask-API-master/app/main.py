# import main Flask class and request object
from flask import Flask, request
import nltk
import numpy as np
import random
import string
import ssl
import bs4 as bs
import urllib.request
import re
import warnings
from googletrans import Translator

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('punkt')
nltk.download('omw-1.4')
nltk.download('wordnet')

#translator=Translator()
#from translate import Translator
warnings.filterwarnings("ignore")

# create the Flask app
app = Flask(__name__)

@app.route('/query-example')
def query_example():
    wiki_page = 'Agriculture'
 
    with open(wiki_page+".txt", 'r',encoding="utf-8") as file:
        article_text = file.read()
    

    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    article_sentences = nltk.sent_tokenize(article_text)
    article_words = nltk.word_tokenize(article_text)

    wnlemmatizer = nltk.stem.WordNetLemmatizer()

    def perform_lemmatization(tokens):
        return [wnlemmatizer.lemmatize(token) for token in tokens]

    punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)

    def get_processed_text(document):
        return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))

    greeting_inputs = ("hey", "good morning", "good evening", "morning","greetings!", "evening", "hi", "whatsup")
    greeting_responses = ["hey", "hey hows you?", "hello, how you doing", "hello", "Welcome, I am good and you"]

    def generate_greeting_response(greeting):
        for token in greeting.split():
            if token.lower() in greeting_inputs:
                return random.choice(greeting_responses)
    def generate_response(user_input):
        mariam_response = ''
        article_sentences.append(user_input)

        word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
        all_word_vectors = word_vectorizer.fit_transform(article_sentences)
        similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
        similar_sentence_number = similar_vector_values.argsort()[0][-2]

        matched_vector = similar_vector_values.flatten()
        matched_vector.sort()
        vector_matched = matched_vector[-2]

        if vector_matched == 0:
            mariam_response = mariam_response + "I am sorry, I could not understand you"
            return mariam_response
        else:
            mariam_response = mariam_response + article_sentences[similar_sentence_number]
            return mariam_response
    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
    all_word_vectors = word_vectorizer.fit_transform(article_sentences) 
    similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    similar_sentence_number = similar_vector_values.argsort()[0][-2]
    translator=Translator()
    def translator_english(input_text):
        generated_translation=translator.translate(input_text,src='en', dest='hi')
        return generated_translation
    def translator_hindi(input_text):
        generated_translation=translator.translate(input_text,src='hi', dest='en')
        return generated_translation
    language = request.args.get('language')
    translation=translator_hindi(language)
    print(translation.text)
    # if key doesn't exist, returns None
    responseText=''
    if language != 'अलविदा' and language!='विदा':
        if language == 'धन्यवाद' or language == 'जी बहुत बहुत शुक्रिया':
            responseText="मरियम: आपकी सेवा में किसी भी समय"
            
            
        else:
            translated_human_text=translator_hindi(language)
            translated_human_text=translated_human_text.text
            # type(generate_greeting_response(translated_human_text))
            greetingToBeTranslated=generate_greeting_response(translated_human_text)
            if greetingToBeTranslated != None:
                
                greetingToBeTranslated=generate_greeting_response(translated_human_text)
                greeting_response_translated=translator_english(greetingToBeTranslated)
                responseText="मरियम: " + greeting_response_translated.text
                
            else:
                translated_human_text = translated_human_text.lower()
                response=generate_response(translated_human_text)
                responseText="मरियम: " + translator_english(response).text
                
                
                #article_sentences.remove(human_text)
    else:
        continue_dialogue = False
        responseText="मरियम: अलविदा और अपना ख्याल रखना..."
    return '''<h1>The language value is: {}</h1>'''.format(responseText)

@app.route('/')
def form_example():
    return 'Form Data Example'

@app.route('/json-example')
def json_example():
    return 'JSON Object Example'

# if __name__ == '__main__':
#     # run app in debug mode on port 5000
#     app.run(debug=True, port=5000)