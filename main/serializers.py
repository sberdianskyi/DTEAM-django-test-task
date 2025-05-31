from rest_framework import serializers
from .models import CV, Skill, Project, Contact


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("name", "level")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("name", "description", "technologies", "start_date", "end_date")


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("type", "value")


class CVSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    projects = ProjectSerializer(many=True)
    contacts = ContactSerializer(many=True)

    class Meta:
        model = CV
        fields = (
            "id",
            "first_name",
            "last_name",
            "bio",
            "skills",
            "projects",
            "contacts",
        )

    def create(self, validated_data):
        skills_data = validated_data.pop("skills")
        projects_data = validated_data.pop("projects")
        contacts_data = validated_data.pop("contacts")

        cv = CV.objects.create(**validated_data)

        for skill_data in skills_data:
            Skill.objects.create(cv=cv, **skill_data)

        for project_data in projects_data:
            Project.objects.create(cv=cv, **project_data)

        for contact_data in contacts_data:
            Contact.objects.create(cv=cv, **contact_data)

        return cv
