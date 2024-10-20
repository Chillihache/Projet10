from django.contrib import admin
from projecthub.models import Project, Issue, Comment, Contribute


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time',)


class IssueAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time',)


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time',)


class ContributeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time',)


# Enregistrez les modèles avec leur configuration personnalisée
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contribute, ContributeAdmin)
