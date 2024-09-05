from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Shortener
from .forms import ShortenerForm
from .services import shorten_url, get_list_url

from users.models import CustomUser


class AddUrlView(LoginRequiredMixin, FormView):
    form_class = ShortenerForm
    template_name = 'url/add_url.html'
    success_url = '/' 

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        form = self.get_form()
        if form.is_valid():
            new_url = shorten_url(request, form.cleaned_data['long_url'])

            return JsonResponse({'long_url': new_url.long_url, 'short_url': new_url.short_url})

        return JsonResponse({'error': 'Invalid URL'}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ShortenerForm()
        context['url'] = get_list_url(self.request)
        return context


class UrlListView(ListView):
    model = Shortener
    template_name = 'url/url_list.html'
    context_object_name = 'urls'

    def get_queryset(self):
        users = CustomUser.objects.prefetch_related('shortener_set').all()
        urls = []
        for user in users:
            user_urls = user.shortener_set.all()
            urls.append({
                'user': user,
                'urls': user_urls
            })
        return urls
