from django.db.models import Q
from rest_framework.filters import SearchFilter


# Все примеры кода изъяты из контекста, так как проект, в котором они использовались, защищён NDA


class IsAutoSalesExistsFilter(SearchFilter):
    """Ищет бренды/модели для котрых существуют
    опубликованные объявления"""

    search_param = 'is_auto_sales_exists'
    template = 'rest_framework/filters/search.html'
    lookup_prefixes = {
        '=': 'iexact'
    }
    search_title = 'Existing auto-sales'
    search_description = 'Looking for brands/models with existing auto-sales'

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        for search_term in search_terms:
            if search_term.lower() == 'true':
                adverts = Advertisement.objects.filter(status=AdvertisementStatusEnum.PUBLISHED).all()
                auto_brands = []
                auto_models = []
                model = queryset.model
                for advert in adverts:
                    auto_brands.append(advert.brand)
                    auto_models.append(advert.model)
                try:
                    queryset = model.objects.filter(Q(Q(name__in=auto_models) & Q(brand__name__in=auto_brands))).all()
                except:
                    queryset = model.objects.filter(
                        Q(Q(name__in=auto_brands))).all()
        return queryset
