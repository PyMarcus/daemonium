import json
from typing import List

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests


class IndexView(LoginRequiredMixin, TemplateView):
    template_name: str = 'index.html'

    def get_context_data(self, **kwargs):
        response = requests.get("http://localhost:9999/api/v1/ransoms/")
        context = super().get_context_data(**kwargs)
        context['info'] = json.loads(response.content)
        return context
