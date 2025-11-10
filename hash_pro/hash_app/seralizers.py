from rest_framework import seralizers
from . models import Developers
class Developerseralizer (seralizers.ModelSerializer):
    class Meta:
        model=Developers
        fields="__all__"
