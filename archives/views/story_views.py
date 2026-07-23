import datetime

from django.contrib import messages
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from archives.forms import Author, ChapterForm, StoryForm, StoryFilterForm
from archives.models import Chapter, Story, PairingType, Reaction, ReactionsRelationships

from utils import stories_handler


class Index(generic.ListView):
    template_name = 'archives/index.html'
    context_object_name = 'stories'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.kwargs.get('author_id'):
            context["random_rec"] = stories_handler.return_a_rec(
                self.request.user
            )
            context["filter_form"] = StoryFilterForm

        return context

    def get_queryset(self):
        if self.kwargs.get('author_id'):
            return stories_handler.get_all_visible_stories_of_author(
                self.request.user,
                self.kwargs['author_id']
            )

        pairing_types = self.request.GET.getlist('filter_pairing_types')
        ratings = self.request.GET.getlist('filter_ratings')
        authors = self.request.GET.getlist('filter_authors')
        request_filters = {
            "pairing_types": pairing_types,
            "ratings": ratings,
            "authors": authors
        }
        return stories_handler.get_all_visible_stories(
            self.request.user,
            request_filters
        )


class StoryReadView(generic.View):
    template_name = 'archives/story_get.html'

    def get(self, request, story_id, chapter_number, *args, **kwargs):
        request_user = self.request.user

        story = get_object_or_404(Story, pk=story_id)
        chapter = get_object_or_404(Chapter, story=story, number=chapter_number)
        reactions = Reaction.objects.all()
        reaction_relationships = ReactionsRelationships.objects.filter(
            member=self.request.user).filter(
            chapter=chapter
        )
        picked_reactions_ids = [x.reaction.id for x in reaction_relationships]

        if request.user.is_authenticated is False and story.visibility != 'Everyone':
            return redirect('voiture_noire:index')
        elif request_user.id != story.author.member.id and story.visibility == 'Private':
            return redirect('voiture_noire:index')
        else:
            return render(
                request,
                self.template_name,
                {
                    "story": story,
                    "chapter": chapter,
                    "reactions": reactions,
                    "picked_reactions_ids": picked_reactions_ids
                }
            )


class StoryPublishView(generic.View):
    template_name = 'archives/publish.html'
    chapter_form = ChapterForm
    story_form = StoryForm

    def get(self, request, *args, **kwargs):
        story_form = self.story_form(
            initial={"story_date": datetime.date.today()}
        )
        chapter_form = self.chapter_form(
            initial={"publishing_date": datetime.date.today()}

        )
        return render(
            request,
            self.template_name,
            {
                "chapter_form": chapter_form,
                "story_form": story_form,
            }
        )
    
    def post(self, request, *args, **kwargs):
        story_form = StoryForm(request.POST)
        chapter_form = ChapterForm(request.POST)

        # story_form.errors

        if story_form.is_valid() & chapter_form.is_valid():
            story_author = Author.objects.get_or_create(
                member=request.user,
                defaults={"nickname": request.user.username}
            )[0]
            story_instance = story_form.save(commit=False)
            story_instance.clap = 0
            story_instance.author = story_author
            story_instance.save()
            new_story = Story.objects.filter(author=story_author).latest("id")
            pairing_types = story_form.cleaned_data["pairing_type"]
            pairing_types = PairingType.objects.filter(id__in=pairing_types)
            new_story.pairing_type.set(pairing_types)
            new_story.save()
            chapter_form = chapter_form.save(commit=False)
            chapter_form.story = new_story
            chapter_form.number = 1
            chapter_form.save()
            return redirect(
                'archives:read_story',
                story_id=new_story.id,
                chapter_number=1
            )

        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Problème dans les champs que vous avez rempli."
            )
            return render(
                request,
                self.template_name,
                {
                    "chapter_form": chapter_form,
                    "story_form": story_form,
                }
            )



##### EDITING        
class StoryEditView(generic.View):
    template_name = 'archives/story_edit.html'
    story_form = StoryForm

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        chapters = Chapter.objects.filter(story=story)

        if request.user != story.author.member:
            redirect('voiture_noire:index')
    

        story_form = self.story_form(
            instance=story,
        )

        return render(
            request,
            self.template_name,
            {
                "story_form": story_form,
                "chapters": chapters,
                "story_id": story.id
            }
        )

    def post(self, request, story_id, *args, **kwargs):
        story_initial_instance = Story.objects.get(id=story_id)
        # NOTE : passer aussi les chapitres existants en arg
        if request.user != story_initial_instance.author.member:
            redirect('voiture_noire:index')

        story_form = StoryForm(request.POST)

        if story_form.is_valid():
            story_instance = story_form.save(commit=False)
            story_initial_instance.story_title = story_instance.story_title
            story_initial_instance.visibility = story_instance.visibility
            story_initial_instance.story_date = story_instance.story_date
            story_initial_instance.summary = story_instance.summary
            story_initial_instance.story_author_note = story_instance.story_author_note
            story_initial_instance.pairing_archetype = story_instance.pairing_archetype
            story_initial_instance.one_sentence_summary = story_instance.one_sentence_summary
            story_initial_instance.rating = story_instance.rating
            story_initial_instance.text_length = story_instance.text_length
            story_initial_instance.complete = story_instance.complete

            pairing_types = story_form.cleaned_data["pairing_type"]
            pairing_types = PairingType.objects.filter(id__in=pairing_types)
            story_initial_instance.pairing_type.set(pairing_types)
            story_initial_instance.save()
            return redirect(
                'archives:read_story',
                story_id=story_id,
                chapter_number=1
            )

        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Une erreur est survenue durant l'édition de votre récit. Désolée !"
            )
            chapters = Chapter.objects.filter(story=story)

            return render(
                request,
                self.template_name,
                {
                    "story_form": story_form,
                    "chapters": chapters,
                    "story_id": story.id
                }
            )


def story_delete(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    if request.user == story.author.member:
        story.delete()
        return redirect('voiture_noire:profile')
    else:
        raise HttpResponseNotAllowed("Vous n'êtes pas l'auteur de cette histoire !")
    
def clap_story(request, story_id):
    try:
        story = Story.objects.get(id=story_id)
        story.clap = story.clap+1
        story.save()
        return JsonResponse({"code": 200})
    except Exception:
        return JsonResponse({"code": 500})

