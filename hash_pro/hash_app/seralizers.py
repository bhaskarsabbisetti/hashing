from rest_framework import serializers
from . models import Developers
class Developerseralizer (serializers.ModelSerializer):
    class Meta:
        model=Developers
        fields="__all__"
