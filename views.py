
# ? VIEWS.PY

# Importing dependencies.
from flask import Blueprint, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from decouple import config
import numpy as np

from goose3 import Goose

# Creating a blueprint for views to use for routing.
views = Blueprint(__name__, "views")

# Importing pre-trained model for Sentiment Analysis.
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
CACHE_DIR = config("CACHE_DIR", '')

# Model Training for Polarity Scores.
tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL, cache_dir=CACHE_DIR)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(
    SENTIMENT_MODEL, cache_dir=CACHE_DIR)


# * Routing for Home Page.
@views.route('/', methods=["GET", "POST"])
def home():
    # When opening the page, render the webpage.
    if request.method == "GET":
        return render_template("index.html")
    # When a form input is received, show the sentiment based on the input.
    elif request.method == "POST":
        response = request.get_json()
        input_type = response["type"]

        # Find the input text from different types.
        input = ''

        if (input_type == "text"):
            input = response["input"]
        elif (input_type == "url"):
            url = response["input"]
            g = Goose()
            article = g.extract(url=url)
            input = article.cleaned_text

        elif (input_type == "media"):
            pass

        print(input)

        # Find the sentiment values.
        sentiment_analysis = find_sentiment_analysis(input)

        return jsonify(sentiment_analysis)


# Chunk the text into pieces of 510 characters.
def chunk_text(text, max_len=510):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ''

    for sentence in sentences:
        # If the chunk is less than max length.
        if len(current_chunk) + len(sentence) < max_len:
            if current_chunk:
                # Add a space for continuing sentences.
                current_chunk += ' '
            current_chunk += sentence
        # If the chunk is more than max length.
        else:
            chunks.append(current_chunk)
            current_chunk = sentence

        # Adding the last chunk to chunks.
        chunks.append(current_chunk)

        return chunks


# * Find the polarity scores of the input.
def find_sentiment_analysis(input):

    # Split the input into separate chunks.
    chunks = chunk_text(input)
    sentiment_dicts = []

    for chunk in chunks:
        # Find tokenized words.
        encoded_text = tokenizer(chunk, return_tensors="pt")

        # Find polarity scores.
        output = sentiment_model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # Scores
        val_neg = str(scores[0])
        val_neu = str(scores[1])
        val_pos = str(scores[2])

        # Find Prominent Sentiment
        if (val_neg > val_pos) and (val_neg > val_neu):
            prominent_sentiment = "NEGATIVE"
        elif (val_pos > val_neg) and (val_pos > val_neu):
            prominent_sentiment = "POSITIVE"
        else:
            prominent_sentiment = "NEUTRAL"

        # Create Sentiment Analysis Dictionary
        sentiment_dict = {
            'score_negative': val_neg,
            'score_neutral': val_neu,
            'score_positive': val_pos,
            'prominent_sentiment': prominent_sentiment
        }

        sentiment_dicts.append(sentiment_dict)

    # Aggregate the list of chunks to find average sentiment.
    avg_sentiment_dict = {
        'score_negative': str(np.mean([float(d['score_negative']) for d in sentiment_dicts])),
        'score_neutral': str(np.mean([float(d['score_neutral']) for d in sentiment_dicts])),
        'score_positive': str(np.mean([float(d['score_positive']) for d in sentiment_dicts])),
        'prominent_sentiment': max(set([d['prominent_sentiment'] for d in sentiment_dicts]), key=[d['prominent_sentiment'] for d in sentiment_dicts].count)
    }

    return avg_sentiment_dict
