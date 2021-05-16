from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    NAME = models.TextField()
    DESCRIPTION = models.TextField()

    def __str__(self):
        return self.NAME + "," + self.DESCRIPTION


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    TRUCK = 'truck'
    SEDAN = 'sedan'
    SUV = 'suv'
    SPORT = 'sport'
    TYPE_CHOICES= [
        (TRUCK, 'Truck'),
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (SPORT, 'Sport'),
    ]


    CARMODEL = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    DEALER_ID= models.IntegerField()
    NAME= models.TextField()
    TYPE= models.CharField(max_length=15, choices=TYPE_CHOICES)
    YEAR= models.DateField()

    def __str__(self):
        return self.YEAR +" "+ self.NAME +" "+ self.TYPE
# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
