from django.db import models


class Package(models.Model):
    """Dynamic pricing package model"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)
    is_popular = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PackageFeature(models.Model):
    """Feature included or excluded in a package"""
    package = models.ForeignKey(Package, related_name='features', on_delete=models.CASCADE)
    feature_text = models.CharField(max_length=200)
    is_included = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.feature_text} for {self.package.name}"
