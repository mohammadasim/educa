"""
Django comes with an abstraction layer to work with multiple forms
on the same page. These groups of forms are known as formsets. Formsets
manage multiple instances of a certain Form or ModelForm. All forms are
submitted at once and the formset takes care of the initial number of forms
to display, limiting the maximum number of forms that can be submitted and
validating all the forms.
Formset include an is_valid() method to validate all forms at once. You can
also provide initial data for the forms and specify how many additional
empty forms to display.
"""
from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module
"""
This is the ModuleFormset formset. You build it using the inlineformset_factory
function provided by Django. This function is a small abstraction on top of
formsets that simplify working with related objects.
"""
ModuleFormSet = inlineformset_factory(Course, Module,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)
