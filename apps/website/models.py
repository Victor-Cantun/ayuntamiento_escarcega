from django.db import models
from django.utils import timezone


# Create your models here.
# TODO-carrosel principal
class carousel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        verbose_name="Titulo", max_length=100, unique=True, null=True
    )
    image = models.ImageField(verbose_name="Imagen", upload_to="images/carousel/")
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.image}"


# TODO-post del blog
class Post(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)
    content = models.TextField(verbose_name="Contenido")
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/post/")
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.post.title}"


# TODO-posicion
class position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Cargo", max_length=50, unique=True)

    def __str__(self):
        row = self.name
        return row


# TODO-cabildo
class council(models.Model):
    id = models.AutoField(primary_key=True)
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
        verbose_name="Dirección", max_length=200, blank=True, null=True
    )
    cellphone = models.CharField(
        verbose_name="Celular", max_length=10, blank=True, null=True
    )
    phone = models.CharField(
        verbose_name="Teléfono", max_length=10, blank=True, null=True
    )
    position = models.ForeignKey(
        position, verbose_name="Cargo", on_delete=models.CASCADE, blank=True, null=True
    )
    profile_image = models.ImageField(
        verbose_name="Imagen de perfil",
        null=True,
        blank=True,
        upload_to="images/council_profiles/",
    )
    creation = models.DateTimeField(auto_now=True)

    def position_name(self):
        return self.position

    def __str__(self):
        row = "Integrante del Cabildo: " + self.name
        return row


# TODO-director
class director(models.Model):
    id = models.AutoField(primary_key=True)
    profession = models.CharField(verbose_name="Profesión", max_length=50, blank=True, null=True)
    name = models.CharField(verbose_name="Nombre", max_length=50)
    firstlastname = models.CharField(verbose_name="Primer apellido", max_length=50, blank=True, null=True)
    secondlastname = models.CharField(verbose_name="Segundo apellido", max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name="Correo electrónico",max_length=100,unique=True,blank=True,null=True,)
    address = models.CharField(verbose_name="Dirección", max_length=200, blank=True, null=True)
    cellphone = models.CharField(verbose_name="Celular", max_length=10, blank=True, null=True)
    phone = models.CharField(verbose_name="Teléfono", max_length=10, blank=True, null=True)
    profile_image = models.ImageField(verbose_name="Imagen de perfil",null=True,blank=True,upload_to="images/directors_profiles/")
    creation = models.DateTimeField(auto_now=True)

    def director_name(self):
        if self.firstlastname != None and self.secondlastname == None:
            return f"{self.name} {self.firstlastname}"
        if self.firstlastname == None and self.secondlastname != None:
            return f"{self.name} {self.secondlastname}"
        if self.firstlastname != None and self.secondlastname != None:
            return f"{self.name} {self.firstlastname} {self.secondlastname}"

    def __str__(self):
        row = "Director: " + self.director_name()
        return row

    def delete(self, *args, **kwargs):
        # Condición para eliminar la imagen solo si existe
        if self.profile_image:
            self.profile_image.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        permissions = [
            ("puede_crear", "Puede crear director"),
            ("puede_leer", "Puede leer director"),
            ("puede_actualizar", "Puede actualizar director"),
            ("puede_eliminar", "Puede eliminar director"),
        ]


