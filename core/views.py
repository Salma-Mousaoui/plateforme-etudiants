"""
Views for the core app.
"""

from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = "core/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Elan - Moroccan Students in Spain"
        context["services"] = [
            {
                "icon": "building",
                "title": "Housing",
                "description": "Find verified rooms and apartments in Spain",
                "url": "/housing/",
            },
            {
                "icon": "journal-text",
                "title": "Counselors",
                "description": "University and academic degree advice",
                "url": "/counselors/",
            },
            {
                "icon": "briefcase",
                "title": "Lawyers",
                "description": "Immigration lawyers, certified and verified",
                "url": "/lawyers/",
            },
            {
                "icon": "chat-dots",
                "title": "Community",
                "description": "Chat with Moroccan students across Spain",
                "url": "/chat/",
            },
        ]
        return context
