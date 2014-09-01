# -*- coding: utf-8 -*-

from cms.api import get_page_draft
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.utils import get_cms_setting
from cms.utils.permissions import has_page_change_permission
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from .models import RichPage, RichSlideshow
from cms.utils.urlutils import add_url_parameters
from cms.utils.permissions import get_user_sites_queryset, has_page_change_permission
from cms.utils import get_language_from_request
from cms.utils.i18n import get_language_object

# Pages
PAGE_MENU_BREAK = 'Page Menu Break'
PAGE_MENU_ADD = 'admin:cms_page_add'
PAGE_MENU_DELETE = 'admin:cms_page_delete'

# Rich Page
RICHPAGE_MENU_ADD = 'admin:rich_page_richpage_add'
RICHPAGE_MENU_CHANGE = 'admin:rich_page_richpage_change'
RICHPAGE_MENU_DELETE = 'admin:rich_page_richpage_delete'

# Rich Slideshow
RICHSLIDESHOW_MENU_ADD = 'admin:rich_page_richslideshow_add'
RICHSLIDESHOW_MENU_CHANGE = 'admin:rich_page_richslideshow_change'

@toolbar_pool.register
class RichPageToolbar(CMSToolbar):
    def populate(self):

        # always use draft if we have a page
        self.page = get_page_draft(self.request.current_page)

        if not self.page:
            # Nothing to do
            return

        self.lang = get_language_from_request(self.request)

        try:
            self.title_page = self.page.title_set.get(language=self.lang)
        except:
            # Nothing to do
            return

        #
        # Remove default menu
        #
        #self.page_menu = self.toolbar.get_or_create_menu('page')
        #self.toolbar.remove_item(self.page_menu)

        #
        # check global permissions
        #
        if get_cms_setting('PERMISSION'):
            has_global_current_page_change_permission = has_page_change_permission(self.request)
        else:
            has_global_current_page_change_permission = False

        can_change = self.request.current_page and self.request.current_page.has_change_permission(self.request)

        if has_global_current_page_change_permission or can_change:
            # Page urls
            page_url = reverse(PAGE_MENU_ADD)
            delete_page_url = reverse(PAGE_MENU_DELETE, args=(self.page.pk,))
            sub_page_params = {'edit': 1, 'position': 'last-child', 'target': self.page.pk}

            # Rich page urls
            rich_page_add_url = reverse(RICHPAGE_MENU_ADD) + '?extended_object=%s' % self.title_page.pk
            
            # Rich Slideshow
            rich_slideshow_add_url = reverse(RICHSLIDESHOW_MENU_ADD) + '?extended_object=%s' % self.page.pk

            
            #
            # build the Pages menu
            #

            menu = self.toolbar.get_or_create_menu('rich-page-new', _('Pages'), position=1)
            menu.add_modal_item(_('New Page'), url=page_url)
            menu.add_modal_item(_('New Sub Page'), url=add_url_parameters(page_url, sub_page_params))
            menu.add_modal_item(_('Delete page'), url=delete_page_url)

            try:
                rich_page = RichPage.objects.get(extended_object_id=self.title_page.pk)
            except RichPage.DoesNotExist:
                rich_page = None


            try:
                rich_slideshow = RichSlideshow.objects.get(extended_object_id=self.page.id)
            except RichSlideshow.DoesNotExist:
                rich_slideshow = None

            if not rich_page:
                menu.add_break(PAGE_MENU_BREAK)
                menu.add_modal_item(_('Add article'), url=rich_page_add_url)

            #
            # Check if the page has rich content or rich collection
            #
            if rich_page:
                menu.add_break(PAGE_MENU_BREAK)
                
                #
                # Rich page urls
                #
                rich_page_change_url = reverse(RICHPAGE_MENU_CHANGE, args=(self.title_page.pk,)) + '?extended_object=%s' % self.title_page.pk
                rich_page_delete_url = reverse(RICHPAGE_MENU_DELETE, args=(self.title_page.pk,)) + '?extended_object=%s' % self.title_page.pk

                menu.add_modal_item(_('Edit article'), url=rich_page_change_url)
                menu.add_modal_item(_('Delete article'), url=rich_page_delete_url)

                menu.add_break(PAGE_MENU_BREAK)

                if rich_slideshow:
                    rich_slideshow_change_url = reverse(RICHSLIDESHOW_MENU_CHANGE, args=(rich_slideshow.pk,)) + '?extended_object=%s' % self.page.pk
                    menu.add_modal_item(_('Delete slideshow'), url=rich_slideshow_change_url)
                else:
                    menu.add_modal_item(_('Add slideshow'), url=rich_slideshow_add_url)
                

                