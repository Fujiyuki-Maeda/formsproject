from django_filters import filters
from django_filters import FilterSet
from .models import Item


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = '%s （降順）'


class ItemFilter(FilterSet):

    member_no = filters.CharFilter(label='会員番号', lookup_expr='contains')
    name = filters.CharFilter(label='氏名', lookup_expr='contains')

    order_by = MyOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('member_no', 'member_no'),
            ('name', 'name'),
        ),
        field_labels={
            'member_no': '会員番号',
            'name': '氏名',
        },
        label='並び順'
    )

    class Meta:

        model = Item
        fields = ('member_no', 'name',)

