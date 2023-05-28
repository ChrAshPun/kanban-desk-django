from project.models import Project

class GetFirstProjectMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_project = Project.objects.filter(owner=self.request.user).first()
        if (first_project):
          context['first_project'] = first_project
        else:
          context['first_project'] = -1
        return context
