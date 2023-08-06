from flask_themes2 import get_theme, render_theme_template

from cornerstone.models import MenuLink
from cornerstone.settings import get_setting


def render(template, **context):
    theme_name = get_setting('theme', 'bootstrap4')
    context['links'] = MenuLink.query.filter_by(is_enabled=True).order_by(MenuLink.weight.asc()).all()
    return render_theme_template(get_theme(theme_name), template, **context)
