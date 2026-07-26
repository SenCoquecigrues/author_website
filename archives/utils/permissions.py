import datetime


class AccessPermission:
    def get_story_is_allowed(request, story):
        if request.user.is_authenticated is False and story.visibility != 'Everyone':
            return False
        elif request.user.id != story.author.member.id and story.visibility == 'Private':
            return False
        elif request.user.id != story.author.member.id and story.story_date > datetime.date.today():
            return False

        return True

    def modify_story_is_allowed(request, story):
        return request.user.id == story.author.member.id