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
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from . serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.dispatch import receiver
from django.db.models.signals import post_save


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
        return HttpResponseRedirect(reverse('accounts:login'))

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
        return HttpResponseRedirect(reverse('accounts:login'))


class DetailUserView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/dashboard.html'
    queryset = CustomUser.objects.all()

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)


class DeleteAccountView(DeleteView):
    pass


class RegisterUserApiView(CreateAPIView):
    """ API View for user Registration """

    serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
       try:
           serializer = self.get_serializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           validatedData = serializer.validated_data
           instance = self.perform_create(serializer)
           return Response(
               {'message': 'You have been successfully registered', 'success': True, 'data': serializer.data},
               status=status.HTTP_201_CREATED)
       except Exception as err:
           print(err)
           return Response({'message': 'Failed to register, some error occurred!', 'success': False},
               status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Update user password here
        return serializer.save(password=make_password(serializer.validated_data['password']))


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomObtainAuthToken(ObtainAuthToken):

  def post(self, request, *args, **kwargs):
    response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
    token = Token.objects.get(key=response.data['token'])
    return Response({'token': token.key, 'id': token.user_id, }, status=status.HTTP_200_OK)


class DashboardAPIView(RetrieveAPIView):
    """ API Detail View for user data """

    serializer_class = UserSerializer

    def get_object(self):
        return CustomUser.objects.get(id=self.request.user.id)


class ListAllUsersApiView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = []
    queryset = CustomUser.objects.all()




