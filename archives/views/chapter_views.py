import json

from django.contrib import messages
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from archives.forms import ChapterForm
from archives.models import Chapter, Story, Reaction, ReactionsRelationships


class ChapterPostView(generic.View):
    template_name = 'archives/chapter_post.html'
    chapter_form = ChapterForm

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)

        if request.user != story.author.member:
            redirect('voiture_noire:index')
    
        return render(
            request,
            self.template_name,
            {
                "chapter_form": self.chapter_form,
                "story": story
            }
        )

    def post(self, request, story_id, *args, **kwargs):
        root_story = Story.objects.get(id=story_id)
        chapter_nb = root_story.number_of_chapter + 1

        if request.user != root_story.author.member:
            redirect('voiture_noire:index')

        chapter_form = ChapterForm(request.POST)

        # # story_form.errors

        if chapter_form.is_valid():
            chapter_form = chapter_form.save(commit=False)
            chapter_form.story = root_story
            chapter_form.number = chapter_nb
            chapter_form.save()

        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Une erreur est survenue durant l'enregistrement de votre récit."
            )
        return redirect('voiture_noire:index')


class ChapterEditView(generic.View):
    template_name = 'archives/chapter_edit.html'
    chapter_form = ChapterForm

    def get(self, request, story_id, chapter_number, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        chapter = get_object_or_404(Chapter, story=story, number=chapter_number)

        if request.user != story.author.member:
            redirect('voiture_noire:index')
    
        chapter_form = self.chapter_form(instance=chapter)

        return render(
            request,
            self.template_name,
            {
                "chapter_form": chapter_form,
                "story": story
            }
        )

    def post(self, request, story_id, chapter_number, *args, **kwargs):
        root_story = Story.objects.get(id=story_id)

        if request.user != root_story.author.member:
            redirect('voiture_noire:index')

        chapter_form = ChapterForm(request.POST)

        # # story_form.errors
        if chapter_form.is_valid():
            chapter_initial_instance = Chapter.objects.get(story=root_story, number=chapter_number)
            chapter_form = chapter_form.save(commit=False)
            chapter_initial_instance.chapter_title = chapter_form.chapter_title
            chapter_initial_instance.chapter_author_note = chapter_form.chapter_author_note
            chapter_initial_instance.content = chapter_form.content
            chapter_initial_instance.publishing_date = chapter_form.publishing_date
            chapter_initial_instance.save()

        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Une erreur est survenue durant l'enregistrement de votre récit."
            )
        return redirect('voiture_noire:index')

def chapter_delete(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)

    if request.user == chapter.story.author.member:
        chapter.delete()
        return redirect('voiture_noire:profile')
    else:
        raise HttpResponseNotAllowed("Vous n'êtes pas l'autrice de ce récit !")

def react_to_chapter(request, chapter_id):
    try:
        chapter = Chapter.objects.get(id=chapter_id)        
        request_json = json.loads(request.body)
        reaction_id = request_json["reaction_id"]

        if type(reaction_id) is not int:
            raise TypeError

        reaction = Reaction.objects.get(id=reaction_id)
        existing_reaction_for_chapter = ReactionsRelationships.objects.filter(
            member=request.user).filter(
            reaction=reaction).filter(
            chapter=chapter).first()
        if existing_reaction_for_chapter:
            existing_reaction_for_chapter.delete()
        else:
            ReactionsRelationships.objects.create(
                member=request.user,
                reaction=reaction,
                chapter=chapter
            )

        return JsonResponse({"code": 200})
    except TypeError:
        return JsonResponse({"code": 500, "error": "Wrong data type"})
    except Exception:
        return JsonResponse({"code": 500, "error": Exception})
