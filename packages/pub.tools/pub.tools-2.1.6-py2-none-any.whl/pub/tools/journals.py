import csv
import json
import os
import requests

base_path = os.path.dirname(os.path.realpath(__file__))


# cache journal info on start up
def cache():
    url = 'http://www.ncbi.nlm.nih.gov/pmc/front-page/NIH_PA_journal_list.csv'
    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError:
        return
    except requests.exceptions.ProxyError:
        return
    else:
        if response.status_code == 200:

            _atoj = {}
            _jtoa = {}
            dates = {}
            reader = csv.reader(response.text.split('\n'))

            for row in reader:
                if row:
                    title, abbr, pissn, eissn, start, end = row
                    _atoj[abbr.lower()] = title
                    _jtoa[title.lower()] = abbr
                    dates[abbr.lower()] = (start, end)
            data = {'atoj': _atoj, 'jtoa': _jtoa, 'dates': dates}

            with open(os.path.join(base_path, 'journals.json'), 'w') as f:
                json.dump(data, f)


def get_abbreviations():
    with open(os.path.join(base_path, 'journals.json')) as f:
        return json.load(f)['atoj']


def get_journals():
    with open(os.path.join(base_path, 'journals.json')) as f:
        return json.load(f)['jtoa']


def atoj(abbrv):
    data = get_abbreviations()
    return data.get(abbrv.lower())


def jtoa(journal):
    data = get_journals()
    return data.get(journal.lower())


def atodates(abbrv):
    f = open(os.path.join(base_path, 'journals.json'))
    data = json.load(f)['dates']
    return data.get(abbrv.lower())


cache()
