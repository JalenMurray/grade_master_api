from django.db import models
from django.db.models import Model, CharField, DateTimeField, EmailField, IntegerField, FloatField,\
    ForeignKey, BooleanField


class User(Model):
    username = CharField(max_length=50)
    display_name = CharField(max_length=200)
    email = EmailField()
    created_at = DateTimeField()

    def __str__(self):
        return self.username


class Semester(Model):
    season = CharField(max_length=7, choices=[('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall'),
                                              ('Winter', 'Winter')])
    year = IntegerField()
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='semesters')

    def __str__(self):
        return f'{self.season} {self.year}'


class Class(Model):
    code = CharField(max_length=20)
    title = CharField(max_length=255)
    semester = ForeignKey(Semester, on_delete=models.CASCADE, related_name='classes')
    desired_score = FloatField(default=100.0)
    units = IntegerField(verbose_name="Units/Credits")
    display_color = CharField(max_length=10, default='#23447d')

    def __str__(self):
        return f'{self.code}-{self.semester}'

    @property
    def score(self):
        a_types = AssignmentType.objects.filter(class_associated=self)
        score = 0.0

        for at in a_types:
            assignments = Assignment.objects.filter(assignment_type=at)
            for a in assignments:
                if at.max_score > 0:
                    weighted_score = (a.score / a.max_score) * a.weight
                    score += weighted_score
        return score


class AssignmentType(Model):
    name = CharField(max_length=100)
    max_score = FloatField(blank=True, null=True, default=100.0)
    weight = FloatField(blank=True, null=True)
    class_associated = ForeignKey(Class, on_delete=models.CASCADE, related_name='assignment_types')
    default_name = CharField(max_length=100)
    lock_weights = BooleanField(default=False)

    def __str__(self):
        return self.name


    @property
    def total_score(self):
        assignments = Assignment.objects.filter(assignment_type=self)
        total_score = sum((a.score / a.max_score) * a.weight for a in assignments)
        return total_score

    @property
    def max_total_score(self):
        assignments = Assignment.objects.filter(assignment_type=self)
        max_total_score = sum(a.weight for a in assignments)
        return max_total_score

    def balance_weight(self):
        if self.lock_weights:
            assignments = Assignment.objects.filter(assignment_type=self)
            num_assignments = assignments.count()
            new_weight = self.weight / num_assignments
            assignments.update(weight=new_weight)
        else:
            self.weight = sum([a.weight for a in Assignment.objects.filter(assignment_type=self)])
            self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.score = self.max_score
        if self.lock_weights:
            self.balance_weight()
        super().save(*args, **kwargs)


class Assignment(Model):
    name = CharField(max_length=100)
    score = FloatField(null=True, blank=True)
    max_score = models.FloatField(null=True, blank=True)
    weight = FloatField(blank=True, null=True)
    assignment_type = ForeignKey(AssignmentType, on_delete=models.CASCADE, related_name='assignments')

    def __str__(self):
        return f'{self.name}\t{self.score} / {self.assignment_type.max_score}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.max_score = self.assignment_type.max_score if self.assignment_type.max_score else 100.0
            self.score = self.max_score
            self.weight = 0.0
        super().save(*args, **kwargs)
        self.assignment_type.balance_weight()