from rest_framework import serializers
from .models import (
    CategoryTransparency,
    DependenceTransparency,
    Post,
    PostImage,
    Transparency,
    carousel,
    accounting,
    gazette,
    infoGroup,
    infoSubgroup,
    position,
    council,
    director,
    dependence,
)


class carouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = carousel
        fields = "__all__"


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "created_at", "updated_at", "images"]


class positionSerializer(serializers.ModelSerializer):
    class Meta:
        model = position
        fields = "__all__"


class councilSerializer(serializers.ModelSerializer):

    position_name = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    position_detail = positionSerializer(source="position", read_only=True)
    position = serializers.PrimaryKeyRelatedField(
        queryset=position.objects.all(), write_only=True
    )

    class Meta:
        model = council
        fields = [
            "position_name",
            "position_detail",
            "position",
            "id",
            "name",
            "firstlastname",
            "secondlastname",
            "email",
            "address",
            "cellphone",
            "phone",
            "profile_image",
        ]

    def get_position_name(self, obj):
        return obj.position.position_name() if obj.position else None


class directorSerializer(serializers.ModelSerializer):
    dependence = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = director
        fields = "__all__"


class dependenceSerializer(serializers.ModelSerializer):

    director_name = serializers.SerializerMethodField()
    director_detail = directorSerializer(source="director", read_only=True)
    director = serializers.PrimaryKeyRelatedField(
        queryset=director.objects.all(), write_only=True
    )

    class Meta:
        model = dependence
        fields = "__all__"
        fields = [
            "id",
            "name",
            "director_name",
            "director_detail",
            "director",
            "email",
            "address",
            "phone",
        ]  # Incluye ambos campos de director

    def get_director_name(self, obj):
        return obj.director.director_name() if obj.director else None


class infoGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = infoGroup
        fields = "__all__"


class infoSubgroupSerializer(serializers.ModelSerializer):
    group_detail = infoGroupSerializer(source="infoGroup", read_only=True)

    class Meta:
        model = infoSubgroup
        fields = "__all__"


class accountingSerializer(serializers.ModelSerializer):
    # subgroup_detail = infoSubgroupSerializer(source="infoSubgroup", read_only=True)
    # dependence_detail = dependenceSerializer(source="dependence", read_only=True)

    class Meta:
        model = accounting
        fields = "__all__"


class SubgrupoSerializer(serializers.ModelSerializer):
    documentos = accountingSerializer(many=True)  # Relación con documentos

    class Meta:
        model = infoSubgroup
        fields = ["id", "name", "documentos"]


class GrupoSerializer(serializers.ModelSerializer):
    subgrupos = SubgrupoSerializer(many=True)  # Relación con subgrupos

    class Meta:
        model = infoGroup
        fields = ["id", "name", "subgrupos"]


class gazetteSerializer(serializers.ModelSerializer):
    class Meta:
        model = gazette
        fields = "__all__"

class YearSerializer(serializers.Serializer):
    year = serializers.IntegerField() 

class TransparencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transparency
        fields = ['name','document']    

class DependenceTransparencySerializer(serializers.ModelSerializer):

    class Meta:
        model = DependenceTransparency    
        fields = "__all__"

class CategoryTransparencySerializer(serializers.ModelSerializer):
    dependences = serializers.SerializerMethodField()
    class Meta:
        model = CategoryTransparency
        fields = "__all__"

    def get_dependences(self, obj):
        dependences = DependenceTransparency.objects.all()
        return DependenceTransparencySerializer(dependences, many=True).data