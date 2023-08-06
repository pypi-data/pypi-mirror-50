import inspect
import re
from pathlib import Path

from unidecode import unidecode
from flask import flash, redirect, url_for, request
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_user import current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from cornerstone.models import MenuLink, Page, Preacher, Sermon, Topic, User, session
from cornerstone.settings import get_all_settings, get_setting, has_setting, save_setting


def _create_slug(title):
    """
    Convert the title to a slug
    """
    return re.sub(r'\W+', '-', unidecode(title).lower()).strip('-')


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class MenuLinkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    is_enabled = BooleanField('Enabled')


class AuthorizedMixin(object):
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('/'))
        else:
            return redirect(url_for('user.login', next=request.url))


class AuthorizedAdminIndexView(AuthorizedMixin, AdminIndexView):
    pass


class AuthorizedModelView(AuthorizedMixin, ModelView):
    extra_js = ['//cdn.ckeditor.com/4.11.4/full/ckeditor.js']
    column_exclude_list = ('password', 'can_edit')
    column_descriptions = {
        'weight': 'Use this to order items in the menu'
    }
    form_excluded_columns = ('slug', 'can_edit')
    form_overrides = {
        'password': PasswordField,
        'weight': IntegerField
    }

    def on_model_change(self, form, model, is_create):
        if isinstance(model, Page):
            model.slug = _create_slug(model.title)
            if get_setting('pages-in-menu', False) and not MenuLink.query.filter_by(slug=model.slug).first():
                session.add(
                    MenuLink(
                        title=model.title,
                        slug=model.slug,
                        url=url_for('pages.get', slug=model.slug),
                        is_enabled=True
                    )
                )
                session.commit()


class SettingsView(AuthorizedMixin, BaseView):
    @expose('/', methods=['GET'])
    def index(self):
        settings = get_all_settings()
        return self.render('admin/settings.html', settings=settings)

    @expose('/', methods=['POST'])
    def index_post(self):
        for key, value in request.form.items():
            if has_setting(key):
                save_setting(key, value)
        return redirect(self.get_url('settings.index'))


class MenuView(AuthorizedMixin, BaseView):
    @expose('/', methods=['GET'])
    def index(self):
        links = MenuLink.query.order_by(MenuLink.weight).all()
        return self.render('admin/menu.html', links=links)

    @expose('/new', methods=['GET', 'POST'])
    def new(self):
        form = MenuLinkForm()
        if request.method == 'POST' and form.validate_on_submit():
            link = MenuLink(title=form.title.data, url=form.url.data, slug=_create_slug(form.title.data),
                            is_enabled=form.is_enabled.data, can_edit=True)
            session.add(link)
            session.commit()
            flash('Successfully created menu item', 'success')
            return redirect(url_for('menu.index'))
        return self.render('admin/menu_edit.html', form=form)

    @expose('/<int:id>', methods=['GET', 'POST'])
    def edit(self, id):
        link = MenuLink.query.get(id)
        if not link:
            flash('No such menu item', 'error')
            return redirect(url_for('menu.index'))
        form = MenuLinkForm(obj=link)
        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(link)
            session.add(link)
            session.commit()
            flash('Successfully saved menu item', 'success')
            return redirect(url_for('menu.index'))
        return self.render('admin/menu_edit.html', form=form, link=link)


def _get_template_mode():
    """
    Detect template mode. This allows us to use the bootstrap4 theme if it exists, and fall back to bootstrap3.

    NB: This is a temporary workaround until the Bootstrap 4 branch merges into Flask-Admin master
    """
    templates_path = Path(inspect.getfile(Admin)).resolve().parent / 'templates'
    admin_themes = [theme.name for theme in templates_path.iterdir()]
    if 'bootstrap4' in admin_themes:
        return 'bootstrap4'
    else:
        return 'bootstrap3'


# Set up the admin
admin = Admin(name='CornerstoneCMS', template_mode=_get_template_mode(), index_view=AuthorizedAdminIndexView())
admin.add_view(AuthorizedModelView(Page, session, name='Pages'))
admin.add_view(AuthorizedModelView(Sermon, session, name='Sermons', category='Sermons'))
admin.add_view(AuthorizedModelView(Preacher, session, name='Preachers', category='Sermons'))
admin.add_view(AuthorizedModelView(Topic, session, name='Topics', category='Sermons'))
admin.add_view(MenuView(name='Menu', endpoint='menu'))
admin.add_view(SettingsView(name='Settings', endpoint='settings'))
admin.add_view(AuthorizedModelView(User, session, name='Users'))
