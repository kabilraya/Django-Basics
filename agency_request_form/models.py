from django.db import models

# Create your models here.

class Developer(models.Model):
    developer_name = models.CharField(max_length=100)

    def __str__(self):
        return self.developer_name #the database will return the name as a string instead of Developer Object(1)
class AgencyRequest(models.Model):
    #First define the choices for dropdowns
    
    BID_TYPE_CHOICES = [
        ("new", "New"),
        ("update" , "Update"),
    ]

    PRIORITY_CHOICES = [
        ("low","Low"),
        ("high" ,"High"),
        ("normal" , "Normal")
    ]

    PROCUREMENT_TYPE_CHOICES = [
        ("spider" , "Spider"),
        ("amr" , "AMR"),
        ("manual" , "Manual")
    ]
    HAS_BID_CHOICES = [
        ("True","Yes"),
        ("False","No")
    ]
    agency_name = models.CharField(max_length=400)
    ecgains = models.CharField(max_length = 100)
    state = models.CharField(max_length=10)
    contact_email = models.EmailField()
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE)
    module_name = models.CharField(max_length=100)
    bid_type = models.CharField(max_length=50,choices=BID_TYPE_CHOICES)
    procurement_type = models.CharField(max_length = 100 , choices = PROCUREMENT_TYPE_CHOICES)
    comments = models.TextField(blank = True)
    main_bid_link = models.URLField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    has_bids = models.CharField(max_length=10, choices = HAS_BID_CHOICES, default=False)
    
