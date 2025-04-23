from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    DocumentTransparencyForm,
    FormAccountingCategory,
    FormAccountingDocument,
    FormAccountingSubcategory,
    PostForm,
    accountingForm,
    carouselForm,
    councilForm,
    directorForm,
    dependenceForm,
    documentForm,
    gazetteForm,
    infogroupForm,
    infosubgroupForm,
    obligationDocumentForm,
    obligationForm,
)

from .models import (
    CategoryTransparency,
    DependenceTransparency,
    Obligation,
    ObligationDocument,
    Post,
    PostImage,
    Transparency,
    carousel,
    accounting,
    document,
    gazette,
    infoGroup,
    infoSubgroup,
    position,
    council,
    director,
    dependence,
)
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    CategoryTransparencySerializer,
    GrupoSerializer,
    ObligationDocumentSerializer,
    ObligationSerializer,
    PostSerializer,
    TransparencySerializer,
    YearSerializer,
    accountingSerializer,
    carouselSerializer,
    gazetteSerializer,
    infoGroupSerializer,
    infoSubgroupSerializer,
    positionSerializer,
    councilSerializer,
    directorSerializer,
    dependenceSerializer,
)
from rest_framework.response import Response
from .permissions import CustomObjectPermissions

#from django.http import JsonResponse
#from django.db.models import Q
#from django.contrib.auth.decorators import permission_required
#from django.template.loader import render_to_string
#from django.conf import settings
#import os
#from django.http import FileResponse

# ?Create your views here.


# ?view login
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("start")
        else:
            messages.error(
                request, ("Ocurrio un error al iniciar sesión, intentelo de nuevo")
            )
            return redirect("login")
    else:
        return render(request, "authenticate/login.html")


@login_required
def exit(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def start(request):
    return render(request, "pages/start.html")


@login_required
def home(request):
    return render(request, "pages/welcome.html")


# ListarCabildo
@api_view(["GET"])
def listCouncil(request):
    list = council.objects.all()
    serializer = councilSerializer(list, many=True)
    return Response(serializer.data)


# ListarSlider
@api_view(["GET"])
def listCarousel(request):
    list = carousel.objects.all()
    serializer = carouselSerializer(list, many=True)
    return Response(serializer.data)


# ListarDependencias
@api_view(["GET"])
def PublicListDependences(request):
    dependences = dependence.objects.all()
    serializer = dependenceSerializer(dependences, many=True)
    return Response(serializer.data)


# SMAPAE
@api_view(["GET"])
def listYearsSMAPAE(request):
    years = (
        accounting.objects.values_list("year", flat=True).distinct().order_by("year")
    )
    data = [{"year": year} for year in years]
    serializer = YearSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)


