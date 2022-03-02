from django.urls import reverse
from django.views.generic import ListView


class BrowseView(ListView):
    """
    Render the browse page with desired model.
    On heritance need to change model, name, filter_queryset.
    Can change option, active, get_data when needed
    """

    model = None
    template_name = "songs/browse.html"
    paginate_by = 100
    name = None
    active = None
    options = """
        <option value="id">id</option>
        <option value="name">Nom</option>
    """

    def filter_queryset(self):
        return self.model.objects

    def get_queryset(self):
        order_val = self.request.GET.get("order", "id")

        queryset = self.filter_queryset().order_by(order_val)

        return queryset

    def get_data(self, item):
        """
        Returns data to fill the card.

        Needs to return id, image_link and a name
        """

        return item.id, item.imageUrl, item.name

    def get_cards(self):
        cards = ""
        for item in self.paginate_queryset(self.get_queryset(), self.paginate_by)[2]:
            id, image_url, name = self.get_data(item)
            card = f"""
            <div style="margin: 0 5px">
                <a href="{reverse(self.model.__name__.lower(), args=[id])}">
                    <img style="width:10rem" src="{image_url}" alt="{name}">
                    <p style="text-align:center;text-overflow: ellipsis;overflow: hidden;white-space: nowrap;width:17ch">
                        {name}</p>
                </a>
            </div>
            """

            cards += card
        return cards

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        context["order"] = self.request.GET.get("order", "title")
        context["cards"] = self.get_cards()
        context["name"] = self.name
        context["active"] = self.active
        context["options"] = self.options

        get_copy = self.request.GET.copy()

        if get_copy.get("page"):
            get_copy.pop("page")

        context["get_copy"] = get_copy

        return context
