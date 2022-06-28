from rest_framework import serializers

class FilmSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    year = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=9, decimal_places=1)
    pic = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)

