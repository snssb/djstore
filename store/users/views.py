from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    # В settings - AUTH_USER_MODEL = 'users.User'
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('index')
    title = 'Галерея - Авторизация'

    def form_valid(self, form):
        user = form.get_user()
        if user.is_verified_email:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Ваш аккаунт не подтвержден.')
            return super().form_invalid(form)
            # return self.render_to_response(self.get_context_data(form=form, error='Ваш аккаунт не подтвержден.'))


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрированы! Осталось подтвердить email'
    title = 'Галерея - Регистрация'

    # def get_context_data(self, **kwargs):
    #     context = super(UserRegistrationView, self).get_context_data()
    #     context['title'] = 'Галерея - Регистрация'
    #     return context

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, 'Вы успешно зарегестрированы!')
    #     return response


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегестрированы!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Галерея - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data()
    #     # context['title'] = 'Галерея - Личный кабинет'
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     # context['baskets'] = Basket.objects.filter(user=self.request.user)
    #     return context


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     # baskets = Basket.objects.filter(user=request.user)
#     # total_sum = sum(basket.sum() for basket in baskets)
#     # total_quantity = sum(basket.quantity for basket in baskets)
#
#     # total_sum = 0
#     # total_quantity = 0
#     # for basket in baskets:
#     #     total_sum += basket.sum()
#     #     total_quantity += basket.quantity
#
#     context = {
#         'title': 'Галерея - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'users/profile.html', context)


class UserLogoutView(LogoutView):
    pass

# class UserLogoutView(LogoutView):
#     next_page = reverse_lazy('index')
#     template_name = 'users/logout.html'

# next_page¶
# URL-адрес для перенаправления после выхода из системы. По умолчанию LOGOUT_REDIRECT_URL.
#
# template_name¶
# Полное имя шаблона для отображения после выхода пользователя из системы. По умолчанию registration/logged_out.html.


# @login_required
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Галерея - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(self, request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
