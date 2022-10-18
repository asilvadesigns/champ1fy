from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('champs/', views.ChampionList.as_view(), name="champion_list"),
    path('champs/new/', views.ChampionCreate.as_view(), name="champion_create"),
    path('champs/<int:pk>/', views.ChampionDetail.as_view(), name="champion_detail"),
    path('champs/<int:pk>/update',
         views.ChampionUpdate.as_view(), name="champion_update"),
    path('champs/<int:pk>/delete',
         views.ChampionDelete.as_view(), name="champion_delete"),
    path('champs/<int:pk>/songs/new/',
         views.SongCreate.as_view(), name="song_create"),
    path('playlists/<int:pk>/songs/<int:song_pk>/',
         views.PlaylistSongAssoc.as_view(), name="playlist_song_assoc"),
    path('accounts/signup/', views.Signup.as_view(), name="signup")
]
