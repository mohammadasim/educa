from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from .fields import OrderField


class Subject(models.Model):
    """Subject model"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    """Course model"""

    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    """Module model"""
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # The order field is named order, for_fields is set to course,
    # This means that the order of a new module will be assigned by
    # adding 1 to the last module of the same course object.
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


class Content(models.Model):
    """Content model"""

    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text', 'video', 'image', 'file'
                                     )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    """Abstract model"""

    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        """
        render_to_string, loads a template like get_template()
        and calls its render() method immediately. It takes as
        argument template_name, context, option request, optional
        template engine.
        The render method itself is designed to render content.
        so when a student selects a course, it will get a list
        of course modules. And each module will have a number of
        contents, these contents will be either text, image, file or video.
        We have designed generic text, file, image and video html templates
        that displays these specific content.
        So when a module is selected by a student, we iterate over the modules
        associated content and on each content we call the render method, which then
        displays the text, file, image or video html file.
        what it does
        :return:
        """
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )


class Text(ItemBase):
    """Model for text content"""
    content = models.TextField()


class File(ItemBase):
    """Model for file content"""
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """Model for Image content"""
    file = models.ImageField(upload_to='images')


class Video(ItemBase):
    """Model for Video content"""
    url = models.URLField()
