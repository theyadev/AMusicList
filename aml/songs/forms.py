from django import forms


class AddForm(forms.Form):
    """Form used to lookup songs/albums/playlists"""

    query = forms.CharField(label="Recherche")
    type = forms.ChoiceField(
        choices=[("track", "Titre"), ("album", "Album"), ("playlist", "Playlist")]
    )
