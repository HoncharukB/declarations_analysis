import uuid

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_http_methods
from urllib.parse import urlencode

from apps.core.forms import DeclarantForm
from apps.core.models import Declarant
from apps.core.models.declarant import CountryDeclarant, ResponsiblePositionType, CorruptionAffectedType, PublicPersonType
from apps.core.services.declarants_api import DeclarationsService



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.core.models import Declarant, Declaration
from apps.users.models import CustomUser, UserDeclaration
from apps.core.services.declarants_api import DeclarationsService
from datetime import datetime
import requests



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
    query = {
        "lastname": request.GET.get("lastname", "").strip(),
        "firstname": request.GET.get("firstname", "").strip(),
        "middlename": request.GET.get("middlename", "").strip(),
        "user_declarant_id": request.GET.get("user_declarant_id", "").strip(),
    }

    page = int(request.GET.get("page", 1))   # сторінка з URL
    per_page = 100                            # скільки показувати на сторінці

    if request.method == "POST":
        search_type = request.POST.get("search_type")

        if search_type == "name":
            lastname = request.POST.get("lastname", "").strip()
            firstname = request.POST.get("firstname", "").strip()
            middlename = request.POST.get("middlename", "").strip()

            if not (lastname or firstname or middlename):
                return render(request, 'core/pages/declarants_search.html', {
                    "query": query,
                    "empty_name_search": True,  # прапорець
                })

            params = {}
            if lastname:
                params["lastname"] = lastname
            if firstname:
                params["firstname"] = firstname
            if middlename:
                params["middlename"] = middlename

            query_string = urlencode(params)
            return redirect(f"{request.path}?{query_string}")

        elif search_type == "id":
            user_declarant_id = request.POST.get("user_declarant_id", "").strip()
            if not user_declarant_id:
                return render(request, 'core/pages/declarants_search.html', {
                    "query": query,
                    "empty_id_search": True,  # прапорець
                })
            return redirect(f"{request.path}?user_declarant_id={user_declarant_id}")

        # скидаємо на першу сторінку при новому пошуку
        page = 1

    # --- якщо ніяких параметрів немає → пошук не виконуємо ---
    if not (query["lastname"] or query["firstname"] or query["middlename"] or query["user_declarant_id"]):
        return render(request, 'core/pages/declarants_search.html', {
            "results": [],
            "query": query,
            "count": 0,
            "page": 1,
            "total_pages": 0
        })

    results, count = DeclarationsService.find_declarant(
        lastname=query["lastname"],
        firstname=query["firstname"],
        middlename=query["middlename"],
        user_declarant_id=query["user_declarant_id"],
        page=page,
        per_page=per_page
    )

    # рахуємо кількість сторінок
    total_pages = (count + per_page - 1) // per_page

    # обмежуємо номер сторінки (щоб не виліз за межі)
    if page > total_pages:
        page = total_pages if total_pages > 0 else 1

    pagination_query = {k: v for k, v in request.GET.items() if k != "page"}
    pagination_querystring = urlencode(pagination_query)

    # ✅ додаємо списки id користувача
    user_declaration_ids = [str(id) for id in request.user.declarations.values_list("document_id", flat=True)]
    user_declarant_ids = list(request.user.declarant.values_list("user_declarant_id", flat=True))

    return render(request, 'core/pages/declarants_search.html', {
        "results": results,
        "query": query,
        "count": count,
        "page": page,
        "total_pages": total_pages,
        "pagination_querystring": pagination_querystring,
        "user_declaration_ids": user_declaration_ids,
        "user_declarant_ids": user_declarant_ids,
    })

@login_required
def add_declaration_view(request):
    if request.method == "POST":
        raw_id = request.POST.get("document_id")
        user = request.user

        # конвертуємо у UUID
        try:
            document_id = uuid.UUID(raw_id) if raw_id else None
        except (ValueError, TypeError):
            messages.error(request, "Невірний формат document_id.")
            return redirect("add_declaration")

        if not document_id:
            messages.error(request, "Порожній document_id.")
            return redirect("add_declaration")

        # перевіряємо, чи вже є декларація у БД
        declaration = Declaration.objects.filter(document_id=document_id).first()
        if not declaration:
            # завантажуємо JSON з API
            url = f"https://public-api.nazk.gov.ua/v2/documents/{document_id}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            step1 = data.get("data", {}).get("step_1", {}).get("data", {})
            step0 = data.get("data", {}).get("step_0", {}).get("data", {})

            # шукаємо/створюємо декларанта
            declarant, _ = Declarant.objects.get_or_create(
                user_declarant_id=data.get("user_declarant_id"),
                defaults={
                    "lastname": step1.get("lastname", ""),
                    "firstname": step1.get("firstname", ""),
                    "middlename": step1.get("middlename", ""),
                    "work_place": step1.get("workPlace", ""),
                    "work_post": step1.get("workPost", ""),
                    "region": step1.get("region_txt", ""),
                    "actual_country": step1.get("actual_country") or 1,
                    "responsible_position": step1.get("responsiblePosition", ""),
                    "corruption_affected": step1.get("corruptionAffected", ""),
                    "public_person": step1.get("public_person", ""),
                }
            )

            year = step0.get("declaration_year")
            period = step0.get("declaration_period")

            # створюємо декларацію
            declaration = Declaration.objects.create(
                document_id=document_id,
                document_type=data.get("type"),
                declaration_year=int(year) if year else 0,
                declaration_type=data.get("declaration_type") or 1,
                declaration_period=period or "",
                date=datetime.fromisoformat(data.get("date")) if data.get("date") else None,
                declarant=declarant,
            )

        # додаємо зв’язок користувача з декларацією
        user.declarations.add(declaration)
        referer = request.META.get("HTTP_REFERER", reverse("declarants_search"))
        return redirect(referer)


