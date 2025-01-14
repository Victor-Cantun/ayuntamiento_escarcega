from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import EvidenceProcedureForm, TrackingProcedureForm, commentProcedureForm, deliveryProcedureForm, documentProcedureForm, requestProcedureForm, citizenForm
from .models import DeliveryProcedure, DocumentProcedure, EvidenceProcedure, citizen,RequestProcedure, TrackingProcedure, commentProcedure
from rest_framework.views import APIView
from django.db.models import Count, Q

# Create your views here.
# TODO-PLANTILLAS-GESTIONES
@login_required
def procedures(request):
    return render(request, "admin/procedures/index.html")

def listRequetsProcedures(request):
    if request.method =="POST" and ('start' in request.POST) and ('end' in request.POST):
        
        start_date = request.POST['start']
        end_date = request.POST['end']
        print(start_date)
        print(end_date)

        resultados = RequestProcedure.objects.filter(date__range=[start_date,end_date]).values('procedure_type__name').annotate(
        total_pendientes=Count('id', filter=Q(status='Pendiente')),
        total_autorizadas=Count('id', filter=Q(status='Autorizada')),
        total_entregadas=Count('id', filter=Q(status='Entregada')),
        total_canceladas=Count('id', filter=Q(status='Cancelada')),
        total_solicitudes=Count('id')
        ).order_by('procedure_type__name')
  
        #pending_count = RequestProcedure.objects.filter(status="Pendiente",date__range=[start_date,end_date]).count()
        #authorized_count = RequestProcedure.objects.filter(status="Autorizada",date__range=[start_date,end_date]).count()
        #delivered_count = RequestProcedure.objects.filter(status="Entregada",date__range=[start_date,end_date]).count()
        #canceled_count = RequestProcedure.objects.filter(status="Cancelada",date__range=[start_date,end_date]).count()
        #status_count = RequestProcedure.objects.values('status').annotate(total=Count('status'))
        #total = pending_count + authorized_count + delivered_count + canceled_count
        list = RequestProcedure.objects.filter(date__range=[start_date,end_date])
        return render(request, "admin/procedures/list.html",{
        "list":list,
        #"pendientes":pending_count,
        #"autorizadas":authorized_count,
        #"entregadas":delivered_count,
        #"canceladas":canceled_count,
        #"total":total,
        'resultados': resultados,
        })
    else: 
        list = RequestProcedure.objects.all()     
        resultados = RequestProcedure.objects.filter(date__range=[start_date,end_date]).values('procedure_type__name').annotate(
        total_pendientes=Count('id', filter=Q(status='Pendiente')),
        total_autorizadas=Count('id', filter=Q(status='Autorizada')),
        total_entregadas=Count('id', filter=Q(status='Entregada')),
        total_canceladas=Count('id', filter=Q(status='Cancelada')),
        total_solicitudes=Count('id')
        ).order_by('procedure_type__name')

        #pending_count = RequestProcedure.objects.filter(status="Pendiente",date__range=[start_date,end_date]).count()
        #authorized_count = RequestProcedure.objects.filter(status="Autorizada").count()
        #delivered_count = RequestProcedure.objects.filter(status="Entregada").count()
        #canceled_count = RequestProcedure.objects.filter(status="Cancelada").count()
        #status_count = RequestProcedure.objects.values('status').annotate(total=Count('status'))
        #total = pending_count + authorized_count + delivered_count + canceled_count
    return render(request, "admin/procedures/list.html",{
        "list":list,
        #"pendientes":pending_count,
        #"autorizadas":authorized_count,
        #"entregadas":delivered_count,
        #"canceladas":canceled_count,
        #"total":total,
        'resultados': resultados,
        })

