from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
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
)

from .models import (
    Post,
    PostImage,
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
    GrupoSerializer,
    PostSerializer,
    accountingSerializer,
    carouselSerializer,
    gazetteSerializer,
    positionSerializer,
    councilSerializer,
    directorSerializer,
    dependenceSerializer,
)
from django.db.models import Q
from rest_framework.response import Response
from .permissions import CustomObjectPermissions
from django.contrib.auth.decorators import permission_required
from django.template.loader import render_to_string


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
def listDependences(request):
    dependences = dependence.objects.all()
    serializer = dependenceSerializer(dependences, many=True)
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
    posts = gazette.objects.all()
    serializer = gazetteSerializer(posts, many=True)
    return Response(serializer.data)


# ListarBlog
@api_view(["GET"])
def listPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
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
    list = director.objects.all()
    return render(request, "pages/list_directors.html", {"directors": list})


@login_required
def newDirector(request):
    formulario = directorForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, ("Registro creado correctamente"))
        return redirect("list_directors")
    return render(request, "pages/newDirector.html", {"formulario": formulario})


@login_required
def editDirector(request, pk):
    mimodelo = get_object_or_404(director, pk=pk)
    if request.method == "POST":
        form = directorForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, "El registro ha sido actualizado exitosamente.")
            return redirect("list_directors")
    else:
        form = directorForm(instance=mimodelo)
    return render(request, "pages/editDirector.html", {"formulario": form})


@login_required
def deleteDirector(request, pk):
    mimodelo = get_object_or_404(director, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_directors")
    return render(request, "pages/confirmar_eliminar.html", {"mimodelo": mimodelo})


# TODO-PLANTILLAS-DEPENDENCIA
@login_required
def list_dependences(request):
    list = dependence.objects.all()
    return render(request, "pages/list_dependences.html", {"dependences": list})


@login_required
def newDependence(request):
    formulario = dependenceForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, ("Registro creado correctamente"))
        return redirect("list_dependences")
    return render(request, "pages/newDependence.html", {"formulario": formulario})


@login_required
def editDependence(request, pk):
    mimodelo = get_object_or_404(dependence, pk=pk)
    if request.method == "POST":
        form = dependenceForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, "El registro ha sido actualizado exitosamente.")
            return redirect("list_dependences")
    else:
        form = dependenceForm(instance=mimodelo)
    return render(request, "pages/editDependence.html", {"formulario": form})


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
def list_carousel(request):
    list = carousel.objects.all()
    return render(request, "pages/list_carousel.html", {"carousel": list})


@login_required
def newCarousel(request):
    formulario = carouselForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, ("Registro creado correctamente"))
        return redirect("list_carousel")
    return render(request, "pages/newCarousel.html", {"formulario": formulario})


@login_required
def editCarousel(request, pk):
    mimodelo = get_object_or_404(carousel, pk=pk)
    if request.method == "POST":
        form = carouselForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, "El registro ha sido actualizado exitosamente.")
            return redirect("list_carousel")
    else:
        form = carouselForm(instance=mimodelo)
    return render(request, "pages/editCarousel.html", {"formulario": form})


