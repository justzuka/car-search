from django.db import models

class Make(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=10, blank=False, null=True)

    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CarType(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    start_year = models.IntegerField(null=True, blank=False)
    end_year = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return self.name