@api_view(["GET"])
def listCategoriesSMAPAE(request):
    if request.method == "GET":
        list = infoGroup.objects.all()
        serializer = infoGroupSerializer(list, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def listSubcategoriesSMAPAE(request, pk):
    if request.method == "GET":
        list = infoSubgroup.objects.filter(group_id=pk)
        serializer = infoSubgroupSerializer(list, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def listDocumentsSMAPAE(request, pk, year):
    if request.method == "GET":
        list = accounting.objects.filter(subgroup_id=pk, year=year)
        serializer = accountingSerializer(list, many=True)
        return Response(serializer.data)


# ListarContabilidad
@api_view(["GET"])
def listAccounting(request):
    # posts = accounting.objects.all()
    # serializer = accountingSerializer(posts, many=True)
    # return Response(serializer.data)
    grupos = infoGroup.objects.prefetch_related(
        "subgrupos__documentos"
    )  # Optimización de consultas
    serializer = GrupoSerializer(grupos, many=True)
    return Response(serializer.data)


# ListarGaceta
@api_view(["GET"])
def listGazette(request):
    # posts = gazette.objects.all()
    # serializer = gazetteSerializer(posts, many=True)
    # return Response(serializer.data)
    if request.method == "GET":
        # print("entre al method")
        if "year" in request.GET:
            year_select = request.GET["year"]
            if year_select == "0":
                list = gazette.objects.all()
            else:
                list = gazette.objects.filter(year=year_select).order_by("month")
        else:
            list = gazette.objects.all().order_by("month")

        serializer = gazetteSerializer(list, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def listYears(request):
    years = gazette.objects.values_list("year", flat=True).distinct().order_by("year")
    data = [{"year": year} for year in years]
    serializer = YearSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)


# ListarBlog
@api_view(["GET"])
def listPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def listCategoryTransparency(request):
    categories = CategoryTransparency.objects.all()
    serializer = CategoryTransparencySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def listDocumentsTransparency(request, category, dependence):
    documents = Transparency.objects.filter(
        category_id=category, dependence_id=dependence
    )
    serializer = TransparencySerializer(documents, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def listCommonObligations(request):
    obligations = Obligation.objects.all()
    serializer = ObligationSerializer(obligations, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def listCommonObligationsDocuments(request, pk):
    documents = ObligationDocument.objects.filter(obligation_id=pk)
    serializer = ObligationDocumentSerializer(documents, many=True)
    return Response(serializer.data)


# TODO-PLANTILLAS-CABILDO
@login_required
def list_council(request):
    list = council.objects.all()
    return render(request, "pages/list_council.html", {"council": list})


@login_required
def newCouncil(request):
    formulario = councilForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, ("Registro creado correctamente"))
        return redirect("list_council")
    return render(request, "pages/newCouncil.html", {"formulario": formulario})


@login_required
def editCouncil(request, pk):
    mimodelo = get_object_or_404(council, pk=pk)
    if request.method == "POST":
        form = councilForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, "El registro ha sido actualizado exitosamente.")
            return redirect("list_council")
    else:
        form = councilForm(instance=mimodelo)
    return render(request, "pages/editCouncil.html", {"formulario": form})


@login_required
def deleteCouncil(request, pk):
    mimodelo = get_object_or_404(council, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_council")
    return render(
        request, "pages/confirmar_eliminar_council.html", {"mimodelo": mimodelo}
    )


# TODO-PLANTILLAS-DIRECTOR
@login_required
def list_directors(request):
    directors = director.objects.all()
    return render(request, "dependences/partials/directors_list.html", {"directors": directors})

@login_required
def new_director(request):
    formulario = directorForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        #formulario.save()
        #messages.success(request, ("Registro creado correctamente"))
        #return redirect("list_directors")
        formulario.save()
        message = "Registro realizado correctamente"
        response = render(request, "dependences/success.html", {"message": message})
        response["HX-Trigger"] = "updateListDirectors"
        return response    
    return render(request, "dependences/partials/director_new.html", {"formulario": formulario})


@login_required
def edit_director(request, pk):
    mimodelo = get_object_or_404(director, pk=pk)
    if request.method == "POST":
        form = directorForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "dependences/success.html", {"message": message})
            response["HX-Trigger"] = "updateListDirectors"
            return response  
    else:
        form = directorForm(instance=mimodelo)
    return render(request, "dependences/partials/director_edit.html", {"formulario": form, "model":mimodelo})


@login_required
def deleteDirector(request, pk):
    mimodelo = get_object_or_404(director, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_directors")
    return render(request, "pages/confirmar_eliminar.html", {"mimodelo": mimodelo})

# * * TEMPLATE DEPENDENCES
# TODO-PLANTILLA-DEPENDENCIAS
@login_required
def dependences_admin(request):
    return render(request, "dependences/index.html")

@login_required
def list_dependences(request):
    list = dependence.objects.all()
    return render(request, "dependences/partials/dependences_list.html", {"dependences": list})


@login_required
def new_dependence(request):
    formulario = dependenceForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        #formulario.save()
        #messages.success(request, ("Registro creado correctamente"))
        #return redirect("list_dependences")
        formulario.save()
        message = "Registro realizado correctamente"
        response = render(request, "dependences/success.html", {"message": message})
        response["HX-Trigger"] = "updateListDependences"
        return response
    return render(request, "dependences/partials/dependence_new.html", {"formulario": formulario})


@login_required
def edit_dependence(request, pk):
    mimodelo = get_object_or_404(dependence, pk=pk)
    if request.method == "POST":
        form = dependenceForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "dependences/success.html", {"message": message})
            response["HX-Trigger"] = "updateListDependences"
            return response
    else:
        form = dependenceForm(instance=mimodelo)
    return render(request, "dependences/partials/dependence_edit.html", {"formulario": form, "model":mimodelo})


@login_required
def deleteDependence(request, pk):
    mimodelo = get_object_or_404(dependence, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_dependences")
    return render(
        request, "pages/confirmar_eliminar_dependence.html", {"mimodelo": mimodelo}
    )


# TODO-PLANTILLAS-CARRUSEL
@login_required
def carousel_admin(request):
    list = carousel.objects.all()
    return render(request, "carousel/index.html", {"list": list})


@login_required
def list_carousel(request):
    list = carousel.objects.all()
    # return render(request, "pages/list_carousel.html", {"carousel": list})
    return render(request, "carousel/partials/list.html", {"list": list})


@login_required
def newCarousel(request):
    form = carouselForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            # return HttpResponse(status=204,headers={'HX-Trigger':'updateList'})
            message = "Registro realizado correctamente"
            form = carouselForm()
            return render(
                request,
                "carousel/partials/new.html",
                {"form": form, "message": message},
            )
            # Enviar un mensaje de éxito y desencadenar actualización
            # return JsonResponse({'status':'success','message':'Registro creado exitosamente'},status=200)
            # Enviar errores de validación
    return render(request, "carousel/partials/new.html", {"form": form})


@login_required
def editCarousel(request, pk):
    model = get_object_or_404(carousel, pk=pk)
    if request.method == "POST":
        form = carouselForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid() and request.POST:
            form.save()
            message = "Registro realizado correctamente"
            form = carouselForm()
            return render(
                request,
                "carousel/partials/new.html",
                {"form": form, "message": message},
            )
    else:
        form = carouselForm(instance=model)
    return render(
        request, "carousel/partials/edit.html", {"form": form, "model": model}
    )


@login_required
def deleteCarousel(request, pk):
    model = get_object_or_404(carousel, pk=pk)
    if request.method == "POST":
        model.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_carousel")
    return render(
        request,
        "carousel/partials/delete.html",
        {"model": model},
        # request, "pages/confirmar_eliminar_carousel.html", {"model": model}
    )


def listInfoGroup(request):
    list = infoGroup.objects.all()
    return render(request, "pages/listInfoGroup.html", {"grupos": list})


def newInfoGroup(request):
    if request.method == "POST":
        # print(request.POST["name"])
        formulario = infogroupForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
            formulario.save()
            groups = infoGroup.objects.all()
            return render(request, "accounting/groups.html", {"groups": groups})
    else:
        return redirect("error")


def editInfoGroup(request, pk):
    group = get_object_or_404(infoGroup, pk=pk)
    if request.method == "POST":
        group.name = request.POST["name"]
        group.name = request.POST.get("name", "").strip()

        if not group.name:
            return render(
                request, "accounting/partials/edit_row_group.html", {"group": group}
            )
        group.save()
        group = infoGroup.objects.get(pk=pk)
        return render(
            request, "accounting/partials/select_row_group.html", {"group": group}
        )

    return render(request, "accounting/partials/edit_row_group.html", {"group": group})


def selectInfoGroup(request, pk):
    group = infoGroup.objects.get(pk=pk)
    return render(
        request, "accounting/partials/select_row_group.html", {"group": group}
    )


def deleteInfoGroup(request, pk):
    group = infoGroup.objects.get(pk=pk)
    group.delete()
    return HttpResponse("")


def listInfoSubgroup(request):
    grupo_id = request.POST["group"]
    list = infoSubgroup.objects.filter(group_id=grupo_id)
    return render(
        request,
        "admin/transparency/SMAPAE/accounting/document/listSubcategory.html",
        {"subgroups": list},
        # request, "accounting/partials/SelectSubgroup.html", {"subgroups": list}
    )


def newInfoSubgroup(request):
    if request.method == "POST":
        formulario = infosubgroupForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
            formulario.save()
            subgroups = infoSubgroup.objects.all()
            return render(
                request, "accounting/subgroups.html", {"subgroups": subgroups}
            )
    else:
        return redirect("error")


def editInfoSubgroup(request, pk):
    subgroup = get_object_or_404(infoSubgroup, pk=pk)
    if request.method == "POST":
        subgroup.name = request.POST["name"]
        subgroup.group_id = request.POST["group"]
        subgroup.name = request.POST.get("name", "").strip()
        subgroup.group_id = request.POST.get("group", "").strip()

        if not subgroup.name or not subgroup.group_id:
            groups = infoGroup.objects.all()
            return render(
                request,
                "accounting/partials/edit_row_subgroup.html",
                {"subgroup": subgroup, "groups": groups},
            )

        subgroup.save()
        subgroup = infoSubgroup.objects.get(pk=pk)
        return render(
            request,
            "accounting/partials/select_row_subgroup.html",
            {"subgroup": subgroup},
        )
    groups = infoGroup.objects.all()
    return render(
        request,
        "accounting/partials/edit_row_subgroup.html",
        {"subgroup": subgroup, "groups": groups},
    )


def deleteInfoSubgroup(request, pk):
    subgroup = infoSubgroup.objects.get(pk=pk)
    subgroup.delete()
    return HttpResponse("")


def selectInfoSubgroup(request, pk):
    pass


# TODO-PLANTILLAS-TRANSPARENCIA
@login_required
def list_accounting(request):
    list = accounting.objects.all()
    groups = infoGroup.objects.all()
    subgroups = infoSubgroup.objects.all()

    return render(
        request,
        "accounting/list.html",
        {"list": list, "groups": groups, "subgroups": subgroups},
    )


def listAllDocuments(request):
    list = accounting.objects.all()
    return render(request, "accounting/documents.html", {"list": list})


@login_required
def newAccounting(request):
    formulario = accountingForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, ("Registro creado correctamente"))
        return redirect("listAllDocuments")
    groups = infoGroup.objects.all()

    return render(
        request,
        "accounting/new.html",
        {"form": formulario, "grupos": groups},
    )


@login_required
def editAccounting(request, pk):
    mimodelo = get_object_or_404(accounting, pk=pk)
    if request.method == "POST":
        form = accountingForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, "El registro ha sido actualizado exitosamente.")
            return redirect("listAllDocuments")
    else:
        form = accountingForm(instance=mimodelo)
        # subgrupos = infoSubgroup.objects.all()
        grupos = infoGroup.objects.all()
    return render(
        request,
        "accounting/edit.html",
        {
            "form": form,
            "grupos": grupos,
        },
    )


@login_required
def deleteAccounting(request, pk):
    model = get_object_or_404(accounting, pk=pk)
    if request.method == "POST":
        model.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("listAllDocuments")
    return render(request, "accounting/delete.html", {"model": model})


# TODO-PLANTILLAS-GACETA
@login_required
def gazette_admin(request):
    return render(request, "gazette/index.html")


@login_required
def list_gazette(request):
    list = gazette.objects.all()
    return render(request,"gazette/list.html",{"list":list})


@login_required
def newGazette(request):
    form = gazetteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        message = "Registro realizado correctamente"
        response = render(request, "gazette/success.html", {"message": message})
        response["HX-Trigger"] = "updateListGazette"
        return response        
        #form.save()
        #message = "Registro realizado correctamente"
        #form = gazetteForm()
        #return render(request, "gazette/partials/new.html", {"form": form, "message": message})
        # messages.success(request, ("Registro creado correctamente"))
        # return redirect("list_gazette")
    return render(request, "gazette/partials/new.html", {"form": form})


@login_required
def editGazette(request, pk):
    model = get_object_or_404(gazette, pk=pk)
    if request.method == "POST":
        form = gazetteForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid() and request.POST:
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "gazette/success.html", {"message": message})
            response["HX-Trigger"] = "updateListGazette"
            return response               
            #message = "Registro realizado correctamente"
            #form = gazetteForm()
            #return render(request,"gazette/partials/edit.html",{"form": form, "model": model, "message": message},)
    else:
        form = gazetteForm(instance=model)
    return render(request, "gazette/partials/edit.html", {"form": form, "model": model})


