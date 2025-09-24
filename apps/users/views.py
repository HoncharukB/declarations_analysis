from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from apps.users.models import CustomUser

from apps.users.forms import CustomeUserCreationForm


# Create your views here.
class RegisterView(generic.CreateView):
    form_class = CustomeUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def logged_out_view(request):
    return render(request, 'registration/logout.html')

@login_required
def users_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role = request.POST.get("role")
        user = CustomUser.objects.get(id=user_id)
        user.role = role
        user.save()
        return redirect("users")  # після збереження — оновлюємо сторінку

    users = CustomUser.objects.all()
    return render(request, "registration/users.html", {"users": users})