from django.db.models import Count, Q
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View


from voiture_noire.models import Prompt
from voiture_noire.forms import PromptForm
                    

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

        try:
            criteria = request.POST['sort_value']
        except Exception:
            raise BadRequest

        match criteria:
            case "prompt_id":
                prompt_list = Prompt.objects.order_by("id")
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

# TODO: eventually handle errors during form validation
def post_prompt(request):
    new_prompt = PromptForm(request.POST)
    if new_prompt.is_valid():
        saved_prompt = new_prompt.save()
        saved_prompt.would_create.add(request.user)
        saved_prompt.would_receive.add(request.user)
        return redirect('voiture_noire:prompts')
    else:
        raise BadRequest

def would_create(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    prompt.would_create.add(request.user)
    return JsonResponse({"code": 200})

def would_not_create(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    prompt = Prompt.objects.get(id=prompt_id)
    prompt.would_create.remove(request.user)
    return JsonResponse({"code": 200})

def would_receive(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    prompt.would_receive.add(request.user)
    return JsonResponse({"code": 200})

def would_not_receive(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    prompt.would_receive.remove(request.user)
    return JsonResponse({"code": 200})
