import pytest
from django.urls import reverse
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('make_bulk_of_news')
def test_news_count(client):
    res = client.get(reverse('news:home'))
    object_list = res.context['object_list']
    comments_count = object_list.count()
    assert comments_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.parametrize(
    'username, is_permitted', ((pytest.lazy_fixture('admin_client'), True),
                               (pytest.lazy_fixture('client'), False))
)
def test_comment_form_availability_for_different_users(
        pk_from_news, username, is_permitted):
    res = username.get(reverse('news:detail', args=pk_from_news))
    assert ('form' in res.context) == is_permitted
    if is_permitted:
        assert isinstance(res.context['form'], CommentForm)


def test_news_order(client):
    res = client.get(reverse('news:home'))
    object_list = res.context['object_list']
    sorted_list_of_news = sorted(object_list,
                                 key=lambda news: news.date,
                                 reverse=True)
    for original_news, sorted_news in zip(object_list, sorted_list_of_news):
        assert original_news.date == sorted_news.date


@pytest.mark.usefixtures('make_bulk_of_comments')
def test_comments_order(client, pk_from_news):
    res = client.get(reverse('news:detail', args=pk_from_news))
    object_list = res.context['news'].comment_set.all()
    sorted_list_of_comments = sorted(object_list,
                                     key=lambda comment: comment.created)
    for original_comment, sorted_comment in zip(object_list,
                                                sorted_list_of_comments):
        assert original_comment.created == sorted_comment.created
