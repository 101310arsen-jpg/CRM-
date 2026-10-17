from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import StudentCreateForm, StudentUpdateForm
from .models import Student


class StudentListView(ListView):
    model = Student
    template_name = 'users/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        students = Student.objects.all()
        search = self.request.GET.get('q')
        group = self.request.GET.get('group')
        if search:
            students = students.filter(
                Q(last_name__icontains=search)
                | Q(first_name__icontains=search)
                | Q(middle_name__icontains=search)
            )
        if group:
            students = students.filter(group=group)
        return students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Student.objects.order_by('group').values_list('group', flat=True).distinct()
        context['q'] = self.request.GET.get('q', '')
        context['current_group'] = self.request.GET.get('group', '')
        return context


class StudentDetailView(DetailView):
    model = Student
    template_name = 'users/student_detail.html'
    context_object_name = 'student'


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = 'users/student_form.html'
    success_url = reverse_lazy('users:list')


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'users/student_form.html'
    success_url = reverse_lazy('users:list')


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'users/student_confirm_delete.html'
    success_url = reverse_lazy('users:list')