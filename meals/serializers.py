from rest_framework import serializers

from meals.constants import MENU_POSITION_MAX_LENGTH
from meals.models import MenuPosition


class MenuPositionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=MENU_POSITION_MAX_LENGTH)
    nutritional_value = serializers.IntegerField(min_value=0)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.ImageField(read_only=True)

    def create(self, validated_data):
        return MenuPosition.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.nutritional_value = validated_data.get('nutritional_value', instance.nutritional_value)
        instance.price = validated_data.get('price', instance.price)
        # instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


