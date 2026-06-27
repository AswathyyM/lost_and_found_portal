from django.shortcuts import render
from django.shortcuts import redirect
from .models import Item
from .forms import ItemForm
from .auth_forms import StudentSignUpForm
from .notifications import EMAIL_MISSING_CONFIG
from .notifications import EMAIL_MISSING_OWNER
from .notifications import EMAIL_SEND_FAILED
from .notifications import EMAIL_SENT
from .notifications import send_item_claimed_email
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages

class UserLoginView(LoginView):
    template_name='items/login.html'

def home(request):

    items = Item.objects.all()

    title = request.GET.get('title', '')
    location = request.GET.get('location', '')

    if title:
        items = items.filter(
            title__icontains=title
        )

    if location:
        items = items.filter(
            location__icontains=location
        )

    return render(
        request,
        'items/home.html',
        {
            'items': items,
            'title': title,
            'location': location
        }
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

    item=get_object_or_404(
        Item,
        id=id
    )

    if item.owner == request.user:
        messages.error(
            request,
            'You cannot claim your own item.'
        )
        return redirect('/')

    if item.claimed:
        messages.warning(
            request,
            'This item has already been claimed.'
        )
        return redirect('/')

    email_status = send_item_claimed_email(
        item,
        request.user
    )

    if email_status == EMAIL_MISSING_CONFIG:
        messages.error(
            request,
            'Claim failed because email notifications are not configured. Add EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, and DEFAULT_FROM_EMAIL in the .env file. For Gmail, use a Google App Password, not your normal account password. Restart the server after saving .env.'
        )
        return redirect('/')

    if email_status == EMAIL_MISSING_OWNER:
        messages.error(
            request,
            'Claim failed because the item owner does not have a registered email address.'
        )
        return redirect('/')

    if email_status == EMAIL_SEND_FAILED:
        messages.error(
            request,
            'Claim failed because the notification email could not be sent. Check that EMAIL_HOST_USER and DEFAULT_FROM_EMAIL match the sender Gmail, and that EMAIL_HOST_PASSWORD is a valid Google App Password. Restart the server after changing .env.'
        )
        return redirect('/')

    if email_status != EMAIL_SENT:
        messages.error(
            request,
            'Claim failed because the owner could not be notified by email.'
        )
        return redirect('/')

    item.claimed=True

    item.claimed_by=request.user

    item.save()

    messages.success(
        request,
        'Item claimed successfully. The owner has been notified by email.'
    )

    return redirect('/')

def signup(request):

    if request.method=='POST':

        form=StudentSignUpForm(
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

        form=StudentSignUpForm()

    return render(
        request,
        'items/signup.html',
        {'form':form}
    )