@login_required
def deleteCarousel(request, pk):
    mimodelo = get_object_or_404(carousel, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_carousel")
    return render(
        request, "pages/confirmar_eliminar_carousel.html", {"mimodelo": mimodelo}
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
            return render(request, "pages/groups.html", {"groups": groups})
    else:
        return redirect("error")


def editInfoGroup(request, pk):
    group = get_object_or_404(infoGroup, pk=pk)
    if request.method == "POST":
        group.name = request.POST["name"]
        group.name = request.POST.get("name", "").strip()

        if not group.name:
            return render(
                request, "pages/partials/edit_row_group.html", {"group": group}
            )
        group.save()
        group = infoGroup.objects.get(pk=pk)
        return render(request, "pages/partials/select_row_group.html", {"group": group})

    return render(request, "pages/partials/edit_row_group.html", {"group": group})


def selectInfoGroup(request, pk):
    group = infoGroup.objects.get(pk=pk)
    return render(request, "pages/partials/select_row_group.html", {"group": group})


def deleteInfoGroup(request, pk):
    group = infoGroup.objects.get(pk=pk)
    group.delete()
    return HttpResponse("")


def listInfoSubgroup(request):
    grupo_id = request.POST["grupo"]
    list = infoSubgroup.objects.filter(group_id=grupo_id)
    return render(request, "pages/listInfoSubgroup.html", {"subgrupos": list})


def newInfoSubgroup(request):
    if request.method == "POST":
        formulario = infosubgroupForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
            formulario.save()
            subgroups = infoSubgroup.objects.all()
            return render(request, "pages/subgroups.html", {"subgroups": subgroups})
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
                "pages/partials/edit_row_subgroup.html",
                {"subgroup": subgroup, "groups": groups},
            )

        subgroup.save()
        subgroup = infoSubgroup.objects.get(pk=pk)
        return render(
            request, "pages/partials/select_row_subgroup.html", {"subgroup": subgroup}
        )
    groups = infoGroup.objects.all()
    return render(
        request,
        "pages/partials/edit_row_subgroup.html",
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
        "pages/list_accounting.html",
        {"accounting": list, "groups": groups, "subgroups": subgroups},
    )


@login_required
def newAccounting(request):
    formulario = accountingForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, ("Registro creado correctamente"))
        return redirect("list_accounting")
    groups = infoGroup.objects.all()

    return render(
        request,
        "pages/newAccounting.html",
        {"formulario": formulario, "grupos": groups},
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
            return redirect("list_accounting")
    else:
        form = accountingForm(instance=mimodelo)
        # subgrupos = infoSubgroup.objects.all()
        grupos = infoGroup.objects.all()
    return render(
        request,
        "pages/editAccounting.html",
        {
            "formulario": form,
            "grupos": grupos,
        },
    )


@login_required
def deleteAccounting(request, pk):
    mimodelo = get_object_or_404(accounting, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_accounting")
    return render(
        request, "pages/confirmar_eliminar_accounting.html", {"mimodelo": mimodelo}
    )


# TODO-PLANTILLAS-GACETA
@login_required
def list_gazette(request):
    list = gazette.objects.all()
    return render(request, "pages/list_gazette.html", {"gazette": list})


@login_required
def newGazette(request):
    formulario = gazetteForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, ("Registro creado correctamente"))
        return redirect("list_gazette")
    return render(request, "pages/newGazette.html", {"formulario": formulario})


@login_required
def editGazette(request, pk):
    mimodelo = get_object_or_404(gazette, pk=pk)
    if request.method == "POST":
        form = gazetteForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, "El registro ha sido actualizado exitosamente.")
            return redirect("list_gazette")
    else:
        form = gazetteForm(instance=mimodelo)
    return render(request, "pages/editGazette.html", {"formulario": form})


@login_required
def deleteGazette(request, pk):
    mimodelo = get_object_or_404(gazette, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_gazette")
    return render(
        request, "pages/confirmar_eliminar_gazette.html", {"mimodelo": mimodelo}
    )


# TODO-PLANTILLAS-DOCUMENTOS
@login_required
def list_document(request):
    list = document.objects.all()
    return render(request, "pages/list_document.html", {"documents": list})


@login_required
def newDocument(request):
    formulario = documentForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, ("Registro creado correctamente"))
        return redirect("list_document")
    return render(request, "pages/newDocument.html", {"formulario": formulario})


@login_required
def editDocument(request, pk):
    mimodelo = get_object_or_404(document, pk=pk)
    if request.method == "POST":
        form = documentForm(
            request.POST or None, request.FILES or None, instance=mimodelo
        )
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, "El registro ha sido actualizado exitosamente.")
            return redirect("list_document")
    else:
        form = documentForm(instance=mimodelo)
    return render(request, "pages/editDocument.html", {"formulario": form})


@login_required
def deleteDocument(request, pk):
    mimodelo = get_object_or_404(document, pk=pk)
    if request.method == "POST":
        mimodelo.delete()
        messages.success(request, "El registro ha sido eliminado exitosamente.")
        return redirect("list_document")
    return render(
        request, "pages/confirmar_eliminar_documento.html", {"mimodelo": mimodelo}
    )


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
