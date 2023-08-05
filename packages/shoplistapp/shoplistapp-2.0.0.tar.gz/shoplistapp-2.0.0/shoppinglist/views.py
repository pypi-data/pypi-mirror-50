from django.shortcuts import render, redirect
from shoppinglist.models import Shoppinglist
from django.utils import timezone
from .forms import NameForm, DeleteForm
from django.contrib import messages


def list_index(request):
    shoplist = Shoppinglist.objects.all()
    context = {
        'shoplist': shoplist
    }
    return render(request, 'list_index.html', context)


def list_details(request, pk):
    shoplists = Shoppinglist.objects.get(pk=pk)
    context = {
        'shoplists': shoplists
    }

    return render(request, 'list_detail.html', context)


def list_add(request):
    if request.method == "POST":
        # create form instance, populate with data from request
        form = NameForm(request.POST)
        # check if it's valid
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.save()
            # process and redirect
            return redirect('list_index')

    else:
        form = NameForm()
    return render(request, 'add.html', {'form': form})


def list_delete(request, pk):
    shoplist = Shoppinglist.objects.get(pk=pk)
    form = DeleteForm(request.POST)
    try:
        if request.method == "POST":
            shoplist.delete()
            messages.success(request, 'Item successfully deleted!')
        else:
            form = DeleteForm(instance=shoplist)
    except Exception as e:
        messages.warning(request, "Could not delete item: Error {}".format(e))
    context = {
        'form': form,
        'shoplist': shoplist
    }
    return render(request, 'list_delete.html', context)
