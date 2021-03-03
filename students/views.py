from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from courses.models import Course

from .forms import CourseEnrollForm


# pylint disable='too-many-ancestors'
class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'],
            password=cd['password1']
        )
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """
    View for enrolling a student to a course. The form is used
    to get the course details. The user, that is student is logged in
    so associated with request. When a valid form is submitted, we
    get the course from the from and add the user/student to the
    course model's student attribute.
    """
    course = None
    form_class = CourseEnrollForm
    template_name = 'students/course/detail.html'

    def form_valid(self, form):
        course_id = form.cleaned_data['course']
        self.course = get_object_or_404(Course, id=course_id)
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """
    View to show the courses that a student is enrolled on.
    """
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    """
    View showing course detail for a student. We have two course detail
    views, one for the teacher and one for student.
    """
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        """
        Return only courses that the student is enrolled on.
        :return:
        """
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context
