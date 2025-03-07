from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address= models.CharField(max_length=3000)
    gender= models.CharField(max_length=30)

class energy_demand_prediction(models.Model):

    Fid= models.CharField(max_length=3000)
    Station_Name= models.CharField(max_length=3000)
    Start_Date= models.CharField(max_length=3000)
    End_Date= models.CharField(max_length=3000)
    Total_Duration_hh_mm_ss= models.CharField(max_length=3000)
    Charging_Time_hh_mm_ss= models.CharField(max_length=3000)
    Energy_kWh= models.CharField(max_length=3000)
    Port_Number= models.CharField(max_length=3000)
    Plug_Type= models.CharField(max_length=3000)
    Address1= models.CharField(max_length=3000)
    City= models.CharField(max_length=3000)
    State_Province= models.CharField(max_length=3000)
    Country= models.CharField(max_length=3000)
    Latitude= models.CharField(max_length=3000)
    Longitude= models.CharField(max_length=3000)
    Fee_USD= models.CharField(max_length=3000)
    Ended_By= models.CharField(max_length=3000)
    Make= models.CharField(max_length=3000)
    Model= models.CharField(max_length=3000)
    Vehicle_Type= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



