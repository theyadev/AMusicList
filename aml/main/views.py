from django.shortcuts import render
from django.views import View
from django.templatetags.static import static


from users.models import Activities


class MainView(View):
    template_name = "main/index.html"
    template_name_logged = "users/logged_index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_list = [request.user]
            user_list.extend(request.user.follows.all())

            activites = Activities.objects.filter(user__in=user_list)
            activites = sorted(
                activites, key=lambda activity: activity.date, reverse=True
            )

            activites_html = ""

            for activity in activites:
                song_html = f'<a href="/song/{ activity.song.id }">{ activity.song.title }</a>'

                if activity.action == "ADDED":
                    text_html = f"a ajouté {song_html} à sa liste !"
                elif activity.action == "REMOVED":
                    text_html = f"a retiré {song_html} de sa liste !"
                elif activity.action == "ADDED FAVOURITE":
                    text_html = f"a ajouté {song_html} à ses favoris !"
                elif activity.action == "REMOVED FAVOURITE":
                    text_html = f"a retiré {song_html} de ses favoris !"

                html = f"""
                <div class="card">
                    <img src="{activity.song.imageUrl}" alt="">
                    <div class="card-content">
                        <a href="/user/{activity.user.id}">{activity.user.username}</a>
                        <p class="card-text">{text_html}</p>
                        <img class="card-avatar" src="{static('avatar.png')}" alt="{activity.user.username}">
                    </div> 
                </div>"""

                activites_html += html

            context = {
                "activities": activites_html,
                "list": request.user.list.all()[:4],
            }

            return render(request, self.template_name_logged, context)

        return render(request, self.template_name)
