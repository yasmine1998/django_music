from django.contrib import admin
from django.urls import path, include
from music import views as music_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', music_views.home, name='home'),
    path('albums/', music_views.albums.as_view(), name='albums'),
    path('addalbum/',music_views.albumCreate,name="add-album"),
    path('albums/<int:album_id>/album_public/',music_views.album_is_public,name="album_public"),
    path('albums/<int:id>/delete',music_views.DeleteAlbum.as_view(),name="delete-album"),
    path('albums/profile/',music_views.profile.as_view(),name="profile"),
    path('albums/<int:id>/',music_views.detailView.as_view(),name="detail"),
    path('albums/<int:id>/addsong/',music_views.CreateSong,name="add-song"),
    path('albums/<int:album_id>/song_public/<int:song_id>/',music_views.song_is_public,name="song_public"),
    path('albums/<int:album_id>/song_favorite/<int:song_id>/',music_views.song_is_favorite,name="song_favorite"),
    path('albums/<int:album_id>/DeleteSong/<int:song_id>',music_views.DeleteSong,name="song-delete"),

    path('albums/filter/',music_views.filter,name="filter"),
    path('login/', auth_views.LoginView.as_view(template_name='music/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='music/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='music/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='music/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='music/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='music/password_reset_complete.html'), name='password_reset_complete'),
    path('register/', music_views.register, name='register'),
]

#Media
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
