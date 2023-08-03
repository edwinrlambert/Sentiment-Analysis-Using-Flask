
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
CACHE_DIR = config("CACHE_DIR", "")

# Model Training for Polarity Scores.
tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL, cache_dir=CACHE_DIR)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(
    SENTIMENT_MODEL, cache_dir=CACHE_DIR)

# Routing for Home Page.
