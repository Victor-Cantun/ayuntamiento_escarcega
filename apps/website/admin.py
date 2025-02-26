from django.contrib import admin
from .models import (
    CategoryTransparency,
    DependenceTransparency,
    Obligation,
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

# Register your models here.


class positionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class councilAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "firstlastname", "secondlastname", "profile_image")


class directorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "firstlastname", "secondlastname", "profile_image")


class dependenceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3  # Número de imágenes adicionales para subir por defecto


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]


admin.site.register(Post, PostAdmin)
admin.site.register(carousel)
admin.site.register(infoGroup)
admin.site.register(infoSubgroup)
admin.site.register(accounting)
admin.site.register(gazette)
admin.site.register(position, positionAdmin)
admin.site.register(council, councilAdmin)
admin.site.register(director, directorAdmin)
admin.site.register(dependence, dependenceAdmin)
admin.site.register(DependenceTransparency)
admin.site.register(CategoryTransparency)
admin.site.register(Transparency)
admin.site.register(Obligation)
admin.site.register(document)
