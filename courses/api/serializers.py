from rest_framework import serializers
from courses.models import Subject
from courses.models import Course
from courses.models import Module


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize instances of Subject Model
    """

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize instance of Module model
    """

    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize instances of Course Model
    """
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                  'created', 'owner', 'modules']
