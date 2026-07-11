import json
from datetime import date, datetime

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Member


@method_decorator(csrf_exempt, name='dispatch')
class Birthday(View):
    def get(self, request, *args, **kwargs):
        date_param = request.GET.get('date')

        if date_param:
            try:
                query_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                query_date = date.today()
        else:
            query_date = date.today()

        profiles = Member.objects.filter(birthday__isnull=False).exclude(discord_id="")
        data = [
            {'discord_ids': member.discord_id} for member in profiles
            if member.birthday.day == query_date.day and member.birthday.month == query_date.month
        ]
        return JsonResponse({'members_birthdays': data, 'query_date': query_date.isoformat()})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'errorMsg': 'Invalid JSON'}, status=400)

        date_param = data.get('birthday')
        discord_id_param = data.get('discord_id')

        if not discord_id_param or not date_param:
            return JsonResponse(
            {'errorMsg': "Expecting a 'birthday' field (YYYY-MM-DD) and a 'discord_id' field."},
            status=400
        )

        try:
            query_date = datetime.strptime(date_param, '%Y-%m-%d').date()
        except Exception:
            return JsonResponse(
            {'errorMsg': "Expecting a 'birthday' field (YYYY-MM-DD) and a 'discord_id' field."},
            status=400
        )

        try:
            member = Member.objects.get(discord_id=discord_id_param)
        except Exception:
            return JsonResponse(
            {'errorMsg': "No member with that discord id."},
            status=404
        )

        birthday_person = member
        birthday_person.birthday = query_date
        birthday_person.save()

        return JsonResponse({'errorMsg':""})