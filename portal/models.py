from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from ckeditor.fields import RichTextField


class User(AbstractUser):
    is_employer = models.BooleanField('Is Employer', default=False)
    is_employee = models.BooleanField('Is Employee', default=False)
    REGIONS_CHOICES = [
    ('Ashanti', 'Ashanti Region'),
    ('Brong', 'Brong Region'),
    ('Central', 'Central Region '),
    ('Eastern', 'Eastern Region '),
    ('Greater_Accra', 'Greater Accra Region'),
    ('Northern', 'Northern Region '),
    ('Savannah', 'Savannah Region '),
    ('North_east', 'North-East Region '),
    ('Upper_east', 'Upper East Region '),
    ('Bono_east', 'Bono East Region '),
    ('Ahafo', 'Ahafo Region '),
    ('Oti', 'Oti Region '),
    ('Volta', 'Volta Region'),
    ('Western', 'Western Region'),
    ('Western_north', 'Western North Region'),
    ('Upper_west', 'Upper West Region '),
]
    region = models.CharField(max_length=20, choices=REGIONS_CHOICES)


from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
class contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=500)
    message = models.TextField(max_length=10000)

    def __str__(self):
        return self.name + '  || ' + self.email 

    def save(self, *args, **kwargs):
        super(contact, self).save(*args, **kwargs)
        account_sid = 'ACa152b6b76837e48b0c4aae323308885e'
        auth_token = '050ebc36590adfc555bb1413adf95a74'
        twilio_phone_number = '+14848785778'
        recipient_phone_number = '+233200036801'
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_=twilio_phone_number,
                body='Hello, you have a new message from: {}\n{}'.format(self.name, self.message),
                to=recipient_phone_number
            )

            print("Message SID:", message.sid)

        except TwilioRestException as e:
            print("Twilio error:", e)
        return self
    

class sectioned(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name





class job_time(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




from hitcount.models import HitCountMixin, HitCount

class PostJobHitCount(models.Model):
    hit_count = models.OneToOneField(HitCount, on_delete=models.CASCADE)
    post = models.ForeignKey('post_job', on_delete=models.CASCADE)


class post_job(models.Model):
    job_title = models.CharField(max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description = RichTextField()
    responsibilities = RichTextField()
    qualifications = RichTextField()
    REGIONS_CHOICES = [
    ('Ashanti', 'Ashanti Region'),
    ('Brong', 'Brong Region'),
    ('Central', 'Central Region '),
    ('Eastern', 'Eastern Region '),
    ('Greater_Accra', 'Greater Accra Region'),
    ('Northern', 'Northern Region '),
    ('Savannah', 'Savannah Region '),
    ('North_east', 'North-East Region '),
    ('Upper_east', 'Upper East Region '),
    ('Bono_east', 'Bono East Region '),
    ('Ahafo', 'Ahafo Region '),
    ('Oti', 'Oti Region '),
    ('Volta', 'Volta Region'),
    ('Western', 'Western Region'),
    ('Western_north', 'Western North Region'),
    ('Upper_west', 'Upper West Region '),
]
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Any', 'Any'),
        
    ]
    sex = models.CharField(max_length=20, choices=GENDER)
    time = models.ForeignKey(job_time, on_delete=models.CASCADE)
    location = models.CharField(max_length=500)
    region = models.CharField(max_length=20, choices=REGIONS_CHOICES)
    deadline = models.DateTimeField()
    post_date = models.DateTimeField(auto_now_add=True, auto_created=True)
    job_for = models.ForeignKey(sectioned, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=600)
    company_address = models.CharField(max_length=600)
    company_email = models.EmailField(max_length=600)
    company_number = models.IntegerField()
    company_image = models.ImageField(upload_to="images/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    approved = models.BooleanField('Approved', default=False)
    view_count = models.PositiveIntegerField(default=0)

    def increment_view_count(self):
        self.view_count += 1
        self.save()


    def save(self, *args, **kwargs):
        if not self.hit_count_generic:
            hit_count, created = HitCount.objects.get_or_create(content_object=self)
            self.hit_count_generic = hit_count
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.location = self.location.capitalize()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job_title} (posted by {self.user.username}) {self.approved}"

    def save(self, *args, **kwargs):
        self.location = self.location.capitalize()  
        super().save(*args, **kwargs)

    def send_sms_notification(self, recipient_phone_number):
        if recipient_phone_number:
            account_sid = 'ACa152b6b76837e48b0c4aae323308885e'
            auth_token = '050ebc36590adfc555bb1413adf95a74'
            twilio_phone_number = '+14848785778'  

            try:
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    from_=twilio_phone_number,
                    body='Your job has been posted successfully!',
                    to=str(recipient_phone_number) 
                )

                print("Message SID:", message.sid)

            except TwilioRestException as e:
                print("Twilio error:", e)

    def __str__(self):
        return f"{self.job_title} (posted by {self.user.username})"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    job_post = models.ForeignKey(post_job, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.username}, To: {self.receiver.username}, Job Post: {self.job_post.job_title}"



class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=600)
    address = models.CharField(max_length=600)
    email = models.EmailField(max_length=600)
    number = models.IntegerField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} (profile for {self.user.username})"




