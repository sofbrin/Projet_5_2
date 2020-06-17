from django.db import models


class CategoryDb(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductDb(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    origin = models.TextField()
    manufacturing_places = models.TextField()
    countries = models.CharField(max_length=255)
    store = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=5)
    url = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryDb, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HistoricDb(models.Model):
    product_original = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='product_original')
    product_replaceable = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='product_replaceable')
