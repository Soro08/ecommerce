from django.db import models

# Create your models here.

class Articles(models.Model):   
    emarque = models.CharField(max_length=255) 
    adescription = models.CharField(max_length=15) 
    aprix = models.CharField(max_length=255) 
    acouleur = models.CharField(max_length=255) 
    atail = models.CharField(max_length=255) 
    aliens = models.TextField() 
    acles = models.TextField() 
    aimg = models.TextField() 
    asource = models.CharField(max_length=255)
    acreated_at = models.DateTimeField(auto_now_add=True)
    aupdated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
    	return self.adescription

class Recherche(models.Model):
    rmot = models.TextField()
    rsite = models.CharField(max_length=255)
    rcreated_at = models.DateTimeField(auto_now_add=True)
    rupdated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
    	return self.rmot

