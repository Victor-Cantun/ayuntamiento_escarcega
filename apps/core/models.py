from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# TODO-director
class director(models.Model):
    profile_image = models.ImageField(
        verbose_name="Imagen de perfil",
        upload_to="images/townhall/directors_profiles/",
        null=True,
        blank=True,
    )
    id = models.AutoField(primary_key=True)
    profession = models.CharField(
        verbose_name="Profesión", max_length=50, blank=True, null=True
    )
    name = models.CharField(verbose_name="Nombre", max_length=50)
    firstlastname = models.CharField(
        verbose_name="Primer apellido", max_length=50, blank=True, null=True
    )
    secondlastname = models.CharField(
        verbose_name="Segundo apellido", max_length=50, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="Correo electrónico",
        max_length=100,
        unique=True,
        blank=True,
        null=True,
    )
    address = models.CharField(
        verbose_name="Domicilio", max_length=200, blank=True, null=True
    )
    cellphone = models.CharField(
        verbose_name="Celular", max_length=10, blank=True, null=True
    )
    phone = models.CharField(
        verbose_name="Teléfono", max_length=10, blank=True, null=True
    )

    creation = models.DateTimeField(auto_now=True)

    def director_name(self):
        if self.firstlastname != None and self.secondlastname == None:
            return f"{self.name} {self.firstlastname}"
        if self.firstlastname == None and self.secondlastname != None:
            return f"{self.name} {self.secondlastname}"
        if self.firstlastname != None and self.secondlastname != None:
            return f"{self.name} {self.firstlastname} {self.secondlastname}"

    def __str__(self):
        # row = "Director: " + self.director_name()
        row = self.director_name()
        return row

    def delete(self, *args, **kwargs):
        # Condición para eliminar la imagen solo si existe
        if self.profile_image:
            self.profile_image.delete(save=False)
        super().delete(*args, **kwargs)


# TODO-dependencia
class dependence(models.Model):
    id = models.AutoField(primary_key=True)
    director = models.ForeignKey(
        director, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(verbose_name="Dependencia", max_length=150, unique=True)
    email = models.EmailField(
        verbose_name="Correo electrónico",
        max_length=100,
        unique=True,
        blank=True,
        null=True,
    )
    address = models.CharField(
        verbose_name="Domicilio", max_length=200, blank=True, null=True
    )
    phone = models.CharField(
        verbose_name="Teléfono", max_length=10, blank=True, null=True
    )
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        row = self.name
        return row


# TODO-departamento
class department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Departamento", max_length=150, unique=True)
    dependence = models.ForeignKey(
        dependence, on_delete=models.CASCADE, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="Correo electrónico",
        max_length=100,
        unique=True,
        blank=True,
        null=True,
    )
    address = models.CharField(
        verbose_name="Domicilio", max_length=200, blank=True, null=True
    )
    phone = models.CharField(
        verbose_name="Teléfono", max_length=10, blank=True, null=True
    )
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        row = f"{self.dependence} - {self.name}"
        return row


# TODO-CIUDADANO
class citizen(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre", max_length=50)
    last_name = models.CharField(verbose_name="Primer apellido", max_length=50)
    second_name = models.CharField(verbose_name="Segundo apellido", max_length=50)
    address = models.CharField(verbose_name="Domicilio", max_length=200)
    colony = models.CharField(verbose_name="Colonia", null=True, blank=True)
    locality = models.CharField(verbose_name="Localidad", null=True, blank=True)
    cellphone = models.CharField(
        verbose_name="Celular", unique=True, null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Correo electrónico", unique=True, null=True, blank=True
    )
    INE = models.CharField(verbose_name="INE", max_length=20, null=True, blank=True)
    birthdate = models.DateField(
        verbose_name="Fecha de nacimiento", max_length=20, null=True, blank=True
    )

    def __str__(self):
        row = f"{self.name} {self.last_name} {self.second_name}"
        return row


# TODO-TIPO DE GESTION
class ProcedureType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre", max_length=50)

    def __str__(self):
        row = self.name
        return row


# TODO-GESTIONES
class RequestProcedure(models.Model):
    request_status = [
        ("Pendiente", "Pendiente"),
        ("Autorizada", "Autorizada"),
        ("Entregada", "Entregada"),
        ("Cancelada", "Cancelada"),
    ]
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="Fecha", auto_now_add=True)
    requester = models.ForeignKey(
        citizen,
        verbose_name="Solicitante",
        related_name="requesters",
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        verbose_name="Descripción de la Solicitud", max_length=200
    )
    document = models.FileField(
        verbose_name="Documento",
        upload_to="documents/requests_procedures/",
        null=True,
        blank=True,
    )
    procedure_type = models.ForeignKey(
        ProcedureType,
        verbose_name="Tipo de gestion",
        related_name="procedures_types",
        on_delete=models.CASCADE,
    )
    current_department = models.ForeignKey(
        department,
        verbose_name="Departamento",
        related_name="department",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name="Estado de la solicitud",
        max_length=20,
        choices=request_status,
        default="Pendiente",
    )
    capturer = models.ForeignKey(
        User,
        verbose_name="Capturista",
        related_name="request_capturer",
        on_delete=models.CASCADE,
    )
    creation = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("change_status", "Puede cambiar el estado de la solicitud"),
            ("view_report_procedure", "Puede ver el reporte de gestiones"),
            ("can_finish_procedure", "Puede finalizar la gestión"),
        ]

    def __str__(self):
        row = f"{self.description}"
        return row

    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete(save=False)
        super().delete(*args, **kwargs)


