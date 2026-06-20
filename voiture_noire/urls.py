from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from . import views

app_name = 'voiture_noire'

urlpatterns = [
    path(
        '',
        RedirectView.as_view(url=reverse_lazy("archives:index")),
        name="index",
    ),
    path('profile', login_required(views.Profile.as_view()), name='profile'),
    path('everyone', login_required(views.MemberList.as_view()), name='everyone'),
    path('member/<int:member_id>', login_required(views.member_profile), name='member_profile'),
    path('prompts', login_required(views.PromptView.as_view()), name='prompts'),
    path('post_prompt', login_required(views.post_prompt), name='post_prompt'),
    path('would_not_create/<int:prompt_id>', views.would_not_create, name='would_not_create'),
    path('would_create/<int:prompt_id>', views.would_create, name='would_create'),
    path('would_not_receive/<int:prompt_id>', views.would_not_receive, name='would_not_receive'),
    path('would_receive/<int:prompt_id>', views.would_receive, name='would_receive'),
    path('accuse/<int:author_id>', login_required(views.brand_as_criminal), name='brand_as_criminal'),
]