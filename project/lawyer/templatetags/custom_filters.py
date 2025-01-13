from django import template

register = template.Library()


@register.filter
def star_list(value):
    if value:
        return f"{value:.1f} ⭐"
    return "Нет оценок"


@register.filter
def stars(value):
    full_stars = int(value)
    half_star = value - full_stars >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)

    stars_html = '⭐' * full_stars
    if half_star:
        stars_html += '½⭐'
    stars_html += '☆' * empty_stars

    return stars_html
