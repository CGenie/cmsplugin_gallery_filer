from django.core import urlresolvers
from django.contrib import admin

from inline_ordering.admin import OrderableStackedInline
import forms
import models


class ImageInline(OrderableStackedInline):

    model = models.Image

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'src':
            kwargs.pop('request', None)
            kwargs['widget'] = forms.AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageInline, self).\
            formfield_for_dbfield(db_field, **kwargs)


class ContainerImageInline(OrderableStackedInline):

    model = models.ContainerImage


    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'src':
            kwargs.pop('request', None)
            kwargs['widget'] = forms.AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ContainerImageInline, self).\
            formfield_for_dbfield(db_field, **kwargs)


class ContainerAdmin(admin.ModelAdmin):
    inlines = [ContainerImageInline,]

admin.site.register(models.Container, ContainerAdmin)


class ContainerInline(OrderableStackedInline):

    model = models.Container

    readonly_fields = ('changeform_link',)

    def changeform_link(self, instance):
        if instance.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = urlresolvers.reverse(
                'admin:cmsplugin_gallery_container_change', args=(instance.id,)
            )
            return u'<a href="%s" target="_blank">Details</a>' % changeform_url
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header

#    def formfield_for_dbfield(self, db_field, **kwargs):
#        if db_field.name == 'src':
#            kwargs.pop('request', None)
#            kwargs['widget'] = forms.AdminImageWidget
#            return db_field.formfield(**kwargs)
#        return super(ImageInline, self).\
#            formfield_for_dbfield(db_field, **kwargs)
