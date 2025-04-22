from rest_framework import serializers
from .models import dependence, director


class directorSerializer(serializers.ModelSerializer):
    dependence = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = director
        fields = "__all__"


class dependenceSerializer(serializers.ModelSerializer):
    director_name = serializers.SerializerMethodField()
    director_detail = directorSerializer(source="director", read_only=True)
    # director = serializers.PrimaryKeyRelatedField(
    #    queryset=director.objects.all(), write_only=True
    # )

    class Meta:
        model = dependence
        # fields = "__all__"
        fields = [
            "id",
            "name",
            "director_name",
            "director_detail",
            # "director",
            "email",
            "address",
            "phone",
        ]  # Incluye ambos campos de director

    def get_director_name(self, obj):
        return obj.director.director_name() if obj.director else None
