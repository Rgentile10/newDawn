from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin


# Create your models here.

# Here, each model is represented by a class that subclasses or is the child of django.db.models.Model

# Each model has a number of class variables, each of which represents a database field in the model.

# each field is associated with a field class e.g. CharField for character fields and DateTimeField for datetimes. this tells django the datatype of the attribute/field for the model class

# Fortunately, there’s a little bug in the polls application for us to fix right away: the Question.was_published_recently() method returns True
# if the Question was published within the last day (which is correct) but also if the Question’s pub_date field is in the future (which certainly isn’t).


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # here we are renaming the field data type to "date published", the databasd will use this as the column or attribute name
    pub_date = models.DateTimeField('date published')

    def __str__(self):  # constructor string
        return self.question_text

    @admin.display(boolean=True,
                   ordering='pub_date',
                   description='Published recently?')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def was_published_recently(self):
        now = timezone.now()

        # if the pub date before (within 1 day ) is before your your
        return now >= self.pub_date >= now - datetime.timedelta(days=1)


class Choice(models.Model):
    # assigning question as the foreign key this tells django that each choice is related to a single question. Django Supports all commmon database relatinooships like many to one, many to many, one to many!
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)  # default value for 0 votes

    def __str__(self):
        return self.choice_text
    

class Comments(models.Model):
    # assigning question as the foreign key this tells django that each comment is related to a single question. Django Supports all commmon database relatinooships like many to one, many to many, one to many!
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title_field = models.CharField(max_length = 100)
    text_field = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title_field
    
