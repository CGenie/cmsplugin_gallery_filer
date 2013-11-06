import threading

from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from inline_ordering.models import Orderable
from filer.fields.image import FilerImageField

import utils

localdata = threading.local()
localdata.TEMPLATE_CHOICES = utils.autodiscover_templates()
TEMPLATE_CHOICES = localdata.TEMPLATE_CHOICES


class GalleryPlugin(CMSPlugin):

    def copy_relations(self, oldinstance):
        for img in oldinstance.image_set.all():
            new_img = Image()
            new_img.gallery=self
            new_img.src = img.src
            new_img.title = img.title
            new_img.alt = img.alt
            new_img.save()

    template = models.CharField(max_length=255,
                                choices=TEMPLATE_CHOICES,
                                default=TEMPLATE_CHOICES[0][0],
                                editable=len(TEMPLATE_CHOICES) > 1)

    def __unicode__(self):
        return _(u'%(count)d image(s) in gallery') % {'count': self.image_set.count()}


class Image(Orderable):

    def get_media_path(self, filename):
        pages = self.gallery.placeholder.page_set.all()
        return pages[0].get_media_path(filename)

    gallery = models.ForeignKey(GalleryPlugin, verbose_name=_("Gallery"))
    src = FilerImageField(null=True, blank=True)
    src_height = models.PositiveSmallIntegerField(_("Image height"), editable=False, null=True)
    src_width = models.PositiveSmallIntegerField(_("Image height"), editable=False, null=True)
    title = models.CharField(_("Title"), max_length=255, blank=True)
    alt = models.TextField(_("Alt text"), blank=True)

    def __unicode__(self):
        return self.title or self.alt or str(self.pk)


class SmartGalleryPlugin(CMSPlugin):
#
#    def copy_relations(self, oldinstance):
#        for img in oldinstance.image_set.all():
#            new_img = Image()
#            new_img.gallery=self
#            new_img.src = img.src
#            new_img.title = img.title
#            new_img.alt = img.alt
#            new_img.save()


    def copy_relations(self, oldinstance):
        for container in oldinstance.container_set.all():
            new_container = Container()
            new_container.gallery = self
            new_container.title = container.title
            new_container.url = container.url
            new_container.save()
            new_container.copy_relations(container)

    template = models.CharField(max_length=255,
                                choices=TEMPLATE_CHOICES,
                                default=TEMPLATE_CHOICES[0][0],
                                editable=len(TEMPLATE_CHOICES) > 1)

    def __unicode__(self):
        return _(u'%(count)d container(s) in gallery') % {'count': self.container_set.count()}


class Container(Orderable):

    gallery = models.ForeignKey(SmartGalleryPlugin, verbose_name=_("Gallery"))
    title = models.CharField(("Title"), max_length=255, blank=True)
    url = models.CharField(_("URL"), max_length=255, blank=True)

    def copy_relations(self, oldinstance):
        for img in oldinstance.containerimage_set.all():
            new_img = ContainerImage()
            new_img.container = self
            new_img.src = img.src
            new_img.title = img.title
            new_img.alt = img.alt
            new_img.save()

    def __unicode__(self):
        return self.title or self.url or str(self.pk)


class ContainerImage(Orderable):

    def get_media_path(self, filename):
        pages = self.gallery.placeholder.page_set.all()
        return pages[0].get_media_path(filename)

    container = models.ForeignKey(Container, verbose_name=_("Container"))
    src = FilerImageField(null=True, blank=True)
    src_height = models.PositiveSmallIntegerField(_("Image height"), editable=False, null=True)
    src_width = models.PositiveSmallIntegerField(_("Image height"), editable=False, null=True)
    title = models.CharField(_("Title"), max_length=255, blank=True)
    alt = models.TextField(_("Alt text"), blank=True)

    def __unicode__(self):
        return self.title or self.alt or str(self.pk)
