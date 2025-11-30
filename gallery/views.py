from django.shortcuts import render, get_object_or_404
from .models import Album

from django.shortcuts import render, get_object_or_404
from .models import Album
from datetime import datetime

def gallery_list(request):
    albums = Album.objects.filter(is_public=True)
    return render(request, 'gallery/gallery_list.html', {'albums': albums})

def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug, is_public=True)
    photos = album.photos.all()
    return render(request, 'gallery/album_detail.html', {'album': album, 'photos': photos})
