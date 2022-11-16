import sys
sys.path.append('.')
sys.path.append('../')
import scrapper
from bs4 import BeautifulSoup
import pytest



def test_checking_arg():
    N_ARGS = 2
    files_names = {"--input":None,"--output":None}
    list_args = ['scrapper.py', '--input', 'input.json', '--output', 'output.json']

    assert scrapper.checking_arguments(files_names,list_args,N_ARGS) == 0

def test_get_links():
    soup = scrapper.get_html_from_id("6JLgWX9iqgo")
    tmp_json = scrapper.get_js_var_json("ytInitialData",soup)
    links = scrapper.get_links(tmp_json)

    links_test = ["http://youtube.com/epenser1","http://facebook.com/epenser","http://twitter.com/epenser","https://fr.wikipedia.org/wiki/Princip...","https://www.youtube.com/watch?v=f5liq...","https://fr.wikipedia.org/wiki/Tenseur...","https://fr.wikipedia.org/wiki/Tenseur...","https://www.youtube.com/watch?v=MTY1K...","https://fr.wikipedia.org/wiki/M%C3%A9...","https://www.youtube.com/DanyCaligula","https://www.youtube.com/pouhiou","https://www.youtube.com/LeCoupdePhil","https://www.youtube.com/codemutv","https://www.youtube.com/fujixgurusynd...","https://www.youtube.com/dirtybiology","https://www.youtube.com/deadwattsoffi...","https://www.youtube.com/channel/UC9Ha...","https://www.youtube.com/physicswoman"]

    assert links == links_test
    assert isinstance(links,list)

def test_get_likes_None():
    soup = scrapper.get_html_from_id("6JLgWX9iqgo")
    tmp_json = scrapper.get_js_var_json("ytInitialData",soup)
    likes = scrapper.get_likes(tmp_json)

    assert likes == None

def test_get_likes_Number():
    soup = scrapper.get_html_from_id("DzJgTXxgY4Q")
    tmp_json = scrapper.get_js_var_json("ytInitialData",soup)
    likes = scrapper.get_likes(tmp_json)

    assert likes.isnumeric()
    assert isinstance(likes,str)

def test_get_comments_None():
    soup = scrapper.get_html_from_id("6JLgWX9iqgo")
    tmp_json = scrapper.get_js_var_json("ytInitialData",soup)
    comments = scrapper.get_comments(tmp_json)

    assert comments == [None]

def test_get_comments_Some():
    soup = scrapper.get_html_from_id("DzJgTXxgY4Q")
    tmp_json = scrapper.get_js_var_json("ytInitialData",soup)
    comments = scrapper.get_comments(tmp_json)

    assert comments != None
    assert isinstance(comments[0], str)
    assert isinstance(comments, list)

def test_generate_dict_from_id():
    dict_test = {"title": "Better than Alaska? Skiing Austria: The Place Beyond The Spines",
                "author": "Nikolai Schirmer",
                "likes": "4367",
                "description": "With the crew:\nhttps://www.instagram.com/robertaaring/\nhttps://www.instagram.com/samfavret/\nhttps://www.instagram.com/nikolaischirmer/\nhttps://www.instagram.com/joonasmattila/\n\nThe crew whose party we crashed:\nhttps://www.instagram.com/samanthamatten/\nhttps://www.instagram.com/tomritsch/\n\nI go through all the gear (including those plates for climbing) here: https://youtu.be/FxytJ9NPM6A\n\nMusic\nWet Leg: https://open.spotify.com/track/260Ub1Yuj4CobdISTOBvM9?si=419eb238517346b1\nArcade Fire: https://open.spotify.com/track/0U0p8weaMIbIFMJ0CPlvHV?si=5e2a20249c584ad8",
                "links": ["https://www.instagram.com/robertaaring/","https://www.instagram.com/samfavret/","https://www.instagram.com/nikolaischi...","https://www.instagram.com/joonasmattila/","https://www.instagram.com/samanthamat...","https://www.instagram.com/tomritsch/","https://youtu.be/FxytJ9NPM6A","https://open.spotify.com/track/260Ub1...","https://open.spotify.com/track/0U0p8w..."],
                "id": "V5l9Ix7yocY",
                "comments": ["We respect you more for your hesitation. Keep doing what you're doing Nikolai, some of the best skiing content out there"]}

    dict_out = scrapper.generate_dict_from_id("V5l9Ix7yocY")
    #/!\ Information about youtube videos can be subject to changes, even author name
    assert dict_out["author"] == dict_test["author"]
    assert isinstance(dict_out,dict)

def test_js_var_json_easy():
    html = "<script> var testvar = { \"one\":\"two\",\"three\":\"four\" }; </script>"
    soup = BeautifulSoup(html,'html.parser')
    dict_test = {"one":"two","three":"four"}

    dict_out = scrapper.get_js_var_json('testvar',soup)

    assert dict_test == dict_out
    assert isinstance(dict_out,dict)

def test_js_var_json_harder():
    html = "<script nonce=\"U9iOStPaWHp2ZlfBuau7_Q\"> bliblou </script><script></script><script nonce=\"U9iOStPaWHp2ZlfBuau7_Q\"> var testvar = { \"one\":\"two\",\"three\":\"four\" };</script>"
    soup = BeautifulSoup(html,'html.parser')
    dict_test = {"one":"two","three":"four"}

    dict_out = scrapper.get_js_var_json('testvar',soup)

    assert dict_test == dict_out
    assert isinstance(dict_out,dict)

def test_js_var_json_none():
    html = "<script nonce=\"U9iOStPaWHp2ZlfBuau7_Q\"> bliblou </script><script></script><script nonce=\"U9iOStPaWHp2ZlfBuau7_Q\"> var stetvar = { \"one\":\"two\",\"three\":\"four\" };</script>"
    soup = BeautifulSoup(html,'html.parser')

    dict_out = scrapper.get_js_var_json('testvar',soup)

    assert dict_out == None

def test_load_json():
    json_test = {"videos_id": ["V5l9Ix7yocY","6JLgWX9iqgo","DzJgTXxgY4Q","fmsoym8I-3o","JhWZWXvN_yo"]}

    json = scrapper.load_json('input.json')

    assert isinstance(json,dict)
    assert json == json_test

def test_load_json_wrongName():
    with pytest.raises(FileNotFoundError):
        scrapper.load_json('intup.json')