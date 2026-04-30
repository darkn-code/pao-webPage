from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import MothersDayProduct
from .serializers import MothersDayProductSerializer


class MothersDayProductQuerySetMixin:
    serializer_class = MothersDayProductSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = MothersDayProduct.objects.all()

        if self.request.method == 'GET' and not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        return queryset


class MothersDayProductListCreateAPIView(
    MothersDayProductQuerySetMixin,
    generics.ListCreateAPIView,
):
    pass


class MothersDayProductRetrieveUpdateDestroyAPIView(
    MothersDayProductQuerySetMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    def perform_update(self, serializer):
        product = self.get_object()
        old_image_name = product.image.name
        updated_product = serializer.save()

        if old_image_name and old_image_name != updated_product.image.name:
            product.image.storage.delete(old_image_name)

    def perform_destroy(self, product):
        image = product.image
        product.delete()

        if image:
            image.delete(save=False)
