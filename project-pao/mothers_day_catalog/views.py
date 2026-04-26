from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import MothersDayProduct
from .serializers import MothersDayProductSerializer


class MothersDayProductViewSet(viewsets.ModelViewSet):
    serializer_class = MothersDayProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = MothersDayProduct.objects.all()

        if self.request.method == 'GET':
            queryset = queryset.filter(is_active=True)

        return queryset
