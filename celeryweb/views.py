import urllib2
import StringIO
import gzip
import json
from django.core.cache import cache
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import News, Tutorial, CommunityLink


def home(request):
    latest_news = News.objects.filter(visible=1).order_by("-creation_date")[:2]
    context = {'latest_news': latest_news, }
    return render(request, "index.html", context)


def news(request, slug=None):
    if slug:
        news_detail = get_object_or_404(News, slug=slug, visible=1)
        return render(
            request,
            "news_detail.html",
            {"news_detail": news_detail}
        )

    news_list = News.objects.filter(visible=1).order_by("-creation_date")
    paginator = Paginator(news_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        news = paginator.page(page)
    except (EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)
    return render(request, "news.html", {"news": news})


def tutorials(request, slug=None):
    if slug:
        tutorial = get_object_or_404(Tutorial, slug=slug, visible=1)
        return render(
            request,
            "tutorial_detail.html",
            {"tutorial_detail": tutorial}
        )
    tutorial_list = Tutorial.objects.filter(
        visible=1).order_by("-creation_date")
    paginator = Paginator(tutorial_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        tutorials = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tutorials = paginator.page(paginator.num_pages)
    return render(
        request,
        "tutorials.html",
        {"tutorials": tutorials}
    )


def community(request):
    links_list = CommunityLink.objects.filter(
        visible=1).order_by("-creation_date")
    paginator = Paginator(links_list, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        links = paginator.page(page)
    except (EmptyPage, InvalidPage):
        links = paginator.page(paginator.num_pages)

    return render(
        request,
        "external_resources.html",
        {"links": links},
    )


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(
        request,
        'user_profile.html',
        {'user': user}
    )

# AJAX


def stackoverflow_questions(request, page_size=10, page=1):
    opener = urllib2.build_opener()
    request_url = urllib2.Request(
        ("http://api.stackexchange.com/2.2/"
         "search?tagged=celery&order=desc&sort=creation&site=stackoverflow"
         "&page=%s&pagesize=%s") % (page, page_size),
        None,
        headers={'Accept-Encoding': 'gzip, identity'})
    gzipped = opener.open(request_url)
    compressed_stream = StringIO.StringIO(gzipped.read())
    gzipped.close()
    jsondata = json.loads(gzip.GzipFile(
        fileobj=compressed_stream).read().decode('utf-8-sig'))
    return render(
        request,
        'ajax/stackoverflow_questions.html',
        {'jsondata': jsondata},
    )


def package_info(request):
    package_info_context = cache.get('package_info_context', None)
    if not package_info_context:
        opener = urllib2.build_opener()
        request_url = urllib2.Request(
            "http://pypi.python.org/pypi/celery/json", None)
        package_info_context = {}
        try:
            package_info_context['package_info'] = json.load(
                opener.open(request_url))
            package_info_context['changelog_link'] = "http://docs.celeryproject.org/en/latest/changelog.html#version-%s"\
                % package_info_context['package_info']['info']['version'].replace(".", "-")
            cache.set('package_info_context', package_info_context, 60 * 120)
        except (urllib2.HTTPError, ValueError) as e:
            package_info_context['error'] = "Something went wrong when trying to get package information from pypi"

    return render(
        request,
        'ajax/celery_package_info.html',
        package_info_context,
    )

class NewsFeed(Feed):
    title = "News | Celery: Distributed Task Queue"
    link = "/sitenews/"
    description = "News"

    def items(self):
        return News.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('news_entry', args=[item.slug])
