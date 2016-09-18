#!/usr/bin/env python3.0
# encoding: utf-8

from bs4 import BeautifulSoup as BSoup
import urllib.request
import urllib.error
import re
import pickle
import logging
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

_opener = urllib.request.build_opener()
_opener.addheaders = [('User-agent', 'Mozilla/5.0')]
_events_calendar = {}
_events_list_file = 'events.data'
_url = 'https://en.wikipedia.org/wiki/'
logging.basicConfig(
    filename='log_histopy.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    with open(_events_list_file,'rb') as f:
        _events_calendar = pickle.load(f)
except IOError as e:
    logging.debug(
        'Cache file does not exist. Creating new file as: '+_events_list_file
    )
    pickle.dump(_events_calendar, open(_events_list_file, 'wb'))
    print ("FAILED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def _remove_html_tags(html):
    p = re.compile(r'<[^<]*?/?>')
    return p.sub('', html)

def _get_wikipedia_link(html):
    p = re.compile(r'/wiki/[^"]*')
    findall = p.findall(html)
    falen = len(findall)
    if (falen >= 2):
        falen = 1
    elif (falen == 1):
        falen = 0
    else:
        return ''
    
    return findall[falen]

def load_history(someday, caching=True):
    formatted_date = someday.strftime("%B_%d")
    if (caching):
        try:
            with open(_events_list_file,'rb') as f:
                _events_calendar = pickle.load(f)
        except IOError as e:
            logging.Error('File I/O Error occured: '+e)

        if formatted_date in _events_calendar:
            logging.debug(formatted_date + ' exists in calendar')
            html = _events_calendar[formatted_date]
        else:
            html = _opener.open(_url+formatted_date).read()
            _events_calendar[formatted_date] = html
            pickle.dump(_events_calendar, open(_events_list_file, 'wb'))
    else:
        html = _opener.open(url+formatted_date).read()
    text = BSoup(html,"html.parser").html.body.findAll('ul')
    return text


def _load_ul(li, text):
    item_list = []
    for li in text[li]:
        s = _remove_html_tags(str(li))
        link = _get_wikipedia_link(str(li))
        #print("s -----------------------------------------------")
        #print(s[0])
        #print(s)
        try:
            if (s[0] and link != '' ):
                line = s.split(' – ')
                #print("line, year, event") 
                #print(line)
                event = []
                year = line[0]
                event.append(year) # year
                event.append(str(line[1])) # event
                event.append(str(link)) # link
                #print(year)
                #print(event)
                item_list.append(event)
        except:
            pass
    return item_list


def load_events(loaded_history):
    return _load_ul(1, loaded_history)


def load_births(loaded_history):
    return _load_ul(2, loaded_history)


def load_deaths(loaded_history):
    return _load_ul(3, loaded_history)
