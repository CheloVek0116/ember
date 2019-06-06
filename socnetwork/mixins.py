from django.shortcuts import render, redirect

from .models import *
from .forms import *

class ShowWallMixin:
	"""
	миксин вывода ленты постов

	# template(обязательно)    - шаблон куда выводить посты
	# role(обязательно)        - роль выводимых постов (1. 'profile' - вывод постов определенного профиля, определяется в аргументе user	2. 'feed' - вывод постов в новостную ленту)
	# redirect(не обязательно) - ссылка для редиректа после создания нового поста пользователем(если это нужно)

	"""
	template = None 
	role     = None 
	redirect = None 


	def get(self, request, **kwargs):
		form = PostForm()
		subs = self.request.user.sub.values_list('id', flat=True) 

		if self.role == 'feed':
			user_posts = Post.objects.filter(user=request.user)
			subs_posts = Post.objects.filter(user__id__in=subs)
			posts = (subs_posts | user_posts).order_by('-published')

			context = {	'posts': posts, 
					'form': form, 
					}

		elif self.role == 'profile':
			subs = self.request.user.sub.values_list('id', flat=True)
			user = User.objects.filter(username=kwargs['username'])
			if user.exists():
				posts = Post.objects.filter(user__in=user).order_by('-published')

				context = {'profile': user[0],
						   'posts': posts, 
						   'form': form, 
						   'subscriptions': subs,
						}
			else:
				return render(request, 'error_page.html')

		return render(request, self.template, context=context)

	def post(self, request, **kwargs):
		author = request.user
		if self.redirect:
			pass
		else:
			if self.role == 'profile':
				self.redirect = author.get_absolute_url()
			elif self.role == 'feed':
				self.redirect = 'feed_list_url'

		bound_form = PostForm(request.POST)
		if bound_form.is_valid():
			bound_form.instance.user = author
			new_post = bound_form.save()
			return redirect(self.redirect)
		return render(request, self.template, context={'posts': posts, 'form': bound_form})
