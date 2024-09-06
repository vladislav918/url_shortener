from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from .forms import LoginUserForm, RegisterUserForm
from .models import CustomUser

from url.models import Shortener
from url.services import get_dict_user_and_urls


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


@method_decorator(user_passes_test(lambda u: u.role == CustomUser.ADMIN), name='dispatch')
class AdminUserCreateView(CreateView):
    model = CustomUser
    template_name = 'users/user_form.html'
    fields = ['username', 'email', 'password'] 
    success_url = reverse_lazy('admin_statistics')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.role == CustomUser.ADMIN), name='dispatch')
class AdminTemplate(TemplateView):
    template_name = 'users/admin_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = get_dict_user_and_urls([CustomUser.USER])
        return context


@method_decorator(user_passes_test(lambda u: u.role == CustomUser.ADMIN), name='dispatch')
class DeleteUrlView(DeleteView):
    model = Shortener
    success_url = reverse_lazy('admin_statistics')


@method_decorator(user_passes_test(lambda u: u.role == CustomUser.ADMIN), name='dispatch')
class DeleteUserView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('admin_statistics')
