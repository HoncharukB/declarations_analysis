from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_http_methods

from apps.core.forms import DeclarantForm
from apps.core.models import Declarant
from apps.core.models.declarant import CountryDeclarant, ResponsiblePositionType, CorruptionAffectedType, PublicPersonType
from apps.core.services.declarants_api import DeclarationsService


# Create your views here.

def about_view(request):
    # print(request)
    # return HttpResponse("<html><body>Hello World</body></html>")
    # return HttpResponse("Hello World!")
    return render(request, 'about.html')


def welcome_view(request):
    return render(request, 'core/pages/welcome.html')


@require_http_methods(["GET", "POST"])
def declarants_view(request):
    # POST
    if request.method == "POST":
        lastname = request.POST.get("lastname")
        firstname = request.POST.get("firstname")
        middlename = request.POST.get("middlename")
        work_place = request.POST.get("work_place")
        work_post = request.POST.get("work_post")
        region = request.POST.get("region")
        actual_country = request.POST.get("actual_country")
        responsible_position = request.POST.get("responsible_position")
        corruption_affected = request.POST.get("corruption_affected")
        public_person = request.POST.get("public_person")
        # Тут можна додати валідацію даних
        # Запис в базу даних
        Declarant.objects.create(
            lastname=lastname,
            firstname=firstname,
            middlename=middlename,
            work_place=work_place,
            work_post=work_post,
            region=region,
            actual_country=actual_country,
            responsible_position=responsible_position,
            corruption_affected=corruption_affected,
            public_person=public_person,
        )
        # Редірект
        return redirect("declarants")

    # GET
    context = {
        "declarants_list": Declarant.objects.all(),
        "actual_country_choices": CountryDeclarant,
        "responsible_position_choices": ResponsiblePositionType,
        "corruption_affected_choices": CorruptionAffectedType,
        "public_person_choices": PublicPersonType,
    }
    return render(request, 'core/pages/declarants.html', context)


def declarants_search_view(request):
    results = []
    count = 0
    query = {"lastname": "", "firstname": "", "middlename": ""}

    if request.method == "POST":
        query["lastname"] = request.POST.get("lastname", "").strip()
        query["firstname"] = request.POST.get("firstname", "").strip()
        query["middlename"] = request.POST.get("middlename", "").strip()

        results, count = DeclarationsService.find_declarant(
            lastname=query["lastname"],
            firstname=query["firstname"],
            middlename=query["middlename"],
        )

    return render(request, 'core/pages/declarants_search.html',{"results": results, "query": query, "count": count})

class DeclarantDetailUpdateView(View):
    model = Declarant
    def get(self, request, pk):
        # client = Client.objects.get(pk=pk)
        declarant = get_object_or_404(Declarant, pk=pk)
        declarant_form = DeclarantForm(instance=declarant)
        return render(request, 'core/pages/declarant_detail.html', {'declarant_form': declarant_form})

    def post(self, request, pk):
        declarant = get_object_or_404(Declarant, pk=pk)
        declarant_form = DeclarantForm(request.POST, instance=declarant)
        if 'submit_declarant' in request.POST:
            if declarant_form.is_valid():
                declarant_form.save()
                # Перезавантаження сторінки з актуальними даними із бази даних
                return redirect("declarant_detail", pk=pk)
            # else:
            #     print(declarant_form.errors)
            #     return HttpResponse(declarant_form.errors.as_ul(), content_type="text/html")
        # else:
        #     return redirect("declarant_detail", pk=pk)
        # Якщо форма невалідна, повертаємо той самий шаблон з формою та помилками
        return render(request, 'core/pages/declarant_detail.html', {'declarant_form': declarant_form})