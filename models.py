# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from djangocms_text_ckeditor.fields import HTMLField
from cms.models.fields import PlaceholderField
from taggit.managers import TaggableManager
from cms.models.pagemodel import Page
from cms.extensions import PageExtension, TitleExtension
from cms.extensions.extension_pool import extension_pool
from aldryn_gallery.cms_plugins import GalleryCMSPlugin, SlideCMSPlugin, SlideFolderCMSPlugin
from django.conf import settings

class RichPage(TitleExtension):
    key_visual = FilerImageField(verbose_name=_('Lead Image'), blank=True, null=True)
    lead_in = HTMLField(_('Lead-in'),
                        help_text=_('Will be displayed as short description of the article.'), default="Your lead in text")

    body = HTMLField(_('Body'),
                        help_text=_('Content of the article.'), default="Your body text")
    
    tags = TaggableManager(blank=True)

    slideshow = PlaceholderField('richpage_slideshow', related_name='richpage_slideshow')


class RichSlideshow(PageExtension):
    slideshow_title = models.CharField(max_length=100, default='Slideshow title')

    def save(self, *args, **kwargs):
        from cms.api import add_plugin

        if not self.pk:
            super(RichSlideshow, self).save(*args, **kwargs)
            page = self.extended_object

            placeholder = page.get_title_obj().richpage.slideshow

            language = settings.LANGUAGES[0][0]

            gallery_plugin = add_plugin(placeholder, GalleryCMSPlugin, language)
            
            data = {'folder_id': 1} # TODO add new folder for each slideshow
            
            child_plugin = add_plugin(placeholder, SlideFolderCMSPlugin, language, target=gallery_plugin, **data)
        else:
            super(RichSlideshow, self).save(*args, **kwargs)


extension_pool.register(RichPage)
extension_pool.register(RichSlideshow)