@login_required
def deleteGazette(request, pk):
    model = get_object_or_404(gazette, pk=pk)
    if request.method == "POST":
        model.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_gazette")
    return render(request, "gazette/partials/delete.html", {"model": model})


# TODO-PLANTILLAS-DOCUMENTOS
@login_required
def documents_admin(request):
    return render(request, "documents/index.html")


@login_required
def list_document(request):
    list = document.objects.all()
    return render(request, "documents/partials/list.html", {"list": list})


@login_required
def newDocument(request):
    if request.method == "POST":
        form = documentForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            form = documentForm()
            return render(
                request, "documents/partials/success.html", {"message": message}
            )
        # messages.success(request, ("Registro creado correctamente"))
        # return redirect("list_document")
    else:
        form = documentForm()
    return render(request, "documents/partials/new.html", {"form": form})


@login_required
def editDocument(request, pk):
    model = get_object_or_404(document, pk=pk)
    if request.method == "POST":
        form = documentForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid() and request.POST:
            form.save()
            message = "Registro realizado correctamente"
            form = documentForm()
            return render(
                request,
                "documents/partials/edit.html",
                {"form": form, "model": model, "message": message},
            )
    else:
        form = documentForm(instance=model)
    return render(
        request, "documents/partials/edit.html", {"form": form, "model": model}
    )


