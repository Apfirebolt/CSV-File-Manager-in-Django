from django.shortcuts import render
from django.views.generic import FormView, ListView, DetailView, TemplateView, DeleteView, View
from . forms import CustomUserForm
from . models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateUserView(FormView):
    """ View written for user registration """
    template_name = 'accounts/register.html'
    form_class = CustomUserForm
    success_url = 'home'

    def form_valid(self, form):
        # create new user instance and save data
        userObj = form.save(commit=False)
        userObj.password = make_password(form.cleaned_data['password1'])
        userObj.staff = False
        userObj.admin = False
        userObj.save()
        messages.add_message(self.request, messages.INFO, 'You have successfully registered, Please login to continue!')
        return HttpResponseRedirect(reverse('login'))

    def form_invalid(self, form):
        # If form is invalid return superclass method
        return super(CreateUserView, self).form_invalid(form)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        userPassword = request.POST['password']

        user = authenticate(username=username, password=userPassword)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO,
                                 'You have successfully logged in! Please continue to your dashboard!')
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        else:
            messages.add_message(request, messages.ERROR,
                                 'Invalid credentials provided, failed to login!')
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        return render(request, 'accounts/login.html', {})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             'Successfully logged out, Please login to continue!')
        return HttpResponseRedirect(reverse('login'))


class DetailUserView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/dashboard.html'
    queryset = CustomUser.objects.all()

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)


class DeleteAccountView(DeleteView):
    pass
