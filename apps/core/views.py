from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import (
    AccountingMomentForm,
    EvidenceProcedureForm,
    TrackingProcedureForm,
    commentProcedureForm,
    deliveryProcedureForm,
    departmentForm,
    dependenceForm,
    directorForm,
    documentProcedureForm,
    requestProcedureForm,
    citizenForm,
    statusProcedureForm,
)
from .models import (
    AccountingMoment,
    DeliveryProcedure,
    DocumentProcedure,
    DocumentTypeProcedure,
    EvidenceProcedure,
    ProcedureType,
    citizen,
    RequestProcedure,
    TrackingProcedure,
    commentProcedure,
    department,
    dependence,
    director,
)
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.db.models import Value, CharField
from django.db.models.functions import Concat


# Create your views here.
# TODO-PLANTILLAS-GESTIONES
@login_required
def cityHall(request):
    return render(request, "admin/cityHall/index.html")


def listDependences(request):
    listDependences = dependence.objects.all()
    return render(
        request,
        "admin/cityHall/dependence/list.html",
        {"listDependences": listDependences},
    )


def listDirectors(request):
    listDirectors = director.objects.all()
    return render(
        request,
        "admin/cityHall/director/list.html",
        {"listDirectors": listDirectors},
    )


def listDepartments(request):
    listDepartments = department.objects.all()
    # print(listDepartments)
    return render(
        request,
        "admin/cityHall/department/list.html",
        {"listDepartments": listDepartments},
    )


def editDependence(request, pk):
    model = get_object_or_404(dependence, pk=pk)
    if request.method == "POST":
        form = dependenceForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/cityHall/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListDependences"
            return response
    else:
        form = dependenceForm(instance=model)
    return render(
        request,
        "admin/cityHall/dependence/edit.html",
        {"form": form, "model": model},
    )


def editDepartment(request, pk):
    model = get_object_or_404(department, pk=pk)
    if request.method == "POST":
        form = departmentForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/cityHall/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListDepartments"
            return response
    else:
        form = departmentForm(instance=model)
    return render(
        request,
        "admin/cityHall/department/edit.html",
        {"form": form, "model": model},
    )


def editDirector(request, pk):
    model = get_object_or_404(director, pk=pk)
    if request.method == "POST":
        form = directorForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/cityHall/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListDirectors"
            return response
    else:
        form = directorForm(instance=model)
    return render(
        request, "admin/cityHall/director/edit.html", {"form": form, "model": model}
    )


def newDirector(request):
    if request.method == "POST":
        form = directorForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/cityHall/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListDirectors"
            return response
    else:
        form = directorForm()
        return render(request, "admin/cityHall/director/new.html", {"form": form})


def newDepartment(request):
    if request.method == "POST":
        form = departmentForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/cityHall/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListDepartments"
            return response
    else:
        form = departmentForm()
        return render(request, "admin/cityHall/department/new.html", {"form": form})


def newDependence(request):
    if request.method == "POST":
        form = dependenceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/cityHall/success.html", {"message": message}
            )
            response["HX-Trigger"] = "updateListDependences"
            return response
    else:
        form = dependenceForm()
        return render(request, "admin/cityHall/dependence/new.html", {"form": form})


def detailDirector(request, pk):
    model_instance = get_object_or_404(director, pk=pk)
    fields = []
    for field in model_instance._meta.fields:
        # Verifica si el campo tiene un método get_<field>_display para opciones (choices)
        display_method = f"get_{field.name}_display"
        if hasattr(model_instance, display_method):
            value = getattr(model_instance, display_method)()
        else:
            value = getattr(model_instance, field.name)
        fields.append(
            {
                "label": field.verbose_name,
                "value": value,
            }
        )
    return render(request, "admin/cityHall/director/detail.html", {"fields": fields})


def detailDependence(request, pk):
    model_instance = get_object_or_404(dependence, pk=pk)
    fields = []
    for field in model_instance._meta.fields:
        # Verifica si el campo tiene un método get_<field>_display para opciones (choices)
        display_method = f"get_{field.name}_display"
        if hasattr(model_instance, display_method):
            value = getattr(model_instance, display_method)()
        else:
            value = getattr(model_instance, field.name)
        fields.append(
            {
                "label": field.verbose_name,
                "value": value,
            }
        )
    return render(request, "admin/cityHall/dependence/detail.html", {"fields": fields})


