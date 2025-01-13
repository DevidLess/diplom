import django_filters
from django_filters.widgets import LinkWidget

from .models import *

CourtOrderSort = [
    ["number", "Номер (по возрастанию)"],
    ["-number", "Номер (по убыванию)"],
    ["registration_date", "Дата (по возрастанию)"],
    ["-registration_date", "Дата (по убыванию)"],
]


class CourtOrderFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        label="Статус",
        choices=list(CourtOrderStatus.objects.all().values_list("id", "title")),
    )
    ordering = django_filters.OrderingFilter(
        choices=CourtOrderSort, required=False, empty_label=None, label="Сортировка"
    )

    class Meta:
        model = CourtOrder
        fields = ["status"]
        order_by_field = "number"


class TemplateFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains", label="Название")
    description = django_filters.CharFilter(lookup_expr="icontains", label="Описание")

    class Meta:
        model = Template
        fields = ["title", "description"]
        # order_by_field = 'number'
