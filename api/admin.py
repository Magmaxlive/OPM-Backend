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
    list_display = ('title', 'author', 'status', 'published_at')
    list_filter = ('status',)
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Enquiry_form)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'subject', 'status', 'submitted_date')
    list_filter = ('status', 'submitted_date')
    search_fields = ('full_name', 'email', 'subject')
    list_editable = ('status',)
    ordering = ('-submitted_date',)


@admin.register(Rental_form)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'property_type', 'status', 'submitted_at')
    list_filter = ('status', 'property_type')
    search_fields = ('first_name', 'last_name', 'email', 'address')
    list_editable = ('status',)
    ordering = ('-submitted_at',)


admin.site.register(Subscribers_Form)