# TODO-dependencia
class dependence(models.Model):
    id = models.AutoField(primary_key=True)
    director = models.OneToOneField(director, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(verbose_name="Dependencia:", max_length=150, unique=True)
    email = models.EmailField(verbose_name="Correo electrónico",max_length=100,unique=True,blank=True,null=True,)
    address = models.CharField(verbose_name="Dirección", max_length=200, blank=True, null=True)
    phone = models.CharField(verbose_name="Teléfono", max_length=10, blank=True, null=True)
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        row = self.name
        return row


# TODO-contabilidad
class infoGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre del grupo", max_length=500, unique=True)

    def __str__(self):
        row = self.name
        return row


class infoSubgroup(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(infoGroup,verbose_name="Categoría o Grupo",related_name="subgrupos",on_delete=models.CASCADE,)
    name = models.CharField(verbose_name="Nombre de la categoría o subgrupo", unique=True, max_length=500)

    class Meta:
        unique_together = ('group', 'name') 

    def __str__(self):
        row = self.name
        return row


class accounting(models.Model):
    no_quarter = [(1, "1"),(2, "2"),(3, "3"),(4, "4"),]
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(infoGroup,related_name="grupos",on_delete=models.CASCADE,null=True,blank=True,)
    subgroup = models.ForeignKey(infoSubgroup,related_name="subgrupos",on_delete=models.CASCADE,null=True,blank=True,)
    name = models.CharField(verbose_name="Nombre del archivo", max_length=200)
    dependence = models.ForeignKey(dependence,verbose_name="Dirección/Dependencia",on_delete=models.CASCADE,blank=True,null=True,)
    quarter = models.IntegerField(verbose_name="Trimestre", choices=no_quarter, null=True, blank=True)
    quarterly = models.CharField(verbose_name="Trimestral", max_length=100, null=True, blank=True)
    year = models.CharField(verbose_name="Año", max_length=5, null=True, blank=True)
    document = models.FileField(verbose_name="Documento",upload_to="documents/accounting/",null=True,blank=True,)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete(save=False)
        super().delete(*args, **kwargs)


# TODO-GACETA
class gazette(models.Model):
    months = [
        (1,  "Enero"),
        (2,  "Febrero"),
        (3,  "Marzo"),
        (4,  "Abril"),
        (5,  "Mayo"),
        (6,  "Junio"),
        (7,  "Julio"),
        (8,  "Agosto"),
        (9,  "Septiembre"),
        (10, "Octubre"),
        (11, "Noviembre"),
        (12, "Diciembre"),
    ]
    id = models.AutoField(primary_key=True)
    year = models.IntegerField(verbose_name="Año", null=True)
    month = models.PositiveSmallIntegerField(verbose_name="Mes",choices=months, null=True)
    document = models.FileField(verbose_name="Documento", upload_to="documents/gazette/", null=True)
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} : {self.get_month_display()}"

    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete(save=False)
        super().delete(*args, **kwargs)


# TODO-DOCUMENTOS
class document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre", max_length=200)
    document = models.FileField(
        verbose_name="Documento",
        upload_to="documents/documents/",
        null=True,
        blank=True,
    )
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete(save=False)
        super().delete(*args, **kwargs)


class DependenceTransparency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre de la Dependencia")

    def __str__(self):
        return self.name


class CategoryTransparency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre de la categoría")

    def __str__(self):
        return self.name


# TODO-Transparencia
class Transparency(models.Model):
    id = models.AutoField(primary_key=True)
    dependence = models.ForeignKey(
        DependenceTransparency, verbose_name="Dependence", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        CategoryTransparency, verbose_name="Categoría", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name="Nombre del archivo")
    document = models.FileField(
        verbose_name="Documento", upload_to="documents/document_transparency/"
    )
    user = models.ForeignKey(
        "auth.User", verbose_name="Usuario", on_delete=models.CASCADE
    )
    creation = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete(save=False)
        super().delete(*args, **kwargs)


# TODO-Obligaciones comunes
class Obligation(models.Model):
    id = models.AutoField(primary_key=True)
    fraction = models.CharField(verbose_name="Fracción")
    obligation = models.CharField(verbose_name="Obligación")
    applicability = models.BooleanField(verbose_name="Aplicabilidad")
    periodicity = models.CharField(verbose_name="Periodicidad")

    def __str__(self):
        return self.obligation


class ObligationDocument(models.Model):
    id = models.AutoField(primary_key=True)
    obligation = models.ForeignKey(
        Obligation, verbose_name="Obligación", on_delete=models.CASCADE
    )
    year = models.IntegerField(verbose_name="Año")
    name = models.CharField(verbose_name="Nombre del archivo")
    document = models.FileField(
        verbose_name="Documento", upload_to="documents/document_obligation/"
    )
    creation = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete(save=False)
        super().delete(*args, **kwargs)
