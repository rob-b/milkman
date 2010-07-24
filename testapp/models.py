from django.db import models

class Root(models.Model):
    big_integer = models.BigIntegerField(blank=False, null=False)
    name = models.CharField(blank=False, null=False,max_length=16)
    boolean = models.BooleanField(blank=False, null=False)
    csi = models.CommaSeparatedIntegerField(blank=False, null=False, max_length=12)
    df = models.DateField(blank=False, null=False)
    dt = models.DateTimeField(blank=False, null=False)
    decimal = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=4)
    email = models.EmailField(blank=False, null=False)
    # = models.FileField(blank=False, null=False)
    # = models.FilePathField(blank=False, null=False)
    my_float = models.FloatField(blank=False, null=False)
    # = models.ImageField(blank=False, null=False)
    integer = models.IntegerField(blank=False, null=False)
    ip = models.IPAddressField(blank=False, null=False)
    null_boolean = models.NullBooleanField(blank=False, null=False)
    positive_integer = models.PositiveIntegerField(blank=False, null=False)
    small_positive_integer = models.PositiveSmallIntegerField(blank=False, null=False)
    s = models.SlugField(blank=False, null=False)
    small_integer = models.SmallIntegerField(blank=False, null=False)
    # = models.TextField(blank=False, null=False)
    mytime = models.TimeField(blank=False, null=False)
    # = models.URLField(blank=False, null=False)
    # = models.XMLField(blank=False, null=False)


class Child(models.Model):
    name = models.CharField(blank=False, null=False, max_length=16)
    root = models.ForeignKey(Root, blank=False, null=False)

class Sibling(models.Model):
    name = models.CharField(blank=False, null=False, max_length=16)
    root = models.ForeignKey(Root, blank=True, null=True)

class GrandChild(models.Model):
    name = models.CharField(blank=False, null=False, max_length=16)
    parent = models.ForeignKey(Child)

class Uncle(models.Model):
    name = models.CharField(blank=False, null=False, max_length=16)

class Aunt(models.Model):
    name = models.CharField(blank=False, null=False, max_length=16)
    uncles = models.ManyToManyField(Uncle, blank=False, null=False)