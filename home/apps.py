from django.apps import AppConfig
from watson import search as watson


class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):
        projectmodel = self.get_model("Project")
        watson.register(projectmodel) #TODO watson.register(YourModel.objects.filter(is_published=True)) voor "verwijderde" projecten
