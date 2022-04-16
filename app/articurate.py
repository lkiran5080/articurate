import re
import time
import uuid
from heapq import nlargest
from string import punctuation

import pyttsx3
import soundfile as sf
import spacy
from memory_profiler import profile
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

  
def summarize(text):
    summary = ''
    try:
        summarize_main(text=text)
    except:
        PER = 0.1
        summary = summarize_fallback(text=text, per=PER)
    
    return summary

def summarize_main(text):
    
    from transformers import pipeline
    MODEL = "sshleifer/distilbart-cnn-12-6"
    classifier = pipeline("summarization", model=MODEL, framework="pt")
    summary = classifier(text)
    return summary

def summarize_fallback(text, per):
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
  
def synthesize(text, path):
    try:
        synthesize_main(text=text,path=path)
    except:
        synthesize_fallback(text=text,path=path)
    
def synthesize_main(text, path):
    from espnet2.bin.tts_inference import Text2Speech
    model = Text2Speech.from_pretrained("espnet/kan-bayashi_ljspeech_vits")
    speech= model(text)["wav"]
    sf.write("elon2.wav", speech.numpy(), model.fs, "PCM_16")

def synthesize_fallback(text, path):
    engine = pyttsx3.init()
    # configure engine
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    # synthesize and save
    engine.save_to_file(text, path)
    engine.runAndWait()


def gen_fn():
    new_filename = str(uuid.uuid4().hex) + ".mp3"
    return new_filename

if __name__ =='__main__':
    
    SAMPLE_URL = "https://medium.com/analytics-vidhya/text-summarization-using-spacy-ca4867c6b744"
    
    #articurate_from_url(SAMPLE_URL)
    pass
