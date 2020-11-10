import json
from datetime import datetime
from random import randint

import django
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return redirect('/news/')


def mainpage(request):

    def simple_date_fun(date):
         return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

    def sort_news(sorted_news):
        date_table = []
        for i in sorted_news:
            i['date'] = simple_date_fun(i['created'])
            if simple_date_fun(i['created']) not in date_table:
                date_table.append(simple_date_fun(i['created']))
        return date_table


    q = request.GET.get('q')
    if q == None:
        q = ''

    with open(settings.NEWS_JSON_PATH, 'r') as f:
        data_from_json = json.load(f)
        sorted_news = sorted(data_from_json, key=lambda i: i['created'], reverse=True)

    final_news = []

    for i in sorted_news:
        if q in i['title']:
            final_news.append(i)
    date_table = sort_news(final_news)
    return render(request, 'mainpage.html', {'sorted_news': final_news, 'date_table': date_table})


def news(request, numer):

    with open(settings.NEWS_JSON_PATH, 'r') as f:
        data_from_json = json.load(f)

        for i in data_from_json:

            if i['link']==numer:
                title = i['title']
                created = i['created']
                text = i['text']
                return render(request, 'news.html', {'title': title, 'created': created, 'text': text})

    raise django.http.Http404("Not found")


def create(request):

    title = request.POST.get('title')
    text = request.POST.get('text')
    post_date = datetime.now().replace(microsecond=0)

    with open(settings.NEWS_JSON_PATH, 'r') as f:
        date_from_json = json.load(f)
        links = []
        link = 1

        for i in date_from_json:
            links.append(i['link'])
        while link in links:
            link = randint(1, 10000)

        new_article = {'created': str(post_date), 'text': text, 'title': title, 'link': link}

        if new_article['title'] != None:
            date_from_json.append(new_article,)


    with open(settings.NEWS_JSON_PATH, 'w') as f:
        f.write(json.dumps(date_from_json))

    if title == None:
        return render(request, 'create.html')
    else:
        return redirect('/news/')