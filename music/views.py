from django.shortcuts import render , redirect , get_object_or_404 
from django.contrib import messages
from .forms import RegisterForm ,AlbumForm, SongForm
from .models import Album , Song
from django.urls import reverse_lazy
from django.views.generic import DetailView,ListView, DeleteView
from django.db.models import Q

def home(request):
    albums = Album.objects.all()
    songs = Song.objects.all()
    return render (request, 'music/home.html', {'songs':songs,"all_albums":albums})

class albums(ListView):
    model = Album
    template_name = "music/albums.html"
    context_object_name = "all_albums"
    def get_queryset(self):
        return  Album.objects.all()

def albumCreate(request):
    if not request.user.is_authenticated:
        return redirect('albums')

    form = AlbumForm()
    if request.POST:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            form = AlbumForm()
            return redirect('profile')

    return render(request, 'music/album_form.html', {'form':form})

def album_is_public(request , album_id):
    if not request.user.is_authenticated:
        return redirect ('login')
    album = get_object_or_404(Album,pk=album_id)
    if album.is_public == False :
        album.is_public = True
    else :
        album.is_public = False
    album.save()
    songs = album.song_set.all()
    for song in songs :
        if song.is_public == False :
            song.is_public = True
            song.save()
        else :
            song.is_public = False
            song.save()
    return render (request , 'music/profile.html',{'album':album})

class DeleteAlbum(DeleteView):
    model = Album
    pk_url_kwarg = 'id'

    success_url = reverse_lazy('profile')

class detailView(DetailView):
    model = Album
    template_name = 'music/detail.html'
    pk_url_kwarg = 'id'   

def CreateSong(request , id):
    form = SongForm(request.POST or None , request.FILES)
    album = get_object_or_404(Album,pk=id)
    if form.is_valid():
        album_songs = album.song_set.all()
        for s in album_songs :
            if s.title == form.cleaned_data.get("title"):
                context={'form':form , 'album':album , 'error_message':'You already made that song !'}
                return render(request, 'music/song_form.html', context)
        song = form.save(commit=False)
        song.album = album
        song.song_file = request.FILES['song_file']
        file_type = song.song_file.url.split('.')[-1].lower()
        AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
        if file_type not in AUDIO_FILE_TYPES : 
            context={'form':form , 'album':album , 'error_message':'Audio file must be WAV, MP3, or OGG'}
            return render(request, 'music/song_form.html', context)
        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context={'form':form , 'album':album }
    return render(request, 'music/song_form.html', context) 

def DeleteSong(request , album_id ,song_id):
    album = get_object_or_404(Album,pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request , 'music/detail.html',{'album':album})

def song_is_public(request , album_id , song_id):
    if not request.user.is_authenticated:
        return redirect ('login')
    album = get_object_or_404(Album,pk=album_id)
    song = Song.objects.get(pk=song_id)
    if song.is_public == False :
        song.is_public = True
    else :
        song.is_public = False
    album.save()
    song.save()
    return render (request , 'music/detail.html',{'album':album})

def song_is_favorite(request , album_id , song_id):
    if not request.user.is_authenticated:
        return redirect('login')
    album = get_object_or_404(Album,pk=album_id)
    song = Song.objects.get(pk=song_id)
    if song.is_favorite == False :
        song.is_favorite = True
    else :
        song.is_favorite = False
    song.save()
    return render(request , 'music/detail.html',{'album':album})

def filter(request):
    songs = Song.objects.all()
    x='0'
    if request.POST :
        if request.POST.get('favorite') == "True" :
            x='1'
            songs = Song.objects.filter(is_favorite=request.POST.get('favorite'))

    return render (request, 'music/filter.html', {'songs':songs,'x':x})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect ('login')
    else:
        form = RegisterForm()
    return render (request, 'music/register.html', {'form': form}) 

class profile(ListView):
    model = Album
    template_name = "music/profile.html"
    context_object_name = "all_albums"
    def get_queryset(self):
        return  Album.objects.all()  

def getQuerySet(query=None):
    query_set = []
    for q in query.split(" "): 
        posts = Song.objects.filter(Q(title__icontains=q)).distinct()
        for post in posts:
            query_set.append(post)

    return list(set(query_set)) 