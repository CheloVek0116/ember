from django import forms
from django.views.generic import View, ListView, FormView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .mixins import *



class ProfileWallList(LoginRequiredMixin, ShowWallMixin, ListView):
	"""
	класс для вывода постов в профиле
	"""
	template = 'walls/profile_wall.html'
	role = 'profile'


class FeedList(LoginRequiredMixin, ShowWallMixin, ListView):
	"""
	класс для вывода постов в новостях
	"""
	template = 'walls/feed_wall.html'
	role = 'feed'


class AllProfiles(LoginRequiredMixin, View):
	"""
		
	"""
	def get(self, request):
		subs = self.request.user.sub.values_list('id', flat=True)
		profiles = User.objects.exclude(username=request.user.username)
		return render(request, 'profiles/all_profiles.html', context={'profiles': profiles, 'subscriptions': subs})
		

class Subscribe(LoginRequiredMixin, View):
	"""
		действие кнопки "подписаться"("отписаться")
	"""

	def post(self, request, username):
		if not self.request.user.sub.filter(username=username).exists():
			 self.subscribe(username)
		else:
			self.unsubsribe(username)
		return redirect(request.META.get('HTTP_REFERER'))

	def subscribe(self, username):
		User.objects.get(username=username).subscribers.add(self.request.user)

	def unsubsribe(self, username):
		User.objects.get(username=username).subscribers.remove(self.request.user)


class RegisterFormView(FormView):
    form = UserCreationForm
    template_name = "registration.html"
    success_url = "/accounts/login/"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)



