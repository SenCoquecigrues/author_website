import asyncio

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic, View

from accounts.forms import MemberSelfEditForm
from accounts.models import Member
from archives.forms import AuthorForm, ReaderForm
from archives.models import Author, Reader, Story
from archives.utils.trackbear import TrackbearConnector

from voiture_noire.models import ExchangeParticipant
from voiture_noire.forms import ExchangeParticipantForm


class MemberList(generic.ListView):
    template_name = 'voiture_noire/member_list.html'
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

def member_profile(request, member_id):
    template_name = 'voiture_noire/member_profile.html'

    if request.user.discord_id == "":
        raise Exception("Must be a discord member")

    member = Member.objects.get(id=member_id)

    return render(request, template_name, {"person": member})

def brand_as_criminal(request, author_id):
    author = Author.objects.filter(member=request.user).first()

    if author and request.user == author.member :
        author.criminal = not author.criminal
        author.save()

    return redirect('voiture_noire:profile')

"""
    Test view to get Trackbear projects for a given user.
"""
def get_public_trackbear_projects(request, user_id: int):
    member = Member.objects.filter(id=user_id).first()

    if not member:
        return JsonResponse(
            {
                "project_list": []
            }
        )

    author_profile = Author.objects.filter(member=member).first()
    if not author_profile:
        return JsonResponse(
            {
                "project_list": []
            }
        )

    project_list = asyncio.run(
        TrackbearConnector.get_author_projects(author_profile)
    )
    return JsonResponse(
        {
            "project_list": project_list
        }
    )