def detailDocument(request, pk):
    model = get_object_or_404(document, pk=pk)
    # pdf_url = os.path.join(settings.MEDIA_URL, model.document)
    return render(request, "documents/partials/detail.html", {"model": model})


def verDocument(request, pk):
    model = get_object_or_404(document, pk=pk)
    return render(request, "documents/partials/ver.html", {"model": model})


@login_required
def deleteDocument(request, pk):
    model = get_object_or_404(document, pk=pk)
    if request.method == "POST":
        model.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_document")
    return render(request, "documents/partials/delete.html", {"model": model})


# TODO-PLANTILLAS-POST
@login_required
def list_posts(request):
    list = Post.objects.all()
    return render(request, "pages/list_posts.html", {"posts": list})


@login_required
def newPost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if "images" in request.FILES:
                images = request.FILES.getlist("images")
                for image in images:
                    PostImage.objects.create(post=post, image=image)
            messages.success(request, ("Registro creado correctamente"))
            return redirect("list_posts")
        else:
            messages.error(request, ("No se creo"))
    else:
        formulario = PostForm()
        return render(request, "pages/newPost.html", {"formulario": formulario})


@login_required
def editPost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post.save()
            if "images" in request.FILES:
                images = request.FILES.getlist("images")
                for image in images:
                    PostImage.objects.create(post=post, image=image)
            messages.success(request, ("Registro creado correctamente"))
            return redirect("list_posts")
        else:
            messages.error(request, ("No se creo"))
    else:
        form = PostForm(instance=post)
    return render(request, "pages/editPost.html", {"formulario": form})


