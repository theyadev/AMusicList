from django import forms


class AddForm(forms.Form):
    query = forms.CharField()
    type = forms.ChoiceField(choices=[("track", "Titre"),("album", "Album"),("playlist", "Playlist")])
