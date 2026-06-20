from datetime import date, datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.views import generic, View

from accounts.forms import MemberSelfEditForm
from accounts.models import Member
from archives.forms import AuthorForm, ReaderForm
from archives.models import Author, Reader, Story

from .models import ExchangeParticipant, Prompt
from .forms import ExchangeParticipantForm, PromptForm
            

class MemberList(generic.ListView):
    template_name = 'voiture_noire/memberList.html'
    context_object_name = 'Members'

    def get_queryset(self):
        return Member.objects.exclude(is_active=False).order_by('username')


class Profile(View):
    account_form = MemberSelfEditForm
    author_form = AuthorForm
    reader_form = ReaderForm
    exchange_form = ExchangeParticipantForm
    template_name = 'voiture_noire/profile.html'

    def get(self, request, *args, **kwargs):
        user_stories = []
        author_profile = Author.objects.filter(member=request.user).first()
        if author_profile:
            user_stories = Story.objects.filter(author=author_profile)
        if request.user.is_authenticated:
            reader_profile = Reader.objects.get_or_create(member=request.user)[0]

        return render(
            request,
            self.template_name,
            {
                "admin_form": self.account_form(instance=request.user),
                "exchange_form": self.exchange_form(
                    instance=ExchangeParticipant.objects.filter(
                        member=request.user
                    ).first()
                ),
                "author_profile": author_profile,
                "author_form": self.author_form(
                    instance=author_profile
                ),
                "reader_form": self.reader_form(
                    instance=reader_profile
                ),
                "stories": user_stories,
            }
        )
    
    def post(self, request, *args, **kwargs):
        if request.POST["form_type"] == "admin":
            account_form = self.account_form(request.POST, instance=request.user)
            if account_form.is_valid():
                account_form.save()

        if request.POST["form_type"] == "reader":
            reader_form = self.reader_form(request.POST)
        
            if reader_form.is_valid():
                reader = Reader.objects.get(member=request.user)
                instance = reader_form.save(commit=False)
                reader.serif = instance.serif
                reader.font_size = instance.font_size
                reader.save()
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Une erreur est survenue. Veuillez réessayer."
                )

        if request.POST["form_type"] == "author":
            author_instance = Author.objects.get_or_create(member=request.user)[0]
            author_form = self.author_form(request.POST, instance=author_instance)

            if author_form.is_valid():
                author_form.save()
            else:
                #TODO: handle error messages!
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Votre pseudonyme doit être unique. Si vous n'y avez pas touché, alors mystère."
                )

        if request.POST["form_type"] == "exchange":
            exchange_form = self.exchange_form(request.POST)
        
            if exchange_form.is_valid():
                exchange_participant = ExchangeParticipant.objects.get_or_create(
                    member=request.user
                )[0]

                instance = exchange_form.save(commit=False)
                exchange_participant.likes = instance.likes
                exchange_participant.dislikes = instance.dislikes
                exchange_participant.save()
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Veuillez garder chaque champ en-dessous de 3000 caractères."
                )
        return redirect('voiture_noire:profile')
        

class PromptView(View):
    form_class = PromptForm
    initial = {"key": "value"}
    template_name = "voiture_noire/prompts.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        prompt_list = Prompt.objects.order_by('-id')

        return render(request, self.template_name, {
            "form": form,
            "prompt_list": prompt_list
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        criteria = request.POST['sort_value']
        match criteria:
            case "would_create":
                prompt_list = Prompt.objects.annotate(number_of_would_create=Count('would_create')).order_by("number_of_would_create")
            case "would_receive":
                prompt_list = Prompt.objects.annotate(number_of_would_receive=Count('would_receive')).order_by("number_of_would_receive")
            case "pairing_type":
                prompt_list = Prompt.objects.order_by(criteria, "body")
            case "user_likes_create":
                prompt_list = Prompt.objects.annotate(
                    has_creators=Count(
                        'would_create', filter=Q(would_create__id=request.user.id)
                    )).order_by('-has_creators', 'body')
            case "user_likes_receive":
                prompt_list = Prompt.objects.annotate(
                    has_receivers=Count(
                        'would_receive', filter=Q(would_receive__id=request.user.id)
                    )).order_by('-has_receivers', 'body')
            case _:
                prompt_list = Prompt.objects.order_by(criteria)
        return render(request, self.template_name, {
            "form": form,
            "prompt_list": prompt_list
            })

def post_prompt(request):
    new_prompt = PromptForm(request.POST)
    if new_prompt.is_valid():
        saved_prompt = new_prompt.save()
        saved_prompt.would_create.add(request.user)
        saved_prompt.would_receive.add(request.user)
        return redirect('voiture_noire:prompts')
    # Todo: return message for ano

def would_create(request, prompt_id):
    try:
        prompt = Prompt.objects.get(id=prompt_id)
        prompt.would_create.add(request.user)
    except:
        return redirect('500')
    return redirect('voiture_noire:prompts')

def would_not_create(request, prompt_id):
    try:
        prompt = Prompt.objects.get(id=prompt_id)
        prompt.would_create.remove(request.user)
    except:
        return redirect('500')
    return redirect('voiture_noire:prompts')

def would_receive(request, prompt_id):
    try:
        prompt = Prompt.objects.get(id=prompt_id)
        prompt.would_receive.add(request.user)
    except:
        return redirect('500')
    return redirect('voiture_noire:prompts')

def would_not_receive(request, prompt_id):
    try:
        prompt = Prompt.objects.get(id=prompt_id)
        prompt.would_receive.remove(request.user)
    except:
        return redirect('500')
    return redirect('voiture_noire:prompts')

def brand_as_criminal(request, author_id):
    author = Author.objects.filter(member=request.user).first()

    if author and request.user == author.member :
        author.criminal = not author.criminal
        author.save()

    return redirect('voiture_noire:profile')
