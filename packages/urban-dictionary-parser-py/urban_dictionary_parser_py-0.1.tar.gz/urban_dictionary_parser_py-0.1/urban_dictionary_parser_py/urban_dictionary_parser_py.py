import urllib.request
import urllib.parse
import json


class UdDefinition():
    def __init__(self, id, word, definition, example, link, author, upvotes, downvotes, posted_on_date):
        self.id = id
        self.word = word
        self.definition = definition
        self.example = example
        self.link = link
        self.author = author
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.posted_on_date = posted_on_date


def get_defs(url):
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    #def_dics = sorted(data["list"], key=lambda def_dic: def_dic["thumbs_up"], reverse=True)

    defs = []

    for d in data["list"]:
        defs.append(UdDefinition(
            d["defid"],
            d["word"],
            d["definition"],
            d["example"],
            d["permalink"],
            d["author"],
            d["thumbs_up"],
            d["thumbs_down"],
            d["written_on"]
        ))

    return defs


def define(word):
    url_encoded_word = urllib.parse.quote(word)
    url = "http://api.urbandictionary.com/v0/define?term={0}".format(url_encoded_word)

    # you can change pages by putting "&page=2" at the end of the url
    #TODO: Add support for pages

    return get_defs(url)


def random():
    url = "http://api.urbandictionary.com/v0/random"

    return get_defs(url)
