@login_required
def deletePost(request, pk):
    mimodelo = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_posts")
    return render(request, "pages/confirmar_eliminar_post.html", {"mimodelo": mimodelo})


@login_required
def transparency(request):
    dependences = DependenceTransparency.objects.all()
    categories = CategoryTransparency.objects.all()
    return render(
        request,
        "admin/transparency/index.html",
        {"dependences": dependences, "categories": categories},
    )


def newDocumentTransparency(request):
    if request.method == "POST":
        form = DocumentTransparencyForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro guardado éxitosamente"
            return render(
                request, "admin/procedures/success.html", {"message": message}
            )
    else:
        form = DocumentTransparencyForm(initial={"user": request.user})
        return render(request, "admin/transparency/new.html", {"form": form})


def listDocumenTransparency(request):
    if request.method == "POST":
        dependence = request.POST["dependence"]
        category = request.POST["category"]
        list_docs = Transparency.objects.filter(
            dependence_id=dependence, category_id=category
        )
    else:
        list_docs = Transparency.objects.all()
    return render(request, "admin/transparency/list.html", {"list": list_docs})


def deleteDocumentTransparency(request, pk):
    model = get_object_or_404(Transparency, pk=pk)
    if request.method == "DELETE":
        model.delete()
    return HttpResponse("")


@login_required
def obligation(request):
    return render(request, "admin/obligation/index.html")


def newObligation(request):
    if request.method == "POST":
        form = obligationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro guardado éxitosamente"
            return render(
                request, "admin/obligation/success.html", {"message": message}
            )
    else:
        form = obligationForm()
        return render(request, "admin/obligation/newObligation.html", {"form": form})


def listObligations(request):
    obligations = Obligation.objects.all()
    return render(
        request, "admin/obligation/listObligations.html", {"obligations": obligations}
    )