def detailRequestProcedure(request,pk):
    requestProcedure = get_object_or_404(RequestProcedure, pk=pk)
    tracking = requestProcedure.trackingprocedure_set.all().order_by('id')
    #evidences = requestProcedure.images_evidence.all().order_by('id')
    list_comments = commentProcedure.objects.filter(procedure_id=requestProcedure.id)
    list_documents = DocumentProcedure.objects.filter(procedure_id=requestProcedure.id)
    list_evidences = EvidenceProcedure.objects.filter(procedure_id=requestProcedure.id)
    deliveryInfo = DeliveryProcedure.objects.filter(procedure_id=requestProcedure.id)    
    formComment = commentProcedureForm(initial={'procedure': requestProcedure.id,'user': request.user.id })
    formDocument = documentProcedureForm(initial={'procedure': requestProcedure.id,'user': request.user.id })  
    formEvidence = EvidenceProcedureForm(initial={'procedure': requestProcedure.id,'capturer': request.user.id })
    formDelivery = deliveryProcedureForm(initial={'procedure': requestProcedure.id,'user': request.user.id })
    return render(request,"admin/procedures/detailRequestProcedure.html",{
        "procedure":requestProcedure,
        "tracking":tracking,
        "evidences":list_evidences,
        "form":formComment,
        "comments":list_comments,
        "formDocument":formDocument,
        "documents":list_documents,
        "formEvidence":formEvidence,
        "formDelivery":formDelivery,
        "deliveryInfo":deliveryInfo,
        })

def searchCitizen(request):
    return render(request,"admin/procedures/searchCitizen.html")

def newCitizen(request):
    form = citizenForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        new_citizen = form.save()
        #message = "Registro realizado correctamente" 
        # Crear el formulario para la solicitud prellenado
        request_procedure_form = requestProcedureForm(initial={
                'requester': new_citizen,
                'capturer': request.user,
                'current_department':request.user.profile.dependence.id
            })
        return render(request, "admin/procedures/newRequestProcedure.html", {
                "form": request_procedure_form,
                "citizen": new_citizen,
                #"message": message
            })
        #messages.success(request, ("Registro creado correctamente"))
        #return redirect("list_gazette")
    return render(request, "admin/procedures/newCitizen.html", {"form": form})  

def newRequestProcedure(request):
    form = requestProcedureForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        message = "Registro realizado correctamente" 
        form = requestProcedureForm()
        return render(request, "admin/procedures/newRequestProcedure.html", {"form": form,"message":message})
        #messages.success(request, ("Registro creado correctamente"))
        #return redirect("list_gazette")
    return render(request, "admin/procedures/newRequestProcedure.html", {"form": form})

def editRequestProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "POST":
        form = requestProcedureForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid() and request.POST:
            form.save()
            message = "Registro realizado correctamente" 
            form = requestProcedureForm()
            return render(request, "admin/procedures/editRequestProcedure.html", {"form": form,"model":model,"message":message})
    else:
        form = requestProcedureForm(instance=model)
    return render(request, "admin/procedures/editRequestProcedure.html", {"form": form, "model":model})

