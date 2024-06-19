from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image


# Create your views here.
@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        # form is sent
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image added successfully")
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())

    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    context = {"section": "images", "form": form}
    return render(request, "images/image/create.html", context)


# image details
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    context = {"section": "images", "image": image}
    return render(request, "images/image/detail.html", context)