def newObligationDocument(request):
    if request.method == "POST":
        form = obligationDocumentForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro guardado éxitosamente"
            return render(
                request, "admin/obligation/success.html", {"message": message}
            )
    else:
        form = obligationDocumentForm()
        return render(request, "admin/obligation/newDocument.html", {"form": form})


def listObligationsDocuments(request):
    listDocuments = ObligationDocument.objects.all()
    return render(
        request, "admin/obligation/listDocuments.html", {"listDocuments": listDocuments}
    )


def deleteObligationDocument(request, pk):
    model = get_object_or_404(ObligationDocument, pk=pk)
    if request.method == "DELETE":
        model.delete()
    return HttpResponse("")


@login_required
def Accounting(request):
    return render(request, "admin/transparency/SMAPAE/accounting/index.html")


def AccountingNewCategory(request):
    if request.method == "POST":
        form = FormAccountingCategory(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request,
                "admin/transparency/SMAPAE/accounting/success.html",
                {"message": message},
            )
            response["HX-Trigger"] = "updateListCategories"
            return response
    else:
        form = FormAccountingCategory()
        return render(
            request,
            "admin/transparency/SMAPAE/accounting/category/new.html",
            {"form": form},
        )


def AccountingNewSubcategory(request):
    if request.method == "POST":
        form = FormAccountingSubcategory(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request,
                "admin/transparency/SMAPAE/accounting/success.html",
                {"message": message},
            )
            response["HX-Trigger"] = "updateListSubcategories"
            return response
    else:
        form = FormAccountingSubcategory()
        return render(
            request,
            "admin/transparency/SMAPAE/accounting/subcategory/new.html",
            {"form": form},
        )


def AccountingNewDocument(request):
    if request.method == "POST":
        form = FormAccountingDocument(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request,
                "admin/transparency/SMAPAE/accounting/success.html",
                {"message": message},
            )
            response["HX-Trigger"] = "updateListDocuments"
            return response
    else:
        form = FormAccountingDocument()
        groups = infoGroup.objects.all()
        return render(
            request,
            "admin/transparency/SMAPAE/accounting/document/new.html",
            {"groups": groups, "form": form},
        )


def AccountingListCategories(request):
    listCategories = infoGroup.objects.all()
    return render(
        request,
        "admin/transparency/SMAPAE/accounting/category/list.html",
        {"listCategories": listCategories},
    )


def AccountingListSubcategories(request):
    if request.method == "GET":
        if "category" in request.GET:
            idCategory = int(request.GET["category"])
            if idCategory != 0:
                listSubcategories = infoSubgroup.objects.filter(group_id=idCategory)
            else:
                listSubcategories = infoSubgroup.objects.all()
        else:
            listSubcategories = infoSubgroup.objects.all()
        return render(
            request,
            "admin/transparency/SMAPAE/accounting/subcategory/list.html",
            {"listSubcategories": listSubcategories},
        )


def AccountingListDocuments(request):
    if request.method == "GET":
        listDocuments = accounting.objects.all()
    if request.method == "POST":
        if all(
            key in request.POST and request.POST[key].strip()
            for key in ["category", "subcategory"]
        ):
            idCategroy = int(request.POST["category"])
            idSubcategory = int(request.POST["subcategory"])
            # print(idCategroy)
            # print(idSubcategory)
            if idCategroy != 0 and idSubcategory != 0:
                listDocuments = accounting.objects.filter(
                    group_id=idCategroy, subgroup_id=idSubcategory
                )
            else:
                listDocuments = accounting.objects.filter(
                    group_id__isnull=True, subgroup_id__isnull=True
                )
        else:
            listDocuments = accounting.objects.all()
    return render(
        request,
        "admin/transparency/SMAPAE/accounting/document/list.html",
        {"listDocuments": listDocuments},
    )


def AccountingEditCategory(request, pk):
    model = get_object_or_404(infoGroup, pk=pk)
    if request.method == "POST":
        form = FormAccountingCategory(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request,
                "admin/transparency/SMAPAE/accounting/success.html",
                {"message": message},
            )
            response["HX-Trigger"] = "updateListCategories"
            return response
    else:
        form = FormAccountingCategory(instance=model)
        return render(
            request,
            "admin/transparency/SMAPAE/accounting/category/edit.html",
            {"form": form, "model": model},
        )


