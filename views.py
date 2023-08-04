
# ? VIEWS.PY

# Importing dependencies.
from flask import Blueprint, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from newspaper import Article
from decouple import config

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
        print(input_type)

        # Find the input text from different types.
        input = ''

        if (input_type == "text"):
            input = response["input"]
        elif (input_type == "url"):
            print("yes")
            link = response["input"]
            print(link)
            article = Article(link)
            article.download()
            article.parse()
            article.nlp()
            input = article.text
        elif (input_type == "media"):
            pass

        # Find the sentiment values.
        sentiment_analysis = find_sentiment_analysis(input)

        return jsonify(sentiment_analysis)


# Chunk the text into pieces of 510 characters.
def chunk_text(text, max_len=510):
    pass

# * Find the polarity scores of the input.


def find_sentiment_analysis(input):
    # Find tokenized words.
    encoded_text = tokenizer(input, return_tensors="pt")

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

    return sentiment_dict
