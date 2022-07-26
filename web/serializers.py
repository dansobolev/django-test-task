from rest_framework import serializers
from .models import Entity, Bill


class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class EntitySerializer(serializers.ModelSerializer):
    bill = BillsSerializer()

    class Meta:
        model = Entity
        fields = '__all__'

