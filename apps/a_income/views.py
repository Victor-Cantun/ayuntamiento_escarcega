from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.a_income.forms import (
    catalogCategoryForm,
    catalogConceptForm,
    catalogSubcategoryForm,
    customerForm,
    personMoralForm,
    personPhysicalForm,
)
from apps.a_income.models import Category, Concept, Customer, Subcategory
from django.db.models.functions import Concat
from django.db.models import Value, CharField


# Create your views here.
@login_required
def income_view(request):
    return render(request, "admin/income/pay/index.html")


def customerSearch(request):
    if request.method == "POST":
        # print("si llego")
        name_input = request.POST["name"]
        customers = Customer.objects.annotate(
            nombre_completo=Concat(
                "name",
                Value(" "),
                "paternalsurname",
                Value(" "),
                "maternalsurname",
                output_field=CharField(),
            )
        ).filter(nombre_completo__icontains=name_input)[:10]
        return render(
            request, "admin/income/pay/customersList.html", {"customersList": customers}
        )
    else:
        return render(request, "admin/income/pay/customerSearch.html")


def personType(request):
    return render(request, "admin/income/pay/personType.html")


def newCustomer(request, pk):
    if pk == 1:
        form = personPhysicalForm()
    if pk == 2:
        form = personMoralForm()
    return render(request, "admin/income/pay/newCustomer.html", {"form": form})


def saveCustomer(request):
    form = customerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    return render(request, "admin/income/pay/newPayment.html")


@login_required
def newPayment(request, pk):
    return render(request, "admin/income/pay/newPayment.html")


@login_required
def catalog_view(request):
    return render(request, "admin/income/catalog/index.html")


def catalogListCategories(request):
    listCategories = Category.objects.all()
    return render(
        request,
        "admin/income/catalog/category/list.html",
        {"listCategories": listCategories},
    )


def catalogListSubcategories(request):
    listSubcategories = Subcategory.objects.all()
    return render(
        request,
        "admin/income/catalog/subcategory/list.html",
        {"listSubcategories": listSubcategories},
    )


def catalogListConcepts(request):
    listConcepts = Concept.objects.all()
    return render(
        request,
        "admin/income/catalog/concept/list.html",
        {"listConcepts": listConcepts},
    )


def catalogNewCategory(request):
    if request.method == "POST":
        form = catalogCategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListCategories"
            return response
    else:
        form = catalogCategoryForm()
        return render(request, "admin/income/catalog/category/new.html", {"form": form})


def catalogNewSubcategory(request):
    if request.method == "POST":
        form = catalogSubcategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListSubcategories"
            return response
    else:
        form = catalogSubcategoryForm()
        return render(
            request, "admin/income/catalog/subcategory/new.html", {"form": form}
        )


def catalogNewConcept(request):
    if request.method == "POST":
        form = catalogConceptForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListConcepts"
            return response
    else:
        form = catalogConceptForm()
        return render(request, "admin/income/catalog/concept/new.html", {"form": form})


def catalogEditCategory(request, pk):
    model = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = catalogCategoryForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListCategories"
            return response
    else:
        form = catalogCategoryForm(instance=model)
    return render(
        request,
        "admin/income/catalog/category/edit.html",
        {"form": form, "model": model},
    )


def catalogEditSubcategory(request, pk):
    model = get_object_or_404(Subcategory, pk=pk)
    if request.method == "POST":
        form = catalogSubcategoryForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListSubcategories"
            return response
    else:
        form = catalogSubcategoryForm(instance=model)
    return render(
        request,
        "admin/income/catalog/subcategory/edit.html",
        {"form": form, "model": model},
    )


def catalogEditConcept(request, pk):
    model = get_object_or_404(Concept, pk=pk)
    if request.method == "POST":
        form = catalogConceptForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListConcepts"
            return response
    else:
        form = catalogConceptForm(instance=model)
    return render(
        request,
        "admin/income/catalog/concept/edit.html",
        {"form": form, "model": model},
    )
