from rest_framework import serializers, viewsets

from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(
        format="%d/%m/%Y",
        input_formats=["%d/%m/%Y", "%Y-%m-%d"],
    )

    class Meta:
        model = Person
        fields = ["id", "name", "age", "date_of_birth"]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by("id")
    serializer_class = PersonSerializer
