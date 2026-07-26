from datetime import date

from django.db.models import Q
from archives.models import Author, Story

def return_a_rec(user):
    if user.is_authenticated:
        author_profile = Author.objects.filter(member=user).first() 
        eligible_stories = Story.objects.filter(
            ~Q(author=author_profile) & (~Q(visibility='Private') & Q(story_date__lte=date.today()))
        )
    else:
        eligible_stories = Story.objects.filter(
            (Q(visibility='Everyone') & Q(story_date__lte=date.today()))
        )
    
    return eligible_stories.order_by('?').first()

def get_all_visible_stories(user, request_filters=None):
    stories = []

    if user.is_authenticated:
        stories = Story.objects.filter(
            Q(author__member_id=user.id) | (~Q(visibility='Private') & Q(story_date__lte=date.today()))
        )
    else:
        stories = Story.objects.filter(
            Q(visibility='Everyone') & (Q(story_date__lte=date.today()))
        )

    stories = filter_request(stories, request_filters)
    
    if stories:
        return stories.order_by('-story_date')
    return []

def get_all_visible_stories_of_author(user, author_id):
    return get_all_visible_stories(user, {"authors": [author_id]})

def filter_request(stories, request_filters):
    if request_filters.get('pairing_types'):
        stories = stories.filter(pairing_type__id__in=request_filters['pairing_types'])
    if request_filters.get('ratings'):
        stories = stories.filter(rating__in=request_filters['ratings'])
    if request_filters.get('authors'):
        stories = stories.filter(author__id__in=request_filters['authors'])

    return stories
