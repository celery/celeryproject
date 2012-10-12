from django.contrib import admin
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from sorl.thumbnail.admin import AdminImageMixin
from models import UserProfile
from models import News
from models import Tutorial
from models import CommunityLink
from models import ContentType
from models import ExtendedFlatPage

class TrackingModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user.username
        if not change:
            obj.creator = request.user.username
        obj.save()
        
class NewsAdmin(TrackingModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    
    class Media:
        js = (settings.STATIC_URL+'js/tiny_mce/tiny_mce.js',
              settings.STATIC_URL+'js/tiny_mce/textarea.js',)
        
class TutorialAdmin(TrackingModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    
    class Media:
        js = (settings.STATIC_URL+'js/tiny_mce/tiny_mce.js',
              settings.STATIC_URL+'js/tiny_mce/textarea.js',)
        
class CommunityLinkAdmin(TrackingModelAdmin):
    pass

class ContentTypeAdmin(TrackingModelAdmin):
    pass

class UserProfileAdmin(AdminImageMixin, admin.ModelAdmin):
    class Media:
        js = (settings.STATIC_URL+'js/tiny_mce/tiny_mce.js',
              settings.STATIC_URL+'js/tiny_mce/textarea.js',)
    
    
class ExtendedFlatPageForm(FlatpageForm):
  class Meta:
      model = ExtendedFlatPage

class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'menu_label')}),
        ('Advanced options', {'classes': ('collapse',), 
        'fields': ('enable_comments', 'registration_required',
        'template_name')}),
    )
    class Media:
        js = (settings.STATIC_URL+'js/tiny_mce/tiny_mce.js',
              settings.STATIC_URL+'js/tiny_mce/textarea.js',)

admin.site.register(News, NewsAdmin)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(CommunityLink, CommunityLinkAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.unregister(FlatPage)
admin.site.register(ExtendedFlatPage, ExtendedFlatPageAdmin)
