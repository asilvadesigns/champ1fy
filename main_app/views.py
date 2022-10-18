from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.views.generic.base import TemplateView
from .models import Champion, Song, Playlist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = Playlist.objects.all()
        return context


class About(TemplateView):
    template_name = "about.html"


@method_decorator(login_required, name='dispatch')
class ChampionList(TemplateView):
    template_name = "champion_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mySearchName = self.request.GET.get("champion")
        if mySearchName != None:
            context["champs"] = Champion.objects.filter(
                name__icontains=mySearchName)
            context["stuff_at_top"] = f"Searching through Champions list for {mySearchName}"
        else:
            context["champs"] = Champion.objects.filter(
                user=self.request.user)
            context["stuff_at_top"] = "Champions"
        return context


@method_decorator(login_required, name='dispatch')
class ChampionCreate(CreateView):
    model = Champion
    fields = ['champion', 'image', 'bio', 'favorite_champion']
    template_name = "champion_create.html"

    def form_valid(self, form):

        form.instance.user = self.request.user

        return super(ChampionCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('champion_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class ChampionDetail(DetailView):
    model = Champion
    template_name = "champion_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = Playlist.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class ChampionUpdate(UpdateView):
    model = Champion
    fields = ['champion', 'image', 'bio', 'favorite_champion']
    template_name = "champion_update.html"
    success_url = "/champs/"

    def get_success_url(self):
        return reverse('champion_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class ChampionDelete(DeleteView):
    model = Champion
    template_name = "champion_delete_confirmation.html"
    success_url = "/champs/"


@method_decorator(login_required, name='dispatch')
class SongCreate(View):

    def post(self, request, pk):
        formTitle = request.POST.get("title")
        minutes = request.POST.get("minutes")
        seconds = request.POST.get("seconds")
        formLength = 60 * int(minutes) + int(seconds)
        theChampion = Champion.objects.get(pk=pk)
        Song.objects.create(
            title=formTitle, length=formLength, champion=theChampion)
        return redirect('champion_detail', pk=pk)


class PlaylistSongAssoc(View):

    def get(self, request, pk, song_pk):
        assoc = request.GET.get("assoc")

        if assoc == "remove":
            Playlist.objects.get(pk=pk).songs.remove(song_pk)

        if assoc == "add":

            Playlist.objects.get(pk=pk).songs.add(song_pk)

        return redirect('home')


class Signup(View):
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("champion_list")
        else:
            return redirect("signup")