def detailDepartment(request, pk):
    model_instance = get_object_or_404(department, pk=pk)
    fields = []
    for field in model_instance._meta.fields:
        # Verifica si el campo tiene un método get_<field>_display para opciones (choices)
        display_method = f"get_{field.name}_display"
        if hasattr(model_instance, display_method):
            value = getattr(model_instance, display_method)()
        else:
            value = getattr(model_instance, field.name)
        fields.append(
            {
                "label": field.verbose_name,
                "value": value,
            }
        )
    return render(request, "admin/cityHall/department/detail.html", {"fields": fields})


@login_required
def procedures(request):
    all_departments = department.objects.all()
    return render(
        request, "admin/procedures/index.html", {"departments": all_departments}
    )


def listRequetsProcedures(request):
    if request.method == "POST":
        if all(
            key in request.POST and request.POST[key].strip()
            for key in ["start", "end", "department"]
        ):

            start_date = request.POST["start"]
            end_date = request.POST["end"]
            department = request.POST["department"]
            user = request.user.id

            filtros = Q(date__range=[start_date, end_date])
            if department != "0":
                filtros &= Q(trackingprocedure__from_department=department) | Q(
                    capturer_id=user
                )

            resultados = (
                RequestProcedure.objects.filter(filtros)
                .values("procedure_type__name")
                .annotate(
                    total_pendientes=Count("id", filter=Q(status="Pendiente")),
                    total_autorizadas=Count("id", filter=Q(status="Autorizada")),
                    total_entregadas=Count("id", filter=Q(status="Entregada")),
                    total_canceladas=Count("id", filter=Q(status="Cancelada")),
                    total_solicitudes=Count("id"),
                )
                .order_by("procedure_type__name")
                .distinct()
            )

            # Calcular los totales generales
            totales_generales = {
                "total_pendientes": sum(
                    item["total_pendientes"] for item in resultados
                ),
                "total_autorizadas": sum(
                    item["total_autorizadas"] for item in resultados
                ),
                "total_entregadas": sum(
                    item["total_entregadas"] for item in resultados
                ),
                "total_canceladas": sum(
                    item["total_canceladas"] for item in resultados
                ),
                "total_solicitudes": sum(
                    item["total_solicitudes"] for item in resultados
                ),
            }

            list = RequestProcedure.objects.filter(filtros).distinct()
            return render(
                request,
                "admin/procedures/list.html",
                {
                    "list": list,
                    "resultados": resultados,
                    "totales_generales": totales_generales,
                },
            )
        pass
    pass


def detailRequestProcedure(request, pk):
    requestProcedure = get_object_or_404(RequestProcedure, pk=pk)
    tracking = requestProcedure.trackingprocedure_set.all().order_by("id")
    # evidences = requestProcedure.images_evidence.all().order_by('id')
    list_comments = commentProcedure.objects.filter(procedure_id=requestProcedure.id)
    list_documents = DocumentProcedure.objects.filter(procedure_id=requestProcedure.id)
    list_evidences = EvidenceProcedure.objects.filter(procedure_id=requestProcedure.id)
    deliveryInfo = DeliveryProcedure.objects.filter(procedure_id=requestProcedure.id)
    formComment = commentProcedureForm(
        initial={"procedure": requestProcedure.id, "user": request.user.id}
    )
    document_type = DocumentTypeProcedure.objects.all()
    formDocument = documentProcedureForm(
        initial={"procedure": requestProcedure.id, "user": request.user.id}
    )
    formEvidence = EvidenceProcedureForm(
        initial={"procedure": requestProcedure.id, "capturer": request.user.id}
    )
    formDelivery = deliveryProcedureForm(
        initial={"procedure": requestProcedure.id, "user": request.user.id}
    )
    timeline = TrackingProcedure.objects.filter(procedure_id=requestProcedure.id)
    try:
        momento_contable = AccountingMoment.objects.get(
            procedure_id=requestProcedure.id
        )
        formAccountingMoment = AccountingMomentForm(instance=momento_contable)
    except AccountingMoment.DoesNotExist:
        formAccountingMoment = AccountingMomentForm(
            initial={"procedure": requestProcedure.id, "user": request.user.id}
        )
    # if comprometido:
    # else:

    return render(
        request,
        "admin/procedures/detailRequestProcedure.html",
        {
            "procedure": requestProcedure,
            "tracking": tracking,
            "evidences": list_evidences,
            "form": formComment,
            "comments": list_comments,
            "formDocument": formDocument,
            "documents": list_documents,
            "formEvidence": formEvidence,
            "formDelivery": formDelivery,
            "deliveryInfo": deliveryInfo,
            "timeline": timeline,
            "types_documents": document_type,
            "formAccountingMoment": formAccountingMoment,
        },
    )


