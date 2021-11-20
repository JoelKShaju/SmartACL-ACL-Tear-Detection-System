from django.db import models
import datetime

class User(models.Model):
    emailid= models.CharField(max_length=100,primary_key=True)
    fname= models.CharField(max_length=100, default='none')
    pwd = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.emailid)
    class Meta:
        db_table="userdetails"

class savetodb(models.Model):
    emailid = models.EmailField()
    axial = models.BinaryField(blank=True)
    cor = models.BinaryField(blank=True)
    sag = models.BinaryField(blank=True)
    aclstatus = models.CharField(max_length= 100, default='none')
    updated = models.DateTimeField(default = datetime.datetime.now())
    class Meta:
        db_table="savetodb"



	

 