from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.a_income.forms import (ConceptForm, catalogCategoryForm,catalogConceptForm,catalogSubcategoryForm,customerForm,personMoralForm,personPhysicalForm,PaymentForm)
from apps.a_income.models import Category, Concept, Customer, Subcategory
from django.db.models.functions import Concat
from django.db.models import Value, CharField

# Create your views here.
@login_required
def income_view(request):
    return render(request, "admin/income/pay/index.html")

@login_required
def customer_new(request, pk):
    if pk == 1:
        form = personPhysicalForm()
    if pk == 2:
        form = personMoralForm()
    return render(request, "admin/income/pay/customer_new.html", {"form": form})

@login_required
def person_type(request):
    return render(request, "admin/income/pay/person_type.html")

@login_required
def customer_save(request):
    form = customerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        #OBTENER el ID del cliente guardado para pasarlo al pago
    return render(request, "admin/income/pay/payment_new.html")

@login_required
def customer_search(request):
    if request.method == "POST":
        name_input = request.POST["name"]
        customers = Customer.objects.annotate(
            nombre_completo=Concat("name",Value(" "),"paternalsurname",Value(" "),"maternalsurname",output_field=CharField(),)
        ).filter(nombre_completo__icontains=name_input)[:10]
        return render(
            request, "admin/income/pay/customers_list.html", {"customersList": customers}
        )
    else:
        return render(request, "admin/income/pay/customer_search.html")

@login_required
def payment_new(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    list_categories = Category.objects.all()
    form = ConceptForm()
    return render(request, "admin/income/pay/payment_new.html",{"customer":customer,"list_categories":list_categories,"form":form})

@login_required
def pay_select_concept(request):
    if request.method == "POST":
        category = request.POST["id_category"]
        print(category)
        #pass
        concepts = Concept.objects.all().filter(category_id = category)
    return render(request, "admin/income/pay/select_concept.html",{"concepts":concepts})

@login_required
def payment_save(request):
    pass


@login_required
def catalog_view(request):
    return render(request, "admin/income/catalog/index.html")

@login_required
def catalogListCategories(request):
    listCategories = Category.objects.all()
    return render(
        request,
        "admin/income/catalog/category/list.html",
        {"listCategories": listCategories},
    )

@login_required
def catalogListSubcategories(request):
    listSubcategories = Subcategory.objects.all()
    return render(
        request,
        "admin/income/catalog/subcategory/list.html",
        {"listSubcategories": listSubcategories},
    )

@login_required
def catalogListConcepts(request):
    listConcepts = Concept.objects.all()
    return render(
        request,
        "admin/income/catalog/concept/list.html",
        {"listConcepts": listConcepts},
    )

@login_required
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

@login_required
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

@login_required
def catalogNewConcept(request):
    if request.method == "POST":
        #print("entro al post")
        form = catalogConceptForm(request.POST)
        if form.is_valid():
            #print("es valido")
            #account_number = request.POST['account_number']
            #category = request.POST['category']
            #subcategory = request.POST['subcategory']
            #name = request.POST['name']
            #bank_account = request.POST['bank_account']
            #print(account_number)
            #print(category)
            #print(subcategory)
            #print(name)
            #print(bank_account)
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/catalog/success.html", {"message": message})
            response["HX-Trigger"] = "updateListConcepts"
            return response
        #print("no es valido")
        return render(request, 'admin/income/catalog/concept/new.html', {'form': form})
    else:
        form = ConceptForm()
        return render(request, "admin/income/catalog/concept/new.html", {"form": form})

@login_required
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

@login_required
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

@login_required
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
