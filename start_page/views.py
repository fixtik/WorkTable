from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,HttpRequest



class IndexView(View):
    def get(self, reguest: HttpRequest) -> HttpResponse:
        return render(reguest, 'start_page/index.html')