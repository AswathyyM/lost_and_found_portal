from django.shortcuts import render
from django.shortcuts import redirect
from .models import Item
from .forms import ItemForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

class UserLoginView(LoginView):
    template_name='items/login.html'

def home(request):

    items=Item.objects.all()

    return render(
        request,
        'items/home.html',
        {'items':items}
    )


@login_required
def add_item(request):

    if request.method=='POST':

        form=ItemForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            item=form.save(
                commit=False
            )

            item.owner=request.user

            item.save()

            return redirect('/')

    else:
        form=ItemForm()

    return render(
        request,
        'items/add.html',
        {'form':form}
    )

@login_required
def edit_item(request, id):
    item = get_object_or_404(Item, id=id)

    if item.owner != request.user:
        raise PermissionDenied("You are not allowed to edit this item.")

    if request.method == 'POST':
        form = ItemForm(
            request.POST,
            request.FILES,
            instance=item
        )
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ItemForm(instance=item)

    return render(
        request,
        'items/edit.html',
        {'form': form, 'item': item}
    )


@login_required
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)

    if item.owner != request.user:
        raise PermissionDenied("You are not allowed to delete this item.")

    if request.method == 'POST':
        item.delete()
        return redirect('/')

    return render(
        request,
        'items/delete_confirm.html',
        {'item': item}
    )

@login_required
def claim(request,id):

    item=Item.objects.get(
        id=id
    )

    item.claimed=True

    item.claimed_by=request.user

    item.save()

    return redirect('/')

def signup(request):

    if request.method=='POST':

        form=UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user=form.save()

            login(
                request,
                user
            )

            return redirect('/')

    else:

        form=UserCreationForm()

    return render(
        request,
        'items/signup.html',
        {'form':form}
    )