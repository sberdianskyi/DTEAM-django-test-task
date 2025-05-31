from django.db import models


class CV(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Skill(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)  # e.g. Beginner, Intermediate, Expert

    def __str__(self):
        return self.name


class Project(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    description = models.TextField()
    technologies = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="contacts")
    type = models.CharField(max_length=50)  # e.g. Email, Phone, LinkedIn
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type}: {self.value}"
