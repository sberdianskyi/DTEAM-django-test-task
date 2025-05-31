from django.contrib import admin
from .models import CV, Skill, Project, Contact


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")
    inlines = [SkillInline, ProjectInline, ContactInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "cv")
    list_filter = ("level",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "technologies", "start_date", "end_date", "cv")
    list_filter = ("start_date", "end_date")
    search_fields = ("name", "technologies")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("type", "value", "cv")
    list_filter = ("type",)
    search_fields = ("value",)
