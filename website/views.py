from django.contrib.auth import authenticate,login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm, accountingForm, carouselForm, councilForm, directorForm,dependenceForm

from .models import Post,PostImage,carousel,accounting,position,council,director,dependence
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PostSerializer, accountingSerializer, carouselSerializer,positionSerializer,councilSerializer,directorSerializer,dependenceSerializer
from django.db.models import Q
from rest_framework.response import Response
from .permissions import CustomObjectPermissions
#?Create your views here.
#?view login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('start')
        else:
            messages.error(request,("Ocurrio un error al iniciar sesión, intentelo de nuevo"))
            return redirect('login')
    else:
        return render(request,'authenticate/login.html')
@login_required
def exit(request):
    logout(request)
    return redirect('login')
@login_required(login_url="login")
def start(request):
    return render(request,'pages/start.html')
@login_required
def home(request):
   return render(request, 'pages/welcome.html')
#ListarCabildo
@api_view(["GET"])
def listCouncil(request):
    list = council.objects.all()
    serializer = councilSerializer(list, many=True)
    return Response(serializer.data)
#ListarSlider
@api_view(["GET"])
def listCarousel(request):
    list = carousel.objects.all()
    serializer = carouselSerializer(list, many=True)
    return Response(serializer.data)
#ListarDependencias
@api_view(["GET"])
def listDependences(request):
    dependences = dependence.objects.all()
    serializer = dependenceSerializer(dependences, many=True)
    return Response(serializer.data)
#ListarContabilidad
@api_view(["GET"])
def listAccounting(request):
    posts = accounting.objects.all()
    serializer = accountingSerializer(posts, many=True)
    return Response(serializer.data)
#ListarBlog
@api_view(["GET"])
def listPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
#TODO-PLANTILLAS-CABILDO
@login_required
def list_council(request):
   list = council.objects.all()
   return render(request, 'pages/list_council.html',{'council':list})
@login_required
def newCouncil(request):
    formulario = councilForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request,("Registro creado correctamente"))
        return redirect('list_council')
    return render(request, 'pages/newCouncil.html',{'formulario':formulario})
@login_required
def editCouncil(request, pk):
    mimodelo = get_object_or_404(council, pk=pk)
    if request.method == 'POST':
        form = councilForm(request.POST or None, request.FILES or None, instance=mimodelo)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'El registro ha sido actualizado exitosamente.')
            return redirect('list_council')    
    else:
        form = councilForm(instance=mimodelo)
    return render(request, 'pages/editCouncil.html', {'formulario': form})	
@login_required
def deleteCouncil(request, pk):
    mimodelo = get_object_or_404(council, pk=pk)
    if request.method == 'POST':
        mimodelo.delete()
        messages.success(request, 'El registro ha sido eliminado exitosamente.')
        return redirect('list_council')
    return render(request, 'pages/confirmar_eliminar_council.html', {'mimodelo': mimodelo})
#TODO-PLANTILLAS-DIRECTOR
@login_required
def list_directors(request):
   list = director.objects.all()
   return render(request, 'pages/list_directors.html',{'directors':list})
@login_required
def newDirector(request):
    formulario = directorForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request,("Registro creado correctamente"))
        return redirect('list_directors')
    return render(request, 'pages/newDirector.html',{'formulario':formulario})
@login_required
def editDirector(request, pk):
    mimodelo = get_object_or_404(director, pk=pk)
    if request.method == 'POST':
        form = directorForm(request.POST or None, request.FILES or None, instance=mimodelo)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'El registro ha sido actualizado exitosamente.')
            return redirect('list_directors')    
    else:
        form = directorForm(instance=mimodelo)
    return render(request, 'pages/editDirector.html', {'formulario': form})
@login_required
def deleteDirector(request, pk):
    mimodelo = get_object_or_404(director, pk=pk)
    if request.method == 'POST':
        mimodelo.delete()
        messages.success(request, 'El registro ha sido eliminado exitosamente.')
        return redirect('list_directors')
    return render(request, 'pages/confirmar_eliminar.html', {'mimodelo': mimodelo})
#TODO-PLANTILLAS-DEPENDENCIA
@login_required
def list_dependences(request):
   list = dependence.objects.all()
   return render(request, 'pages/list_dependences.html',{'dependences':list})
@login_required
def newDependence(request):
    formulario = dependenceForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request,("Registro creado correctamente"))
        return redirect('list_dependences')
    return render(request, 'pages/newDependence.html',{'formulario':formulario})
@login_required
def editDependence(request, pk):
    mimodelo = get_object_or_404(dependence, pk=pk)
    if request.method == 'POST':
        form = dependenceForm(request.POST or None, request.FILES or None, instance=mimodelo)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'El registro ha sido actualizado exitosamente.')
            return redirect('list_dependences')    
    else:
        form = dependenceForm(instance=mimodelo)
    return render(request, 'pages/editDependence.html', {'formulario': form})	
@login_required
def deleteDependence(request, pk):
    mimodelo = get_object_or_404(dependence, pk=pk)
    if request.method == 'POST':
        mimodelo.delete()
        messages.success(request, 'El registro ha sido eliminado exitosamente.')
        return redirect('list_dependences')
    return render(request, 'pages/confirmar_eliminar_dependence.html', {'mimodelo': mimodelo})