def deleteRequestProcedure(request,pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "DELETE":
        model.delete()
        return redirect("listRequetsProcedures")
    return render(request, "admin/procedures/deleteRequestProcedure.html", {"model": model})

def newTrackingProcedure(request,pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    form = TrackingProcedureForm(initial={
        'procedure': model,
        'capturer': request.user,
        'to_department':model.current_department        
        }) 
    return render(request, "admin/procedures/newTrackingProcedure.html", {"form": form,"model":model})

def saveTrackingProcedure(request):
    if request.method == 'POST':
        form = TrackingProcedureForm(request.POST or None, request.FILES or None)
        procedure = request.POST['procedure']
        department = request.POST['from_department']
        new_status = request.POST['status']
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            model = get_object_or_404(RequestProcedure, pk=procedure)
            form = TrackingProcedureForm(initial={'procedure': model,'capturer': request.user,'to_department':model.current_department         }) 
            update_current_department = RequestProcedure.objects.filter(id=procedure).update(current_department_id = department,status = new_status)
            return render(request, "admin/procedures/newTrackingProcedure.html", {"form": form,"message":message})
        model = get_object_or_404(RequestProcedure, pk=procedure)
        form = TrackingProcedureForm(initial={
        'procedure': model,
        'capturer': request.user,
        'to_department':model.current_department        
        }) 
        return render(request, "admin/procedures/newTrackingProcedure.html",{"form":form})
        
def showProcedure(request,pk):
    requestProcedure = get_object_or_404(RequestProcedure, pk=pk)
    tracking = requestProcedure.trackingprocedure_set.all().order_by('id')
    evidences = requestProcedure.images_evidence.all().order_by('id')
    print(tracking)
    return render(request, "admin/procedures/timeLine.html",{"procedure":requestProcedure,"tracking":tracking,"evidences":evidences})

def uploadEvidence(request,pk):
    
    if request.method == "POST":
        form = EvidenceProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid() and request.POST:
            post = form.save(commit=False)
            solicitud = request.POST['procedure']
            usuario = request.user.id
            #post.procedure_id = solicitud
            #post.capturer = usuario
            if "images" in request.FILES:
                images = request.FILES.getlist("images")
                for image in images:
                    EvidenceProcedure.objects.create(procedure_id = solicitud, image = image, capturer_id=usuario)
            message = "Registro realizado correctamente" 
            model = get_object_or_404(RequestProcedure, pk=pk)
            form = EvidenceProcedureForm(initial={
        'procedure': model.id,
        'capturer': request.user,      
        })
            return render(request, "admin/procedures/uploadEvidenceProcedure.html", {"form": form,"model":model,"message":message})
    else:
        model = get_object_or_404(RequestProcedure, pk=pk)
        form = EvidenceProcedureForm(initial={
        'procedure': model.id,
        'capturer': request.user,      
        })
    return render(request, "admin/procedures/uploadEvidenceProcedure.html", {"form": form, "model":model})

def addCommentProcedure(request):
    if request.method =='POST':
        procedure = request.POST['procedure']
        #user = request.user.id
        #comment = request.POST['comment']
        #print(procedure)
        #print(user)
        #print(comment)
        form = commentProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            list = commentProcedure.objects.filter(procedure_id=procedure)
            return render(request, "admin/procedures/comments.html",{"comments":list})
        list = commentProcedure.objects.filter(procedure_id=procedure)
        return render(request,"admin/procedures/comments.html",{"comments":list})

def addDocumentProcedure(request):
    procedure = request.POST['procedure']
    user = request.user.id
    #document = request.POST['document']
    document_type = request.POST['document_type']
    print(procedure)
    print(user)
    #print(document)
    print(document_type)
    form = documentProcedureForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        list = DocumentProcedure.objects.filter(procedure_id=procedure)
        return render(request, "admin/procedures/documents.html",{"documents":list})
    list = DocumentProcedure.objects.filter(procedure_id=procedure)
    return render(request,"admin/procedures/documents.html",{"documents":list})

def addEvidenceProcedure(request):
    form = EvidenceProcedureForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(commit=False)
        solicitud = request.POST['procedure']
        usuario = request.user.id
        if "images" in request.FILES:
            images = request.FILES.getlist("images")
            for image in images:
                EvidenceProcedure.objects.create(procedure_id = solicitud, image = image, capturer_id=usuario)
        list = EvidenceProcedure.objects.filter(procedure_id=solicitud)
        return render(request, "admin/procedures/evidences.html",{"evidences":list})
    list = EvidenceProcedure.objects.filter(procedure_id=solicitud)
    return render(request,"admin/procedures/evidences.html",{"evidences":list})    

def addDeliveryProcedure(request):
    if request.method =='POST':
        procedure = request.POST['procedure']
        #user = request.user.id
        #comment = request.POST['comment']
        #print(procedure)
        #print(user)
        #print(comment)
        form = deliveryProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            RequestProcedure.objects.filter(id=procedure).update(status = 'Entregada')
            list = DeliveryProcedure.objects.filter(procedure_id=procedure)
            return render(request, "admin/procedures/delivery_finish.html",{"deliveryInfo":list})
        list = DeliveryProcedure.objects.filter(procedure_id=procedure)
        return render(request,"admin/procedures/delivery_finish.html",{"deliveryInfo":list})