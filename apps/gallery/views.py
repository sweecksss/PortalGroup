from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm


def is_moderator(user):
    return user.is_authenticated and (user.is_superuser or user.role in ('admin', 'moderator'))


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'gallery/album_list.html', {'albums': albums})


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    moderator = is_moderator(request.user)
    photos = album.photos.all() if moderator else album.photos.filter(is_approved=True)
    pending = album.photos.filter(is_approved=False).count() if moderator else 0
    return render(request, 'gallery/album_detail.html', {
        'album': album,
        'photos': photos,
        'is_moderator': moderator,
        'pending_count': pending,
    })


@login_required
def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.save()
            return redirect('gallery:album_detail', pk=album.pk)
    else:
        form = AlbumForm()
    return render(request, 'gallery/album_form.html', {'form': form})


@login_required
def photo_upload(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = album
            photo.uploaded_by = request.user
            # Модератор публікує одразу, решта — після перевірки.
            photo.is_approved = is_moderator(request.user)
            photo.save()
            if photo.is_approved:
                messages.success(request, 'Файл додано до альбому.')
            else:
                messages.info(request, 'Файл надіслано на перевірку модератору.')
            return redirect('gallery:album_detail', pk=album.pk)
    else:
        form = PhotoForm()
    return render(request, 'gallery/photo_form.html', {'form': form, 'album': album})


@login_required
@require_POST
def photo_approve(request, pk):
    if not is_moderator(request.user):
        raise PermissionDenied
    photo = get_object_or_404(Photo, pk=pk)
    photo.is_approved = True
    photo.save(update_fields=['is_approved'])
    messages.success(request, 'Файл схвалено та опубліковано.')
    return redirect('gallery:album_detail', pk=photo.album.pk)


@login_required
@require_POST
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if not (is_moderator(request.user) or photo.uploaded_by == request.user):
        raise PermissionDenied
    album_pk = photo.album.pk
    photo.delete()
    messages.success(request, 'Файл видалено.')
    return redirect('gallery:album_detail', pk=album_pk)
