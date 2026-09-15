from django.db import models

# Create your models here.
class AgencyRequest(models.Model):
    #First define the choices for dropdowns
    DEVELOPER_CHOICES = [
        #(db_value , display value)
        ("kabil" , "Kabil Raya"),
        ("john" , "John Doe"),
        ("sam", "Sam Jackson")
    ]
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
    developer = models.CharField(max_length=100 , choices=DEVELOPER_CHOICES)
    module_name = models.CharField(max_length=100)
    bid_type = models.CharField(max_length=50,choices=BID_TYPE_CHOICES)
    procurement_type = models.CharField(max_length = 100 , choices = PROCUREMENT_TYPE_CHOICES)
    comments = models.TextField(blank = True)
    main_bid_link = models.URLField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    has_bids = models.CharField(max_length=10, choices = HAS_BID_CHOICES, default=False)
    
