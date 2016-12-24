from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.
class Compile(models.Model):
    code = models.CharField(max_length=1000)
    result = models.CharField(max_length=100)
    time_cost = models.CharField(max_length=10)
    
    # use __str__ on python 3.x, but python 2.x, please use __unicode__
    def __str__(self):
        return self.code
        
    def __str__(self):
        return self.result
        
    def __str__(self):
        self.time_cost
        
class CompileForm(ModelForm):
    class Meta:
        model = Compile
        fields = ('code', 'result', 'time_cost', )