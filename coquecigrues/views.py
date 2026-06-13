import datetime
import tempfile

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseNotAllowed, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from coquecigrues.models import Roleplayer, World


class Index(generic.ListView):
    template_name = 'coquecigrues/index.html'
    context_object_name = 'worlds'


    def get_queryset(self):
        roleplayer_profile = Roleplayer.objects.get_or_create(member=self.request.user)

        # TODO: handle worlds visibility with filtering
        return World.objects.all()


# class StoryReadView(generic.View):
#     template_name = 'archives/story_read.html'

#     def get(self, request, story_id, chapter_number, *args, **kwargs):
#         request_user = self.request.user

#         story = get_object_or_404(Story, pk=story_id)
#         chapter = get_object_or_404(Chapter, story=story, number=chapter_number)

#         if request.user.is_authenticated is False and story.visibility != 'Everyone':
#             return redirect('voiture_noire:index')
#         elif request_user.id != story.author.member.id and story.visibility == 'Private':
#             return redirect('voiture_noire:index')
#         else:
#             return render(
#                 request,
#                 self.template_name,
#                 {
#                     "story": story,
#                     "chapter": chapter
#                 }
#             )