import os
from django.db import models
from django.conf import settings
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _


class TrackingModel(models.Model):
    creator = models.CharField(verbose_name=_("_creator"),
                               max_length=255,
                               blank=False,
                               editable=False)
    last_edited_by = models.CharField(verbose_name=_("_last_edited_by"),
                                      max_length=255,
                                      blank=True,
                                      editable=False)
    creation_date = models.DateTimeField(verbose_name=_("_creation_date"),
                                         auto_now_add=True)
    visible = models.BooleanField(verbose_name=_("_visible"))

    class Meta:
        abstract = True


class ExtendedFlatPage(FlatPage):
    menu_label = models.CharField(verbose_name=_("_menu_label"),
                                  max_length=255,
                                  blank=False,
                                  default="")


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                verbose_name=_("_related_user"),
                                primary_key=True)
    description = models.TextField(verbose_name=_("_user_description"),
                                   blank=True,
                                   null=True)
    homepage = models.URLField(verbose_name=_("_homepage"),
                               blank=True,
                               null=True)
    twitter = models.CharField(verbose_name=_("_twitter_profile"),
                               max_length=255,
                               blank=True,
                               null=True)
    github = models.CharField(verbose_name=_("_github_profile"),
                              max_length=255,
                              blank=True,
                              null=True)
    image = ImageField(verbose_name=_("_profile_image"),
                       upload_to=os.path.join(settings.MEDIA_ROOT, 'img/profiles'))

    class Meta:
        verbose_name = _("_user_profile")
        verbose_name_plural = _("_user_profiles")

    def __unicode__(self):
        return "%s" % self.user.username


class ContentType(models.Model):
    name = models.CharField(verbose_name=_("_name"),
                            max_length=255)

    class Meta:
        verbose_name = _("_content_type")
        verbose_name_plural = _("_content_types")

    def __unicode__(self):
        return "%s" % self.name


class CommunityLink(TrackingModel):
    title = models.CharField(verbose_name=_("_title"),
                             max_length=255)
    url = models.URLField(verbose_name=_("_url"))
    author = models.CharField(verbose_name=_("_author"),
                              max_length=255)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_("_content_type"))

    class Meta:
        verbose_name = _("_community_link")
        verbose_name_plural = _("_community_links")

    def __unicode__(self):
        return "%s - %s " % (self.title, self.url)


class News(TrackingModel):
    slug = models.SlugField(verbose_name=_("_slug"), unique=True)
    title = models.CharField(verbose_name=_("_title"), max_length=255)
    text = models.TextField(verbose_name=_("_text"))

    class Meta:
        verbose_name = _("_news")
        verbose_name_plural = _("_news")

    def __unicode__(self):
        return "%s" % (self.title)

    def permalink(self):
        return "/news/%s/" % self.slug


class Tutorial(TrackingModel):
    title = models.CharField(verbose_name=_("_title"), max_length=255)
    slug = models.SlugField(verbose_name=_("_slug"), unique=True)
    content = models.TextField(verbose_name=_("_content"))
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_("_content_type"))
    language = models.CharField(choices=settings.LANGUAGES, max_length=8)
    attachment = models.FileField(upload_to="uploads/tutorial/",
                                  verbose_name=_("_attachment"),
                                  blank=True,
                                  null=True)

    class Meta:
        verbose_name = _("_tutorial")
        verbose_name_plural = _("_tutorials")

    def __unicode__(self):
        return "%s" % (self.title)

    def permalink(self):
        return "/tutorials/%s/" % self.slug