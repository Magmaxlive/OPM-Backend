from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Blog,Enquiry_form,Subscribers_Form,Rental_form


class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = '__all__'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'author', 'is_published', 'published_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Enquiry_form)
admin.site.register(Subscribers_Form)
admin.site.register(Rental_form)
