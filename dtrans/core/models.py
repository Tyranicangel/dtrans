from django.db import models
from model_utils.models import TimeStampedModel
from users.models import User


class Designs(TimeStampedModel):
	customer=models.CharField(max_length=100)
	referenceno=models.CharField(max_length=100)
	rating=models.CharField(max_length=20)
	voltagelv=models.CharField(max_length=20)
	voltagehv=models.CharField(max_length=20)
	connection=models.CharField(max_length=20)

class Revisions(TimeStampedModel):
	noloadloss=models.DecimalField(max_digits=20,decimal_places=3)
	loadloss=models.DecimalField(max_digits=20,decimal_places=3)
	impedance=models.DecimalField(max_digits=20,decimal_places=3)
	costing=models.DecimalField(max_digits=20,decimal_places=3)
	revisionno=models.IntegerField()
	designdata=models.TextField()
	remarks=models.TextField()
	designid=models.ForeignKey(Designs,related_name='design_id')
	revisionuser=models.ForeignKey(User,related_name='revision_user')

class Factor(TimeStampedModel):
	core = models.CharField(max_length=20)
	flux = models.CharField(max_length=20)
	frequency = models.CharField(max_length=20)
	factor = models.CharField(max_length=20)

class Conductors(TimeStampedModel):
	width = models.CharField(max_length=20)
	thickness = models.CharField(max_length=20)
	factor = models.CharField(max_length=20)
	area = models.CharField(max_length=20)

class Eddys(TimeStampedModel):
	thickness = models.CharField(max_length=20)
	parallels = models.CharField(max_length=20)
	factor = models.CharField(max_length=20)

class Radiators(TimeStampedModel):
	pannel = models.CharField(max_length=20)
	length = models.CharField(max_length=20)
	sarea_sec = models.CharField(max_length=20)
	deg35 = models.CharField(max_length=20)
	deg40 = models.CharField(max_length=20)
	deg45 = models.CharField(max_length=20)
	deg50 = models.CharField(max_length=20)
	deg55 = models.CharField(max_length=20)
	deg60 = models.CharField(max_length=20)
	wt_sec = models.CharField(max_length=20)
	oil_sec = models.CharField(max_length=20)

class Vertical(TimeStampedModel):
	vertdist = models.CharField(max_length=20)
	factor = models.CharField(max_length=20)

class Horizontal(TimeStampedModel):
	pannel=models.CharField(max_length=20)
	horzdist=models.CharField(max_length=20)
	factor=models.CharField(max_length=20)

class Fins(TimeStampedModel):
	nums=models.CharField(max_length=20)
	factor=models.CharField(max_length=20)