#TODO-PLANTILLAS-CARRUSEL
@login_required
def list_carousel(request):
   list = carousel.objects.all()
   return render(request, 'pages/list_carousel.html',{'carousel':list})
@login_required
def newCarousel(request):
    formulario = carouselForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request,("Registro creado correctamente"))
        return redirect('list_carousel')
    return render(request, 'pages/newCarousel.html',{'formulario':formulario})
@login_required
def editCarousel(request, pk):
    mimodelo = get_object_or_404(carousel, pk=pk)
    if request.method == 'POST':
        form = carouselForm(request.POST or None, request.FILES or None, instance=mimodelo)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'El registro ha sido actualizado exitosamente.')
            return redirect('list_carousel')    
    else:
        form = carouselForm(instance=mimodelo)
    return render(request, 'pages/editCarousel.html', {'formulario': form})	
@login_required
def deleteCarousel(request, pk):
    mimodelo = get_object_or_404(carousel, pk=pk)
    if request.method == 'POST':
        mimodelo.delete()
        messages.success(request, 'El registro ha sido eliminado exitosamente.')
        return redirect('list_carousel')
    return render(request, 'pages/confirmar_eliminar_carousel.html', {'mimodelo': mimodelo})
#TODO-PLANTILLAS-TRANSPARENCIA
@login_required
def list_accounting(request):
   list = accounting.objects.all()
   return render(request, 'pages/list_accounting.html',{'accounting':list})
@login_required
def newAccounting(request):
    formulario = accountingForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request,("Registro creado correctamente"))
        return redirect('list_accounting')
    return render(request, 'pages/newAccounting.html',{'formulario':formulario})
@login_required
def editAccounting(request, pk):
    mimodelo = get_object_or_404(accounting, pk=pk)
    if request.method == 'POST':
        form = accountingForm(request.POST or None, request.FILES or None, instance=mimodelo)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'El registro ha sido actualizado exitosamente.')
            return redirect('list_accounting')    
    else:
        form = accountingForm(instance=mimodelo)
    return render(request, 'pages/editAccounting.html', {'formulario': form})
@login_required	
def deleteAccounting(request, pk):
    mimodelo = get_object_or_404(accounting, pk=pk)
    if request.method == 'POST':
        mimodelo.delete()
        messages.success(request, 'El registro ha sido eliminado exitosamente.')
        return redirect('list_accounting')
    return render(request, 'pages/confirmar_eliminar_accounting.html', {'mimodelo': mimodelo})
#TODO-PLANTILLAS-POST
@login_required
def list_posts(request):
   list = Post.objects.all()
   return render(request, 'pages/list_posts.html',{'posts':list})
@login_required
def newPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)    
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for image in images:
                    PostImage.objects.create(post=post, image=image)
            messages.success(request,("Registro creado correctamente"))
            return redirect('list_posts')  
        else:
            messages.error(request,("No se creo"))
    else:
        formulario = PostForm()
        return render(request, 'pages/newPost.html',{'formulario':formulario})  
@login_required      
def editPost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)       
        if form.is_valid():
            post.save()
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for image in images:
                    PostImage.objects.create(post=post, image=image)
            messages.success(request,("Registro creado correctamente"))
            return redirect('list_posts')  
        else:
            messages.error(request,("No se creo"))
    else:
        form = PostForm(instance=post)
    return render(request, 'pages/editPost.html', {'formulario': form})	
@login_required
def deletePost(request, pk):
    mimodelo = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        mimodelo.delete()
        messages.success(request, 'El registro ha sido eliminado exitosamente.')
        return redirect('list_posts')
    return render(request, 'pages/confirmar_eliminar_post.html', {'mimodelo': mimodelo})






class CreatePostView(APIView):
    #TODO-Requiere permiso
    permission_classes = [CustomObjectPermissions]    
    def post(self, request, *args, **kwargs):
        # Crear el post
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            # Procesar las imágenes
            images = request.FILES.getlist('images')
            for image in images:
                PostImage.objects.create(post=post, image=image)
            return Response({'message': 'Post creado con éxito'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class carouselListCreateView(generics.ListCreateAPIView):
    queryset = carousel.objects.all()
    serializer_class = carouselSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

class carouselUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = carousel.objects.all()
    serializer_class = carouselSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

class accountingListCreateView(generics.ListCreateAPIView):
    queryset = accounting.objects.all()
    serializer_class = accountingSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

class UserDetail(APIView):
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]
    def get(self, request):
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Agrega otros campos si los necesitas
        }
        return Response(user_data)

class PositionsListCreateView(generics.ListCreateAPIView):
    queryset = position.objects.all()
    serializer_class = positionSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]    

class CouncilListCreateView(generics.ListCreateAPIView):
    queryset = council.objects.all()
    serializer_class = councilSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

class CouncilUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = council.objects.all()
    serializer_class = councilSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

class DirectorsListCreateView(generics.ListCreateAPIView):
    queryset = director.objects.all()
    serializer_class = directorSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

class DirectorsUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = director.objects.all()
    serializer_class = directorSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

class DependencesListCreateView(generics.ListCreateAPIView):
    queryset = dependence.objects.all()
    serializer_class = dependenceSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

class DependencesUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = dependence.objects.all()
    serializer_class = dependenceSerializer
    #TODO-Requiere permiso    
    permission_classes = [CustomObjectPermissions]