@login_required
def add_declarant_view(request):
    if request.method == "POST":
        user_declarant_id = request.POST.get("user_declarant_id")
        user = request.user

        # перевіряємо, чи вже є декларант у БД
        declarant = Declarant.objects.filter(user_declarant_id=user_declarant_id).first()
        if not declarant:
            # витягаємо всі декларації декларанта з API
            url = f"https://public-api.nazk.gov.ua/v2/documents/list?user_declarant_id={user_declarant_id}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            for decl in data.get("data", []):
                step1 = decl.get("data", {}).get("step_1", {}).get("data", {})
                step0 = decl.get("data", {}).get("step_0", {}).get("data", {})

                if not declarant:
                    declarant = Declarant.objects.create(
                        user_declarant_id=decl.get("user_declarant_id"),
                        lastname=step1.get("lastname", ""),
                        firstname=step1.get("firstname", ""),
                        middlename=step1.get("middlename", ""),
                        work_place=step1.get("workPlace", ""),
                        work_post=step1.get("workPost", ""),
                        region="",
                        actual_country=1,
                        responsible_position="",
                        corruption_affected="",
                        public_person="",
                    )

                # Формуємо коректний звітний період
                year = step0.get("declaration_year")
                period = step0.get("declaration_period")

                # додаємо декларації
                declaration, _ = Declaration.objects.get_or_create(
                    document_id=decl.get("id"),
                    defaults={
                        "document_type": decl.get("type"),
                        "declaration_year": int(year) if year and str(year).isdigit() else 0,
                        "declaration_type": decl.get("declaration_type") or 1,
                        "declaration_period": period or "",
                        "date": datetime.fromisoformat(decl.get("date")) if decl.get("date") else None,
                        "declarant": declarant,
                    }
                )

        # додаємо зв’язок користувача з декларантом
        user.declarant.add(declarant)
        referer = request.META.get("HTTP_REFERER", reverse("declarants_search"))
        return redirect(referer)


@login_required
def declarations_analysis_view(request):
    # Сортуємо декларації за спаданням дати подання
    user_declarations_queryset = (
        UserDeclaration.objects
        .filter(user=request.user)
        .select_related("declaration__declarant")
        .order_by("-added_at")
    )

    declarations_list = []
    for ud in user_declarations_queryset:
        d = ud.declaration
        date_str = d.date.strftime("%d.%m.%Y") if d.date else ""
        declarations_list.append({
            "lastname": d.declarant.lastname,
            "firstname": d.declarant.firstname,
            "middlename": d.declarant.middlename,
            "user_declarant_id": d.declarant.user_declarant_id,
            "document_type_display": d.get_document_type_display(),
            "declaration_type_display": d.get_declaration_type_display(),
            "date": date_str,
            "work_post": d.declarant.work_post,
            "work_place": d.declarant.work_place,
        })

    # Сортуємо декларантів за спаданням id (можна замінити на created_at, якщо є)
    declarants_queryset = request.user.declarant.order_by('-id')

    declarants_list = []
    for dec in declarants_queryset:
        decls = []
        # Декларації кожного декларанта теж сортуємо за спаданням дати
        for d in dec.declarations.order_by('-date', '-id'):
            date_str = d.date.strftime("%d.%m.%Y") if d.date else ""
            decls.append({
                "date": date_str,
                "document_id": str(d.document_id),
                "document_type_display": d.get_document_type_display(),
                "declaration_type_display": d.get_declaration_type_display(),
                "work_post": d.declarant.work_post,
                "work_place": d.declarant.work_place,
            })
        declarants_list.append({
            "lastname": dec.lastname,
            "firstname": dec.firstname,
            "middlename": dec.middlename,
            "user_declarant_id": dec.user_declarant_id,
            "declarations_count": dec.declarations.count(),
            "declarations": decls,
        })

    return render(request, 'core/pages/declarations_analysis_page.html', {
        "declarations_list": declarations_list,
        "declarants_list": declarants_list,
    })



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