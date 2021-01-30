import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class BookFilter(django_filters.FilterSet):
	book_name = CharFilter(field_name="Book_Name",  lookup_expr='icontains')
	author = CharFilter(field_name='Author')
	Genre = CharFilter(field_name='Genre')

	class Meta:
		model = Add_Book
		fields = '__all__'
		exclude = ['Book_Name', 'Book_ID','Author','Genre', 'Book_Publisher']
