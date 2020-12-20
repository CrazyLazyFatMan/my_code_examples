from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


# Все примеры кода изъяты из контекста, так как проект, в котором они использовались, защищён NDA


class AutoModificationUniqueGearboxTypeView(mixins.ListModelMixin, GenericViewSet):
    queryset = AutoModification.objects.cache()
    filter_backends = (DjangoFilterBackend,)
    filter_class = AutoModificationUniqueGearboxFilter
    serializer_class = ListAutoModificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        ).exclude(gearbox_type__isnull=True)
        gearbox_types = queryset.values_list('gearbox_type', flat=True).distinct()
        gearbox_types = [AutoModification.gearbox_type.field.choices[gearbox_type][1] for gearbox_type in gearbox_types]
        return Response(gearbox_types)