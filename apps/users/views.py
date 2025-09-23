from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from apps.users.forms import CustomeUserCreationForm


# Create your views here.
class RegisterView(generic.CreateView):
    form_class = CustomeUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def logged_out_view(request):
    return render(request, 'registration/logout.html')