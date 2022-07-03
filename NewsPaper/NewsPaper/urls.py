from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
# from news.views import HelloTask
from django.views.i18n import set_language

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic import View
from django.shortcuts import render
from django.conf import settings


# def set_language(request):
#     print(request.POST)
#     lang = request.POST.get('language', 'en')
#     request.session[settings.LANGUAGE_SESSION_KEY] = lang
#     response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#     response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
#     return response

# class template_view(View):
#     def get(self, request):
#         string = _('default')
#
#         context = {
#             'string':string
#         }
#
#         return HttpResponse(render(request, 'default.html', context))
#
#     def post(self, request):
#         return HttpResponse("<h2>Change language</h2>")

urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')),
   path('admin/', admin.site.urls),
   path('', include('news.urls')),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('news/', include('news.urls')),

   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
   path('appointments/', include(('appointments.urls', 'appointments'), namespace='appointments')),

]

urlpatterns += [
    path(r'set-language/', set_language, name='set_language'),
]