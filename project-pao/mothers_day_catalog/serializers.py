from rest_framework import serializers

from .models import MothersDayProduct


class MothersDayProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MothersDayProduct
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',
            'image_url',
            'is_active',
            'display_order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'image_url', 'created_at', 'updated_at']

    def get_image_url(self, product):
        if not product.image:
            return None

        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(product.image.url)

        return product.image.url
