# -*- coding: utf-8 -*-
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    docfile2 = models.FileField(upload_to='documents2/%Y/%m/%d')

