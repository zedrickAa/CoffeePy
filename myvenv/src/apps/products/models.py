from django.db import models

class ProductType(models.Model):
    """Defines product types like breakfast, salads, meals or beverages."""

    name = models.CharField(max_length=60)
    description = models.TextField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Defines ingredients for products."""

    UNIT_CHOICES = [
        ("L", "litres"),
        ("lb", "pound"),
        ("mL", "mililitres"),
        ("g", "grams"),
        ("gal", "gallon"),
        ("kg", "kilograms"),
        ("oz", "ounces"),
        ("unit", "unit"),
    ]
    name = models.CharField(max_length=60)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    expiration_date = models.DateField()
    stock = models.IntegerField()
    unit_quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=4, choices=UNIT_CHOICES)

    def __str__(self):
        return self.name + " " + str(self.unit_quantity) + " " + self.unit

class Product(models.Model):
    """Defines products for sale."""

    image = models.ImageField(upload_to="products")
    product_type = models.ForeignKey(ProductType, on_delete = models.PROTECT)
    name = models.CharField(max_length=60)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, through="Recipe")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return u'/products/%d' % self.id 


class Recipe(models.Model):
    """Defines how much ingredients needs each product."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit_quantity = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.product.name