def searchCitizen(request):
    if request.method == "POST":
        # print("si llego")
        name_input = request.POST["name"]
        personas = citizen.objects.annotate(
            nombre_completo=Concat(
                "name",
                Value(" "),
                "last_name",
                Value(" "),
                "second_name",
                output_field=CharField(),
            )
        ).filter(nombre_completo__icontains=name_input)[:10]
        # palabras = name_input.split()
        # filtros = Q()
        # for palabra in palabras:
        #    filtros |= Q(name__icontains=palabra) | Q(last_name__icontains=palabra) | Q(second_name__icontains=palabra)
        # list_citizen = citizen.objects.filter(filtros)
        return render(
            request, "admin/procedures/listCitizen.html", {"list_citizen": personas}
        )
    else:
        return render(request, "admin/procedures/searchCitizen.html")


def newCitizen(request):
    if request.method == "POST":
        form = citizenForm(request.POST or None, request.FILES or None)
        if citizen.objects.filter(
            name=request.POST["name"],
            last_name=request.POST["last_name"],
            second_name=request.POST["second_name"],
        ).exists():
            print("el usuario ya exite")
            message = "El ciudadano ya existe"
            return render(
                request,
                "admin/procedures/newCitizen.html",
                {"form": form, "myerror": message},
            )
            # return render(request,"admiin/procedures/newRequestProcedure.html")
        else:
            if form.is_valid():
                new_citizen = form.save()
                request_procedure_form = requestProcedureForm(
                    initial={
                        "requester": new_citizen,
                        "capturer": request.user,
                        "current_department": request.user.profile.department,
                    }
                )
                return render(
                    request,
                    "admin/procedures/newRequestProcedure.html",
                    {
                        "form": request_procedure_form,
                        "citizen": new_citizen,
                    },
                )

        return render(
            request,
            "admin/procedures/newCitizen.html",
            {"form": form, "myerror": message},
        )
    else:
        form = citizenForm()
    return render(request, "admin/procedures/newCitizen.html", {"form": form})


def newRequestProcedure(request):
    if request.method == "POST":
        form = requestProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            # form = requestProcedureForm()
            response = render(
                request, "admin/procedures/success.html", {"message": message}
            )
            response["HX-Trigger"] = "update-list"
            return response
    else:
        print(request)
        pk = request.GET["citizen"]
        print(pk)
        new_citizen = citizen.objects.get(id=pk)
        request_procedure_form = requestProcedureForm(
            initial={
                "requester": new_citizen,
                "capturer": request.user,
                "current_department": request.user.profile.department,
            }
        )
    return render(
        request,
        "admin/procedures/newRequestProcedure.html",
        {
            "form": request_procedure_form,
            "citizen": new_citizen,
        },
    )


def editRequestProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "POST":
        form = requestProcedureForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/procedures/success.html", {"message": message}
            )
            response["HX-Trigger"] = "update-list"
            return response
    else:
        form = requestProcedureForm(instance=model)
    return render(
        request,
        "admin/procedures/editRequestProcedure.html",
        {"form": form, "model": model},
    )


def editCitizen(request, pk):
    model = get_object_or_404(citizen, pk=pk)
    if request.method == "POST":
        form = citizenForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            updated_citizen = get_object_or_404(citizen, pk=pk)
        return render(
            request,
            "admin/procedures/citizen.html",
            {"message": message, "citizen": updated_citizen},
        )
    else:
        form = citizenForm(instance=model)
    return render(
        request, "admin/procedures/editCitizen.html", {"form": form, "model": model}
    )


def editStatusRequestProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "POST":
        procedure = model.id
        new_status = request.POST["status"]
        RequestProcedure.objects.filter(id=procedure).update(status=new_status)
        message = "Registro realizado correctamente"
        form = statusProcedureForm(instance=model)
        return render(
            request,
            "admin/procedures/editStatus.html",
            {"form": form, "model": model, "message": message},
        )
    else:
        form = statusProcedureForm(instance=model)
        return render(
            request, "admin/procedures/editStatus.html", {"form": form, "model": model}
        )


def deleteRequestProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "DELETE":
        model.delete()
    return HttpResponse("")


def newTrackingProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    form = TrackingProcedureForm(
        initial={
            "procedure": model,
            "capturer": request.user,
            "to_department": model.current_department,
        }
    )
    return render(
        request,
        "admin/procedures/newTrackingProcedure.html",
        {"form": form, "model": model},
    )


def saveTrackingProcedure(request):
    if request.method == "POST":
        form = TrackingProcedureForm(request.POST or None, request.FILES or None)
        procedure = request.POST["procedure"]
        new_department = request.POST["from_department"]
        # new_status = request.POST['status']
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            update_current_department = RequestProcedure.objects.filter(
                id=procedure
            ).update(current_department_id=new_department)
            # model = get_object_or_404(RequestProcedure, pk=procedure)
            # form = TrackingProcedureForm(initial={'procedure': model,'capturer': request.user,'to_department':model.current_department         })
            # update_current_department = RequestProcedure.objects.filter(id=procedure).update(current_department_id = department,status = new_status)
            response = render(
                request, "admin/procedures/success.html", {"message": message}
            )
            response["HX-Trigger"] = "update-list"
            return response
        # model = get_object_or_404(RequestProcedure, pk=procedure)
        # form = TrackingProcedureForm(initial={'procedure': model,'capturer': request.user,'to_department':model.current_department        })
        return render(
            request, "admin/procedures/newTrackingProcedure.html", {"form": form}
        )


def showProcedure(request, pk):
    requestProcedure = get_object_or_404(RequestProcedure, pk=pk)
    tracking = requestProcedure.trackingprocedure_set.all().order_by("id")
    evidences = requestProcedure.images_evidence.all().order_by("id")
    print(tracking)
    return render(
        request,
        "admin/procedures/timeLine.html",
        {"procedure": requestProcedure, "tracking": tracking, "evidences": evidences},
    )


def uploadEvidence(request, pk):

    if request.method == "POST":
        form = EvidenceProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid() and request.POST:
            post = form.save(commit=False)
            solicitud = request.POST["procedure"]
            usuario = request.user.id
            # post.procedure_id = solicitud
            # post.capturer = usuario
            if "images" in request.FILES:
                images = request.FILES.getlist("images")
                for image in images:
                    EvidenceProcedure.objects.create(
                        procedure_id=solicitud, image=image, capturer_id=usuario
                    )
            message = "Registro realizado correctamente"
            model = get_object_or_404(RequestProcedure, pk=pk)
            form = EvidenceProcedureForm(
                initial={
                    "procedure": model.id,
                    "capturer": request.user,
                }
            )
            return render(
                request,
                "admin/procedures/uploadEvidenceProcedure.html",
                {"form": form, "model": model, "message": message},
            )
    else:
        model = get_object_or_404(RequestProcedure, pk=pk)
        form = EvidenceProcedureForm(
            initial={
                "procedure": model.id,
                "capturer": request.user,
            }
        )
    return render(
        request,
        "admin/procedures/uploadEvidenceProcedure.html",
        {"form": form, "model": model},
    )


def addCommentProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "POST":
        # procedure = request.POST['procedure']
        form = commentProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save(commit=False)
            procedure = model.id
            comment = request.POST["comment"]
            user = request.user.id
            save_comment = commentProcedure.objects.create(
                procedure_id=procedure, user_id=user, comment=comment
            )
            if save_comment:
                print("se guardo")
            else:
                print("no se guardo")
            list = commentProcedure.objects.filter(procedure_id=procedure)
            response = render(
                request, "admin/procedures/comments.html", {"comments": list}
            )
            response["HX-Trigger"] = "clean-comment"
            return response


def addDocumentProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "POST":
        form = documentProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save(commit=False)
            procedure = model.id
            user = request.user.id
            document_type = request.POST["document_type"]
            if "document" in request.FILES:
                documents = request.FILES.getlist("document")
                for document in documents:
                    save_document = DocumentProcedure.objects.create(
                        procedure_id=procedure,
                        user_id=user,
                        document_type_id=document_type,
                        document=document,
                    )
                    if save_document:
                        print("se guardo")
                    else:
                        print("no se guardo")
            list = DocumentProcedure.objects.filter(procedure_id=procedure)
            return render(
                request, "admin/procedures/documents.html", {"documents": list}
            )
    list = DocumentProcedure.objects.filter(procedure_id=procedure)
    return render(request, "admin/procedures/documents.html", {"documents": list})


def addEvidenceProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "POST":
        form = EvidenceProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save(commit=False)
            procedure = model.id
            user = request.user.id
            if "images" in request.FILES:
                images = request.FILES.getlist("images")
                for image in images:
                    save_image = EvidenceProcedure.objects.create(
                        procedure_id=procedure, image=image, capturer_id=user
                    )
                    if save_image:
                        print("se guardo")
                    else:
                        print("no se guardo")
            list = EvidenceProcedure.objects.filter(procedure_id=procedure)
            return render(
                request, "admin/procedures/evidences.html", {"evidences": list}
            )
    list = EvidenceProcedure.objects.filter(procedure_id=procedure)
    return render(request, "admin/procedures/evidences.html", {"evidences": list})


def addDeliveryProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    if request.method == "POST":
        form = deliveryProcedureForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            procedure = model.id
            RequestProcedure.objects.filter(id=procedure).update(status="Entregada")
            message = "Registro realizado correctamente"
            list = DeliveryProcedure.objects.filter(procedure_id=procedure)
            return render(
                request,
                "admin/procedures/delivery_finish.html",
                {"deliveryInfo": list, "message": message},
            )


def shareRequestProcedure(request, pk):
    model = get_object_or_404(RequestProcedure, pk=pk)
    form = TrackingProcedureForm(
        initial={
            "procedure": model,
            "capturer": request.user,
            "to_department": model.current_department,
        }
    )
    return render(
        request,
        "admin/procedures/newTrackingProcedure.html",
        {"form": form, "model": model},
    )


def typesDocument(request):
    types_documents = DocumentTypeProcedure.objects.all()
    return render(
        request,
        "admin/procedures/typesDocument.html",
        {"types_documents": types_documents},
    )


def newTypeDocument(request):
    if request.method == "POST":
        newName = request.POST["name"]
        save_newName = DocumentTypeProcedure.objects.create(name=newName)
        if save_newName:
            print("se guardo")
            types_documents = DocumentTypeProcedure.objects.all()
            return render(
                request,
                "admin/procedures/typesDocument.html",
                {"types_documents": types_documents},
            )
        else:
            print("no se guardo")
        return
    else:
        return render(request, "admin/procedures/newTypeDocument.html")


def saveAccountingMoment(request, pk):
    print("llego a momento contable")
    if request.method == "POST":
        # procedure = request.POST['procedure']
        print(pk)
        try:
            momento_contable = AccountingMoment.objects.get(procedure_id=pk)
            form = AccountingMomentForm(
                request.POST or None, request.FILES or None, instance=momento_contable
            )
            if form.is_valid():
                form.save()
            return HttpResponse("<h1>Guardado</h1>")
        except AccountingMoment.DoesNotExist:
            form = AccountingMomentForm(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponse("<h1>Guardado</h1>")


def newTypeProcedure(request):
    if request.method == "POST":
        newName = request.POST["name"]
        save_newName = ProcedureType.objects.create(name=newName)
        if save_newName:
            print("se guardo")
            types_procedures = ProcedureType.objects.all()
            return render(
                request,
                "admin/procedures/typesProcedures.html",
                {"types_procedures": types_procedures},
            )
        else:
            print("no se guardo")
        return
    else:
        return render(request, "admin/procedures/newTypeProcedure.html")


def typesProcedure(request):
    types_procedures = ProcedureType.objects.all()
    return render(
        request,
        "admin/procedures/typesProcedures.html",
        {"types_procedures": types_procedures},
    )
