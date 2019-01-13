import string
import gensim
from bs4 import BeautifulSoup
from Request import Request
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora


class WebScraper:
    """
    Scrapes the input URL and identifies the common topic in that web page.
    """
    def __init__(self, url):
        # The input URL
        self.url = url

        # The HTML response after making the GET request
        self.response = None

        # Stopwords to be removed
        self.stopwords = set(stopwords.words('english') + (list(string.punctuation)))

        # WordNet Lemmatizer
        self.lemma = WordNetLemmatizer()

    def extract(self):
        """
        First fetches the HTML for the input URL. Then it extracts the topic from the HTML.
        :return: The topics in the input URL web page.
        """
        self.response = self.fetch_data()
        if self.response is None:
            return None
        return self.parse_response()

    def fetch_data(self):
        """
        Make a HTTP Get Request to fetch the response
        :return: The response received from the request
        """
        return Request.make_request(self.url)

    def parse_response(self):
        """
        Parses the response and identifies the topics
        :return: A List of topics
        """
        soup = BeautifulSoup(self.response.text, "html5lib")
        keywords = self.extract_keywords(soup)
        return self.get_topics(keywords)

        # References:
        # https://pdfs.semanticscholar.org/2df0/129a57a8b4b99208a9b76e63a67f6d20d912.pdf

    def extract_keywords(self, soup):
        """
        Extracts the text for the important tags from the HTML
        :param soup: A beautiful soup object for the HTML
        :return: A list of keywords containing cleaned tokens
        """
        important_tags = ["title", "h1", "h2", "h3", "h4", "h5", "h6", "meta", "img", "embed"]
        keywords = self.extract_data(important_tags, soup)
        return keywords

    def extract_data(self, tags, soup):
        """
        Extracts the text for the input tags, after tokenizing, we clean the tokens and return a list a tokens
        :param tags: The tags in descending priority for which we need to extract the data
        :param soup: A beautiful soup object for the HTML
        :return: A List containing a list of tokens with their frequency adjusted as per the priority of the tags
        """
        data = []
        priority = len(tags)
        for each_tag in tags:
            for each in soup.find_all(each_tag):
                sentence = each.get_text().strip().lower()
                if sentence != "":
                    tokens = word_tokenize(sentence)
                    tokens = [token for token in tokens if token not in self.stopwords]
                    tokens = [self.lemma.lemmatize(token) for token in tokens]
                    data.append(tokens * priority)
                    priority -= 1
        return data

    def get_topics(self, data):
        """
        Identify the topic based on the input tokens
        :param data: A List of all the cleaned tokens in our filtered document
        :return: A List of topics
        """
        dictionary = corpora.Dictionary(data)
        corpus = [dictionary.doc2bow(text) for text in data]

        NUM_TOPICS = 1
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=50)
        topics = []
        results = ldamodel.show_topics(num_words=4)[0][1].split("+")
        for each in results:
            topic = each.strip().split("*")[1].replace('"', '')
            topics.append(topic)
        return topics
        # References:
        # https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
        # https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21

