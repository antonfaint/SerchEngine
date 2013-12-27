# -*- coding: utf-8 -*-
from django.db import models

class Book(models.Model):
    source_file = models.FileField(upload_to='source_documents/%Y/%m/%d')
    target_file = models.FileField(upload_to='target_documents/%Y/%m/%d')
# Create your models here.
