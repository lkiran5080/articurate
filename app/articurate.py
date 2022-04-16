import re
import uuid
from heapq import nlargest
from string import punctuation

import pyttsx3
import spacy
from newspaper import Article
from spacy.lang.en.stop_words import STOP_WORDS


def extract(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def extract_with_metadata(url):
    article = Article(url)
    article.download()
    article.parse()
    
    print('authors: ', article.authors)
    print('date: ', article.publish_date)
    
    data = {
        "title" : article.title,
        "publish_date": str(article.publish_date),
        "authors" : ",".join([str(i) for i in article.authors]),
        "top_image": article.top_image,
        "text": article.text
    }
    return data

def clean_text_for_summary(text):
    # Removing urls
    text = re.sub('http[s]?://\S+', '', text)
    # Removing square brackets and extra spaces
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # Removing special characters and digits but not punctuation
    text = re.sub('.,:;[^a-zA-Z]', ' ', text )
    text = re.sub(r'\s+', ' ', text)

    return text

def clean_text_for_audio(text):
    # Removing urls
    text = re.sub('http[s]?://\S+', '', text)
    # Removing square brackets and extra spaces
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # Removing special characters and digits but not punctuation
    text = re.sub('[^.,:;a-zA-Z]', ' ', text )
    text = re.sub(r'\s+', ' ', text)

    return text

def declutter(text):
    text = text.replace('\n\n', '\n')
    return text

def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    
    return summary
    

def gen_fn():
    new_filename = str(uuid.uuid4().hex) + ".mp3"
    return new_filename

def synthesize(text, path):
    engine = pyttsx3.init()
    # configure engine
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    # synthesize and save
    engine.save_to_file(text, path)
    engine.runAndWait()


def articurate_from_text(text):
    
    # clean data for models
    text_for_summary = clean_text_for_summary(text)
    text_for_audio = clean_text_for_audio(text)
    
    # generate summary
    per = 0.2
    summary = summarize(text_for_summary, per)
    
    # synthesize audio
    new_fn = gen_fn() 
    path = new_fn
    synthesize(text_for_audio, path)
    
    
def articurate_from_url(url):
    
    f = open('log.txt', mode="a+", encoding="utf-8")
    
    # download webpage and extract text
    text = extract(url)
    
    # clean data for models
    text_for_summary = clean_text_for_summary(text)
    text_for_audio = clean_text_for_audio(text)
    
    f.write("Text for summary:\n")
    f.write(text_for_summary)
    
    f.write("Text for audio:\n")
    f.write(text_for_audio)
    
    # generate summary
    per = 0.2
    summary = summarize(text_for_summary, per)
    print("summary: ", summary)
    
    f.write("Summary:\n")
    f.write(summary)
    
    f.close()
    # synthesize audio
    new_fn = gen_fn() 
    path = new_fn
    synthesize(text_for_audio, path)

if __name__ =='__main__':
    
    SAMPLE_URL = "https://medium.com/analytics-vidhya/text-summarization-using-spacy-ca4867c6b744"
    
    articurate_from_url(SAMPLE_URL)
