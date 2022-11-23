# 1450 / ????
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import gettext as _
from helpful.fields import upload_to

from tree_queries.models import TreeNode
from tree_queries.query import TreeQuerySet


class URL(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=256)
    url = models.CharField(verbose_name=_("URL or URL RegEx"), max_length=2048)
    regex = models.BooleanField(verbose_name=_("RegEx"), default=False)

    # Meta base
    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("URL")
        verbose_name_plural = _("URLs")


class Page(TreeNode):
    name = models.CharField(_("Name"), max_length=128)

    # SEO
    title = models.CharField(_("Title"), max_length=256, blank=True, null=True)
    header = models.CharField(_("Header"), max_length=256, blank=True, null=True)
    keywords = models.CharField(_("Keywords"), max_length=1024, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=2048, blank=True, null=True)
    head_code = models.TextField(_("Head code"), blank=True, null=True)
    footer_code = models.TextField(_("Footer code"), blank=True, null=True)

    # Content
    image = models.ImageField(_("Image"), upload_to=upload_to, blank=True)
    intro = models.TextField(_("Intro"), blank=True, null=True)
    text = models.TextField(_("Text"), blank=True, null=True)

    # Settings
    sites = models.ManyToManyField(Site, related_name="pages", verbose_name=_("Sites"), blank=True)
    slug = models.SlugField(_("Slug"), max_length=128, blank=True, default="")
    url = models.CharField(_("URL"), max_length=2048, editable=False)
    template = models.CharField(_("Template"), max_length=128, null=True, blank=True)
    per_page = models.IntegerField(_("Items per page"), default=10)

    position = models.PositiveIntegerField(_("Position"), default=500)

    # Meta base
    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    def public_children(self):
        return self.children.filter(public=True)

    def save(self, sort=True, *args, **kwargs):
        if not self.title:
            self.title = self.name
        if not self.header:
            self.header = self.name

        self.url = "/"
        if self.slug:
            if self.parent:
                self.url = self.parent.url
            self.url += self.slug
            if settings.APPEND_SLASH:
                self.url += "/"
        super(Page, self).save(*args, **kwargs)
        for children in self.children.all():
            children.save()

    objects = TreeQuerySet.as_manager(with_tree_fields=True)

    class Meta:
        base_manager_name = "objects"
        ordering = ["position"]
        # TODO: FIX
        # unique_together = ['sites', 'url']
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


class Area(models.Model):
    name = models.CharField(_("Name"), max_length=128)
    slug = models.SlugField(_("Slug"), unique=True)

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.name


class Block(TreeNode):
    name = models.CharField(_("Name"), max_length=128)
    slug = models.SlugField(_("Slug"))

    header = models.CharField(_("Header"), max_length=256, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=2048, blank=True, null=True)
    text = models.TextField(_("Text"), blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to=upload_to, blank=True, null=True)

    pages = models.ManyToManyField(Page, verbose_name=_("Pages"), related_name="blocks", blank=True)

    area = models.ForeignKey(Area, verbose_name=_("Area"), related_name="blocks", on_delete=models.CASCADE)
    position = models.PositiveIntegerField(_("Position"), default=500)

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["position", "created_at"]
        verbose_name = _("Block")
        verbose_name_plural = _("Blocks")


class Element(TreeNode):
    name = models.CharField(_("Name"), max_length=128)
    block = models.ForeignKey(Block, verbose_name=_("Block"), on_delete=models.CASCADE)

    header = models.CharField(_("Header"), max_length=256, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=2048, blank=True, null=True)
    text = models.TextField(_("Text"), blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to=upload_to, blank=True, null=True)

    position = models.PositiveIntegerField(_("Position"), default=500)

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.name

    def public_children(self):
        return self.children.filter(public=True)

    class Meta:
        ordering = ["position", "created_at"]
        verbose_name = _("Element")
        verbose_name_plural = _("Elements")


# 1500
# add menu
