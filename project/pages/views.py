from django.views.generic import TemplateView
from django.shortcuts import render


class AgenciesListView(TemplateView):
    template_name = "pages/agencies_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resources = [
            {
                "name": "Госуслуги",
                "description": "Госуслуги — это единый портал, предоставляющий гражданам возможность получать доступ к государственным и муниципальным услугам через интернет. На сайте можно подать заявления, запросить информацию, зарегистрировать документы и совершить другие важные действия.",
                "url": "https://www.gosuslugi.ru",
            },
            {
                "name": "ГАС Правосудие",
                "description": "Государственная автоматизированная система Правосудие, предназначена для обеспечения доступа к информации о судебных актах и гражданских делах в России.",
                "url": "https://ej.sudrf.ru/",
            },
            {
                "name": "Портал мировых судей",
                "description": "Официальный портал для поиска информации о мировых судах, судебных актах, а также для подачи заявлений и обращения в суды.",
                "url": "https://mos-sud.ru/",
            },
            {
                "name": "Мосгорсуд",
                "description": "Московский городской суд, занимающийся рассмотрением дел в первой инстанции. Портал для доступа к судебной информации и онлайн-сервисам.",
                "url": "https://mos-gorsud.ru/",
            },
        ]
        context["resources"] = resources
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)