def AccountingEditSubcategory(request, pk):
    model = get_object_or_404(infoSubgroup, pk=pk)
    if request.method == "POST":
        form = FormAccountingSubcategory(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request,
                "admin/transparency/SMAPAE/accounting/success.html",
                {"message": message},
            )
            response["HX-Trigger"] = "updateListSubcategories"
            return response
    else:
        form = FormAccountingSubcategory(instance=model)
        return render(
            request,
            "admin/transparency/SMAPAE/accounting/subcategory/edit.html",
            {"form": form, "model": model},
        )


def AccountingEditDocument(request, pk):
    model = get_object_or_404(accounting, pk=pk)
    if request.method == "POST":
        form = FormAccountingDocument(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request,
                "admin/transparency/SMAPAE/accounting/success.html",
                {"message": message},
            )
            response["HX-Trigger"] = "updateListDocuments"
            return response
    else:
        form = FormAccountingDocument(instance=model)
        groups = infoGroup.objects.all()
        return render(
            request,
            "admin/transparency/SMAPAE/accounting/document/edit.html",
            {"groups": groups, "form": form, "model": model},
        )


def AccountingDetailCategory(request, pk):
    category = get_object_or_404(infoGroup, pk=pk)
    subcategories = category.subgrupos.all()
    return render(
        request,
        "admin/transparency/SMAPAE/accounting/category/detail.html",
        {"category": category, "subcategories": subcategories},
    )


def AccountingDetailSubcategory(request, pk):
    subcategory = get_object_or_404(infoSubgroup, pk=pk)
    documents = subcategory.subgrupos.all().order_by("quarter").values()
    return render(
        request,
        "admin/transparency/SMAPAE/accounting/subcategory/detail.html",
        {"subcategory": subcategory, "documents": documents},
    )


def AccountingSelectCategories(request):
    Categories = infoGroup.objects.all()
    return render(
        request,
        "admin/transparency/SMAPAE/accounting/subcategory/selectCategories.html",
        {"Categories": Categories},
    )


def AccountingSelectCategoriesInDocuments(request):
    Categories = infoGroup.objects.all()
    return render(
        request,
        "admin/transparency/SMAPAE/accounting/document/selectCategories.html",
        {"Categories": Categories},
    )


def AccountingSelectSubcategories(request):
    Subcategories = infoSubgroup.objects.all()
    return render(
        request,
        "admin/transparency/SMAPAE/accounting/document/selectSubcategories.html",
        {"Subcategories": Subcategories},
    )


def AccountingDeleteDocument(request, pk):
    model = get_object_or_404(accounting, pk=pk)
    if request.method == "DELETE":
        model.delete()
    return HttpResponse("")


class CreatePostView(APIView):
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]

    def post(self, request, *args, **kwargs):
        # Crear el post
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            # Procesar las imágenes
            images = request.FILES.getlist("images")
            for image in images:
                PostImage.objects.create(post=post, image=image)
            return Response(
                {"message": "Post creado con éxito"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class carouselListCreateView(generics.ListCreateAPIView):
    queryset = carousel.objects.all()
    serializer_class = carouselSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class carouselUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = carousel.objects.all()
    serializer_class = carouselSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class accountingListCreateView(generics.ListCreateAPIView):
    queryset = accounting.objects.all()
    serializer_class = accountingSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class UserDetail(APIView):
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]

    def get(self, request):
        user = request.user
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            # Agrega otros campos si los necesitas
        }
        return Response(user_data)


class PositionsListCreateView(generics.ListCreateAPIView):
    queryset = position.objects.all()
    serializer_class = positionSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class CouncilListCreateView(generics.ListCreateAPIView):
    queryset = council.objects.all()
    serializer_class = councilSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class CouncilUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = council.objects.all()
    serializer_class = councilSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class DirectorsListCreateView(generics.ListCreateAPIView):
    queryset = director.objects.all()
    serializer_class = directorSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class DirectorsUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = director.objects.all()
    serializer_class = directorSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class DependencesListCreateView(generics.ListCreateAPIView):
    queryset = dependence.objects.all()
    serializer_class = dependenceSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]


class DependencesUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = dependence.objects.all()
    serializer_class = dependenceSerializer
    # TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]