class report_job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    email_address = models.EmailField(max_length=900)
    contact =  models.IntegerField()
    comment = models.TextField(max_length=1000)
    posts = models.ForeignKey(post_job, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment + " " + str(self.posts)
    

    

class apply_job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    email = models.EmailField(max_length=200)
    number = models.IntegerField()
    cv = models.FileField()
    information = models.TextField(blank=True, max_length=3000)
    job = models.ForeignKey(post_job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.email} - {self.job.job_title}"







class details(models.Model):
    name = models.ForeignKey(post_job, on_delete=models.CASCADE)

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class skilled_companies(models.Model):
    AVAILABILITY_CHOICES = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
    )
    REGIONS_CHOICES = [
    ('Ashanti', 'Ashanti Region'),
    ('Brong', 'Brong Region'),
    ('Central', 'Central Region '),
    ('Eastern', 'Eastern Region '),
    ('Greater_Accra', 'Greater Accra Region'),
    ('Northern', 'Northern Region '),
    ('Savannah', 'Savannah Region '),
    ('North_east', 'North-East Region '),
    ('Upper_east', 'Upper East Region '),
    ('Bono_east', 'Bono East Region '),
    ('Ahafo', 'Ahafo Region '),
    ('Oti', 'Oti Region '),
    ('Volta', 'Volta Region'),
    ('Western', 'Western Region'),
    ('Western_north', 'Western North Region'),
    ('Upper_west', 'Upper West Region '),
]
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    region = models.CharField(max_length=20, choices=REGIONS_CHOICES)
    phone_number = models.IntegerField()
    logo = models.ImageField()
    email = models.EmailField()
    services  = models.CharField(max_length=2000)
    description = models.TextField()
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)
    approved = models.BooleanField('Approved', default=False)




    def __str__(self):
        return self.name + ' ' + self.location
    



class CompanyRating(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    company = models.ForeignKey(skilled_companies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = ('company', 'user')







from django.db import models
from django.utils import timezone

class skilled_individuals(models.Model):
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    AVAILABILITY_CHOICES = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
    )
    REGIONS_CHOICES = [
    ('Ashanti', 'Ashanti Region'),
    ('Brong', 'Brong Region'),
    ('Central', 'Central Region '),
    ('Eastern', 'Eastern Region '),
    ('Greater_Accra', 'Greater Accra Region'),
    ('Northern', 'Northern Region '),
    ('Savannah', 'Savannah Region '),
    ('North_east', 'North-East Region '),
    ('Upper_east', 'Upper East Region '),
    ('Bono_east', 'Bono East Region '),
    ('Ahafo', 'Ahafo Region '),
    ('Oti', 'Oti Region '),
    ('Volta', 'Volta Region'),
    ('Western', 'Western Region'),
    ('Western_north', 'Western North Region'),
    ('Upper_west', 'Upper West Region '),
]
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=20, choices=REGIONS_CHOICES)
    location = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    email = models.EmailField()
    services = models.CharField(max_length=2000)
    description = models.TextField()
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    posted_date = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField('Approved', default=False)


    def __str__(self):
        return self.name + ' || ' + self.location

    def save(self, *args, **kwargs):
        if not self.id:  
            self.posted_date = timezone.now()
        super().save(*args, **kwargs)
        
class skilled_ind_Comment(models.Model):
    ind = models.ForeignKey(skilled_individuals, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name + ' || ' + self.email   
        
        
        
class IndividualRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(skilled_individuals, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'company')

    
    
class Comment(models.Model):
    company = models.ForeignKey(skilled_companies, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.company)








class CompanyRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(skilled_companies, on_delete=models.CASCADE, related_name='company_ratings')
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'company')

class Comments(models.Model):
    company = models.ForeignKey(skilled_individuals, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)





import secrets
from .paystack import PayStack



class Payment(models.Model):
    amount = models.PositiveIntegerField()
    email = models.EmailField()
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    job_id = models.IntegerField(default=0) 

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"{self.email} - {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            self.paystack_response = result
            if result["amount"] / 100 == self.amount:
                self.completed = True
            self.save()
            return True
        return False
    
    

class MultipleImages(models.Model):
    post = models.ForeignKey(skilled_individuals, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='skilled_individual_images/')

    def __str__(self):
        return self.post.title
        
class MultipleImages(models.Model):
    post = models.ForeignKey(skilled_companies, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='skilled_company_images/')


