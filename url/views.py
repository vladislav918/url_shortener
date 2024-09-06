from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Shortener
from .forms import ShortenerForm
from .services import shorten_url, get_list_url, get_dict_user_and_urls


class AddUrlView(LoginRequiredMixin, FormView):
    form_class = ShortenerForm
    template_name = 'url/add_url.html'
    success_url = '/' 

    def post(self, request, *args, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = get_dict_user_and_urls()
        return context


class RedirectShortUrlView(View):
    def get(self, request, short_url):
        short_url_obj = get_object_or_404(Shortener, short_url=short_url)
        short_url_obj.click_count += 1
        short_url_obj.save()
        return redirect(short_url_obj.long_url)
