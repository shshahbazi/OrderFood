from rest_framework import serializers

from .models import Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

    def to_representation(self, instance):
        return_dict = dict(super().to_representation(instance))

        choice_dict = {k[0]: k[1] for k in instance.CATEGORY_CHOICES}
        return_dict['category'] = choice_dict[return_dict['category']]

        return return_dict
