from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def visible_chapters(context, story):
    return story.visible_chapters(context["request"].user)