class TrackingProcedure(models.Model):
    request_status = [
        ("Pendiente", "Pendiente"),
        ("Autorizada", "Autorizada"),
        ("Entregada", "Entregada"),
        ("Cancelada", "Cancelada"),
    ]
    id = models.AutoField(primary_key=True)
    procedure = models.ForeignKey(
        RequestProcedure, on_delete=models.CASCADE, null=True, blank=True
    )
    to_department = models.ForeignKey(
        department,
        verbose_name="Departamento que emite",
        related_name="to_department",
        on_delete=models.CASCADE,
    )
    from_department = models.ForeignKey(
        department,
        verbose_name="Departamento que recibe",
        related_name="from_department",
        on_delete=models.CASCADE,
    )
    folio = models.CharField(
        verbose_name="Folio del documento", max_length=20, null=True, blank=True
    )
    document = models.FileField(
        verbose_name="Documento",
        upload_to="documents/tracking_procedures/",
        null=True,
        blank=True,
    )
    remarks = models.TextField(verbose_name="Observaciones")
    status = models.CharField(
        verbose_name="Estado de la solicitud",
        max_length=20,
        choices=request_status,
        default="Pendiente",
    )
    capturer = models.ForeignKey(
        User, related_name="tracking_capturer", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        row = f"{self.id} {self.procedure.description}"
        return row


class EvidenceProcedure(models.Model):
    id = models.AutoField(primary_key=True)
    procedure = models.ForeignKey(
        RequestProcedure, on_delete=models.CASCADE, related_name="images_evidence"
    )
    image = models.ImageField(
        verbose_name="Evidencia", upload_to="images/evidence_procedures/"
    )
    capturer = models.ForeignKey(
        "auth.User", related_name="evidence_capturer", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)


class commentProcedure(models.Model):
    id = models.AutoField(primary_key=True)
    procedure = models.ForeignKey(
        RequestProcedure, on_delete=models.CASCADE, related_name="comments_procedures"
    )
    comment = models.TextField(verbose_name="Comentario de seguimiento")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class DocumentTypeProcedure(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre", max_length=50)

    def __str__(self):
        row = self.name
        return row


class DocumentProcedure(models.Model):
    id = models.AutoField(primary_key=True)
    procedure = models.ForeignKey(
        RequestProcedure, on_delete=models.CASCADE, related_name="documents_procedures"
    )
    document_type = models.ForeignKey(
        DocumentTypeProcedure,
        verbose_name="Tipo de documento",
        related_name="documents_types_procedures",
        on_delete=models.CASCADE,
    )
    document = models.FileField(
        verbose_name="Documento", upload_to="documents/document_procedures/"
    )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class DeliveryProcedure(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="Fecha")
    procedure = models.OneToOneField(
        RequestProcedure, on_delete=models.CASCADE, related_name="deliveries_procedures"
    )
    comment = models.TextField(verbose_name="Se entrega")
    total_amount = models.IntegerField(verbose_name="Monto final")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)


# TODO- MOMENTO CONTABLE
class AccountingMoment(models.Model):
    id = models.AutoField(primary_key=True)
    procedure = models.ForeignKey(
        RequestProcedure, on_delete=models.CASCADE, related_name="moments_procedures"
    )
    # TODO-COMPROMETIDO
    office_1 = models.BooleanField(verbose_name="Oficio de solicitud", default=False)
    office_2 = models.BooleanField(
        verbose_name="Solicitud de material o servicio", default=False
    )
    office_3 = models.BooleanField(
        verbose_name="Suficiencia presupuestal", default=False
    )
    office_4 = models.BooleanField(
        verbose_name="Autorización de la suficiencia", default=False
    )
    office_4a = models.BooleanField(
        verbose_name="3 Invitación a proveedores", default=False
    )
    office_4b = models.BooleanField(verbose_name="3 Cotizaciones", default=False)
    office_4c = models.BooleanField(
        verbose_name="Oficio o caratula de adjudicación", default=False
    )
    office_4d = models.BooleanField(
        verbose_name="Contrato de bienes o servicio desglosado", default=False
    )
    office_4e = models.BooleanField(
        verbose_name="Convenio con instituciones", default=False
    )
    office_4f = models.BooleanField(
        verbose_name="Oficio de solicitud de dictamen", default=False
    )
    office_4g = models.BooleanField(
        verbose_name="Dictamenes y oficio de presidencia", default=False
    )
    office_4h = models.BooleanField(
        verbose_name="Orden de compra y o servicio", default=False
    )
    office_4i = models.BooleanField(verbose_name="Estudio socieconimico", default=False)
    office_4j = models.BooleanField(
        verbose_name="Dictamenes mecanicos o de servicio y bitacora de control",
        default=False,
    )
    office_4k = models.BooleanField(
        verbose_name="Convocatoria o solicitud", default=False
    )
    # TODO-DEVENGADO
    office_5 = models.BooleanField(verbose_name="CFDI", default=False)
    office_6 = models.BooleanField(verbose_name="XML", default=False)
    office_7 = models.BooleanField(verbose_name="Validación del SAT", default=False)
    office_8 = models.BooleanField(
        verbose_name="Nota de entrega del proveedor", default=False
    )
    office_9 = models.BooleanField(verbose_name="Comprobante de entrega", default=False)
    office_9a = models.BooleanField(verbose_name="Lista de comensales", default=False)
    office_10 = models.BooleanField(verbose_name="Evidencia fotográfica", default=False)
    office_11 = models.BooleanField(
        verbose_name="Poliza del sistema contable del comprometido y devengado",
        default=False,
    )
    # TODO-EJERCIDO
    office_12 = models.BooleanField(verbose_name="Orden de pago", default=False)
    # TODO-PAGADO
    office_13 = models.BooleanField(verbose_name="Transferencia de pago", default=False)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
