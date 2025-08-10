from rest_framework import serializers
from .models import collage,student,company,employee
from rest_framework import serializers

class collageserializer(serializers.ModelSerializer):
    class Meta:
        model = collage
        fields = '__all__'

class studentserializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = '__all__'


class employeeserializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = employee
        fields = '__all__'

class companyserializer(serializers.ModelSerializer):
    employees = employeeserializer(many=True,read_only=True)
    class Meta:
        model = company
        fields = '__all__'