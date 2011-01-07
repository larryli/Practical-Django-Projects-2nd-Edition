from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list

from coltrane.models import Entry
from coltrane.models import Category

def entries_index(request):
	return render_to_response('coltrane/entry_index.html', {'entry_list': Entry.objects.all()})

def category_detail(request, slug):

	category = get_object_or_404(Category, slug=slug)

	return object_list(
		request,
		queryset=category.entry_set.all(),
		extra_content={'category': category})
