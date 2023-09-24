from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm,MessageForm, LoginForm, contactus,CommentForm, post_job_form,PaymentForm, apply_job_form, report_job_form, CompanyProfileForm, categoryform, skilled_company_form, skilled_individual_form
from django.contrib.auth import authenticate, login,  logout
from . models import contact,post_job,Comment,Message,sectioned, Category,CompanyProfile, skilled_companies, skilled_individuals, Payment, CompanyRating
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import folium
import geocoder
from bs4 import BeautifulSoup
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from django.shortcuts import render
from django.http import HttpResponse

def print_user(request):
    if request.user.is_authenticated:
        print("Logged-in User: ", request.user)
    else:
        print("No user is logged in.")
    return HttpResponse("User printed in the terminal.")


def add_category(request):
    form = categoryform()
    if request.method == 'POST':
        form = contactus(request.POST)
        if form.is_valid():
            form.save()
            form = categoryform()
            return redirect('contact')
    return render(request,'addcategory.html',{'form':form})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully. You can now log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


from .forms import PostJobForm

def update_job_post(request, job_post_id):
    job_post = get_object_or_404(post_job, id=job_post_id)

    if request.method == 'POST':
        form = PostJobForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
    else:
        initial_data = {
            'job_title': job_post.job_title,
            'job_description': job_post.job_description,
            'responsibilities': job_post.responsibilities,
            'location': job_post.location,
            'company_address': job_post.company_address,
            'company_number': job_post.company_number,
            'company_email': job_post.company_email,
        }
        print(f"Initial Data: {initial_data}")  # Debugging line
        form = PostJobForm(instance=job_post, initial=initial_data)

    return render(request, 'update_job_post.html', {'form': form})



from django.contrib import messages

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_employer:
                login(request, user)
                return redirect('employer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
        else:
            messages.error(request, 'Invalid login')
    return render(request, 'registration/login.html', {'form': form,'messages':'messages'})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('index')


def employer(request):
    return render(request,'employer.html')


def employee(request):
    return render(request,'employee.html')



def about(request):
    return render(request, 'about.html')



from django.utils import timezone

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from .models import sectioned, post_job

def job_list(request):
    current_time = timezone.now()
    jobs = post_job.objects.filter(deadline__gt=current_time)  # Filter out jobs with deadlines in the future
    sections = sectioned.objects.all()
    query = request.GET.get('q')
    location_filter = request.GET.get('location')
    region_filter = request.GET.get('region')
    homes = jobs.filter(job_for__name="Home")
    company_jobs = jobs.filter(job_for__name="Company")

    if query:
        jobs = jobs.filter(Q(job_title__icontains=query))

    if location_filter:
        jobs = jobs.filter(Q(location__icontains=location_filter))

    if region_filter:
        jobs = jobs.filter(region=region_filter)

    return render(request, 'job-list.html', {'homes': homes, 'company_jobs': company_jobs, 'sections': sections, 'jobs': jobs})

from django.shortcuts import render, get_object_or_404, redirect
from .models import post_job, Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, report_job_form
import folium
import geocoder
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from bs4 import BeautifulSoup
from .models import post_job, Comment
from .forms import CommentForm

def job_detail(request, post_id):
    post = get_object_or_404(post_job, pk=post_id)
    post.increment_view_count()
    user_region = request.user.region
    
    # Filter jobs based on the user's region
    jobs_in_region = post_job.objects.filter(region=user_region).exclude(pk=post_id)
    
    if jobs_in_region.exists():
        # If there are jobs in the user's region, suggest two random posts from the region
        job_suggestions = jobs_in_region.order_by('?')[:2]
    else:
        # If there are no jobs in the user's region, suggest any two random posts
        all_jobs = post_job.objects.exclude(pk=post_id)
        job_suggestions = all_jobs.order_by('?')[:2]
    job_location = geocoder.osm(post.location)
    if job_location.lat is not None and job_location.lng is not None:
        job_map = folium.Map(location=[job_location.lat, job_location.lng], zoom_start=10)
        folium.Marker([job_location.lat, job_location.lng], popup=post.job_title).add_to(job_map)
        job_map = job_map._repr_html_()
    else:
        job_map = None

    if request.method == 'POST':
        report_form = report_job_form(request.POST)
        apply_form = apply_job_form(request.POST, request.FILES)
        
        if report_form.is_valid():
            report_form.save(user=request.user, post=post)
        
        elif apply_form.is_valid():
            apply_form.save(user=request.user, job=post)
    else:
        report_form = report_job_form()
        apply_form = apply_job_form()

    context = {
        'job': post,
        'job_map': job_map,
        'view_count': post.view_count,
        'report_form': report_form,
        'apply_form': apply_form,'job_suggestions': job_suggestions,
    }
    return render(request, 'job-detail.html', context)





from django.db.models import Max
from django.shortcuts import render
from django.db.models import Count, Case, When, Value, IntegerField
from django.utils import timezone
from .models import post_job, Category, skilled_individuals, skilled_companies

def index(request):
    job_post = post_job.objects.filter(deadline__gte=timezone.now()).order_by('-view_count').first()
    categories = Category.objects.annotate(
        total_jobs=Count(
            Case(
                When(post_job__approved=True, post_job__deadline__gte=timezone.now(), then=1),
                output_field=IntegerField()
            )
        )
    )[:6]

    user_region = request.user.region if request.user.is_authenticated else None
    job_posted = post_job.objects.filter(region=user_region, deadline__gte=timezone.now()).exclude(pk=job_post.pk).annotate(
    max_view_count=Max('view_count')
).order_by('-max_view_count')[:4]


    if not job_posted:
        job_posted = post_job.objects.filter(approved=True).order_by('-post_date')[1:5]

    if request.user.is_authenticated:
        highly_rated_companies = skilled_companies.objects.filter(region=user_region).annotate(
            avg_rating=Avg('company_ratings__rating')
        ).order_by('-avg_rating')[:4]
    else:
        highly_rated_companies = skilled_companies.objects.annotate(
            avg_rating=Avg('company_ratings__rating')
        ).order_by('-avg_rating')[:4]

    job_posts = post_job.objects.filter(deadline__gte=timezone.now()).order_by('-view_count')[:4]
    skilled_individuals_list = skilled_individuals.objects.all().order_by('-posted_date')[:4]
    skilled_individuals_lists = skilled_individuals.objects.order_by('posted_date').last()
    skilled_companies_list = skilled_companies.objects.all()[:4]
    highly_rated_posts = skilled_individuals.objects.annotate(
        avg_rating=Sum('ratings__rating')
    ).order_by('-avg_rating')[:4]
    highly_rated_companies = skilled_companies.objects.annotate(
        avg_rating=Sum('company_ratings__rating')
    ).order_by('-avg_rating')[:4]

    return render(request, 'index.html', {
        'categories': categories,
        'job_posts': job_posts,
        'job_posted': job_posted,
        'skilled_individuals_list': skilled_individuals_list,
        'skilled_companies_list': skilled_companies_list,
        'job_post': job_post,
        'skilled_individuals_lists': skilled_individuals_lists,
        'highly_rated_individuals': highly_rated_posts,
        'highly_rated_companies': highly_rated_companies,
        'highly_rated_companies': highly_rated_companies,
    })




from django.db.models import Q

def category(request):
    search_query = request.GET.get('search', '')

    categories = Category.objects.annotate(
        total_jobs=Count(
            Case(
                When(post_job__approved=True, post_job__deadline__gte=timezone.now(), then=1),
                output_field=IntegerField()
            )
        )
    ).filter(Q(name__icontains=search_query))

    return render(request, 'category.html', {'categories': categories})


def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    current_time = timezone.now()
    search_region = request.GET.get('region')
    search_location = request.GET.get('location')
    
    posts = post_job.objects.filter(category=category, deadline__gt=current_time)

    if search_region:
        posts = posts.filter(region=search_region)

    if search_location:
        posts = posts.filter(location__icontains=search_location)

    context = {
        'category': category,
        'posts': posts,
        'region_choices': post_job.REGIONS_CHOICES,  # Pass the choices to the context
    }
    return render(request, 'each_category.html', context)



def testimonial(request):
    return render(request,'testimonial.html')


@login_required
def profile(request):
    try:
        company_profile = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        company_profile = None
    num_jobs_posted = post_job.objects.filter(user=request.user).count()
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile)
        if form.is_valid():
            company_profile = form.save(commit=False)
            company_profile.user = request.user
            company_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CompanyProfileForm(instance=company_profile)
    context = {'form': form, 'company_profile': company_profile, 'num_jobs_posted': num_jobs_posted}
    return render(request, 'profile.html', context)



def employer_details(request):
    return render(request, 'employee_details.html')


def delete_job_post(request, pk):
    if request.user.is_authenticated:
        delete_it = post_job.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('job_list')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('index')
    



from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .forms import contactus

def contact(request):
    form = contactus()
    if request.method == 'POST':
        form = contactus(request.POST)
        if form.is_valid():
            form.save()
            
            # Get the user's email from the form
            user_email = form.cleaned_data['email']
            
            # Send the email
            subject = 'Thank you for contacting us'
            message = 'Dear user, thank you for contacting us. We will get back to you soon.'
            from_email = 'amponsahc306@gmail.com'
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('contact')
    return render(request, 'contact.html', {'form': form})




def privacy(request):
    return render(request,'privacy.html')
    

def terms(request):
    return render(request,'terms.html')
    



@login_required
def post_a_job(request):
    cat = Category.objects.all()
    obj = sectioned.objects.all()

    if request.method == 'POST':
        form = post_job_form(request.POST, request.FILES)
        if form.is_valid():
            post_job = form.save(commit=False)
            post_job.user = request.user
            recipient_phone_number = form.cleaned_data['company_number']
            post_job.save()
            post_job.send_sms_notification(recipient_phone_number)
            form = post_job_form()
            messages.success(request, 'Job posted successfully')
            return redirect('job_list')
            
    else:
        form = post_job_form()
    return render(request, 'post_a_job.html', {'form': form, 'obj': obj, 'cat': cat})


@never_cache
def map(request):
    searches = post_job.objects.all()
    m = folium.Map(location=[7.9465, -1.0232], zoom_start=7.4)
    fg = folium.FeatureGroup(name='Job locations')
    
    for search in searches:
        location = geocoder.osm(search.location)
        if location.lat is not None and location.lng is not None:
            lat = location.lat
            lng = location.lng
            country = location.country
            popup_content = f"<strong>{search.job_title}</strong><br><a href='/job_detail/{search.pk}/'>Click here to view job details</a>"
            popup_text = BeautifulSoup(popup_content, 'html.parser').get_text()
            popup = folium.Popup(popup_content, max_width=2650)
            folium.Marker([lat, lng], tooltip='click for details', popup=popup).add_to(fg)

    fg.add_to(m)
    m = m._repr_html_()
    return render(request, 'map.html', {'m': m})


    
def admin_approval(request):
    obj = post_job.objects.all().order_by('-post_date')
    if request.user.is_superuser:
       if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            obj.update(approved=False)
            for x in id_list:
                post_job.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, 'Update successful') 
            return redirect('job_list')
            
       else:
            return render(request,'admin_approval.html',{'obj': obj})
    else:
        messages.success(request, 'You are not authorized')
        return redirect('index')
    return render(request,'admin_approval.html')


from django.contrib.auth.decorators import user_passes_test
def all_jobs(request):
    obj = post_job.objects.all()
    return render(request,'all_posted_jobs.html',{'obj':obj})
    

def search_results(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        jobbs = post_job.objects.filter(job_title__contains=searched)
        if jobbs.count() == 0:
            messages.warning(request, f"No jobs found for {searched}")
        return render(request,'search_results.html',{'searched':searched, 'jobbs':jobbs})

    else:
        return render(request,'search_results.html')


def employer_job_post(request, post_id=None):
    if request.method == 'POST':
        if 'delete' in request.POST:
            job_post = get_object_or_404(post_job, id=post_id)
            job_post.delete()
        elif 'update' in request.POST:
            pass
        return redirect('employer_job_post')
    else:
        job_posts = post_job.objects.filter(user=request.user).order_by('-post_date')
        return render(request, 'employer_job_post.html', {'job_posts': job_posts})





def skilled_individual(request):
    form = skilled_individual_form()
    
    if request.method == 'POST':
        form = skilled_individual_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('skilled_individual')
    obj = skilled_individuals.objects.all().order_by('-posted_date')
    search_name = request.GET.get('search_name', '')
    search_location = request.GET.get('search_location', '')
    search_availability = request.GET.get('search_availability', '')
    search_region = request.GET.get('search_region', '') 
     
    if search_name:
        obj = obj.filter(name__icontains=search_name)
    if search_location:
        obj = obj.filter(location__icontains=search_location)
    if search_availability:
        obj = obj.filter(availability=search_availability)
    if search_region:  
        obj = obj.filter(region=search_region)
    
    return render(request, 'skilled_individual.html', {
        'form': form,
        'obj': obj,
        'search_name': search_name,
        'search_location': search_location,
        'search_availability': search_availability,
        'search_region': search_region,  
    })




def all_applicants(request):
    m_emails = Payment.objects.values_list('email', flat=True)
    user_posts = post_job.objects.filter(user=request.user)
    applicants = []
    for post in user_posts:
        post_applicants = post.apply_job_set.all()
        for applicant in post_applicants:
            applicants.append(applicant)
    is_superuser = request.user.is_superuser
    return render(request, 'all_applicants.html', {'applicants': applicants, 'm_emails': m_emails, 'is_superuser': is_superuser})



from django.shortcuts import render, get_object_or_404, redirect
from .models import skilled_individuals, IndividualRating,Comments, skilled_ind_Comment
from .forms import skilled_individual_form, CommentForm, CommentsForm, MultipleImageForms, skilled_ind_Comment_form
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import geocoder
import folium

from .models import skilled_individuals, IndividualRating


def skilled_individual_details(request, id):
    company = get_object_or_404(skilled_individuals, id=id)
    new_comments = None
    user_already_rated = False

    if request.method == 'POST':
        form = skilled_individual_form(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()

        if IndividualRating.objects.filter(user=request.user, company=company).exists():
            user_already_rated = True
        else:
            try:
                rating_value = int(request.POST.get('rating', 0))
                if 1 <= rating_value <= 5:
                    IndividualRating.objects.create(user=request.user, company=company, rating=rating_value)
                    user_already_rated = True
            except ValueError:
                pass

    form = skilled_individual_form(instance=company)
    comment_form = skilled_ind_Comment_form()
    image_form = MultipleImageForms()

    comment_form = skilled_ind_Comment_form(request.POST)
    if request.method == 'POST':
        comment_form = skilled_ind_Comment_form(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ind = company 
            comment.save()
            comments = company.comments.filter(active=True)
            comment_form = skilled_ind_Comment_form()
    else:
        comment_form = skilled_ind_Comment_form()
    comments = skilled_ind_Comment.objects.filter(ind=company, active=True)
    average_rating = IndividualRating.objects.filter(company=company).aggregate(Avg('rating'))['rating__avg']
    rating_star_range = range(int(average_rating)) if average_rating is not None else range(0)
    job_location = geocoder.osm(company.location)
    if job_location.lat is not None and job_location.lng is not None:
        job_map = folium.Map(location=[job_location.lat, job_location.lng], zoom_start=10)
        folium.Marker([job_location.lat, job_location.lng], popup=company.name).add_to(job_map)
        job_map = job_map._repr_html_()
    else:
        job_map = None
    ratings = IndividualRating.objects.filter(company=company)
    return render(request, 'skilled_individual_details.html', {
        'company': company,
        'form': form,
        'comments': comments,
        'comment_form': comment_form,
        'image_form': image_form,
        'new_comments': new_comments,
        'user_already_rated': user_already_rated,
        'rating_star_range': rating_star_range,
        'job_map': job_map,
          'ratings': ratings,
    })






from django.db.models import Sum

def rating_statistics(request):
    companies = skilled_individuals.objects.annotate(total_rating_points=Sum('ratings__rating')).order_by('-total_rating_points')
    return render(request, 'rating_statistics.html', {'companies': companies})


def find_a_talent(request):
    return render(request, 'find_a_talent.html')



def skilled_company(request):
    obj = skilled_companies.objects.all()
    form = skilled_company_form()
    if request.method == 'POST':
        form = skilled_company_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('skilled_company')
    else:
        form = skilled_company_form()
    search_name = request.GET.get('search_name', '')
    search_location = request.GET.get('search_location', '')
    search_availability = request.GET.get('search_availability', '')
    if search_name:
        obj = obj.filter(name__icontains=search_name)
    if search_location:
        obj = obj.filter(location__icontains=search_location)
    if search_availability:
        obj = obj.filter(availability=search_availability)
    return render(request, 'skilled_company.html', {'form': form, 'obj':obj, 'search_name': search_name, 'search_location': search_location, 'search_availability': search_availability})




from .models import skilled_companies, MultipleImages, Comment,CompanyRating
from . forms import MultipleImagesForm, CompanyRatingForm
from django.http import HttpResponse  # Add this import

from django.db import IntegrityError

def skilled_company_details(request, id):
    company = get_object_or_404(skilled_companies, id=id)
    new_comments = None
    user_already_rated = False

    if request.method == 'POST':
        form = skilled_company_form(request.POST, request.FILES, instance=company)
        images_form = MultipleImagesForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        if images_form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                MultipleImages.objects.create(images=image, post=company)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.company = company
            new_comment.save()

        if CompanyRating.objects.filter(user=request.user, company=company).exists():
            user_already_rated = True
        else:
            try:
                rating_value = int(request.POST.get('rating', 0))
                if 1 <= rating_value <= 5:
                    CompanyRating.objects.create(user=request.user, company=company, rating=rating_value)
                    user_already_rated = True
            except ValueError:
                pass

        return redirect('skilled_company_details', id=id)

    else:
        form = skilled_company_form(instance=company)
        images_form = MultipleImagesForm()
        comment_form = CommentForm()

    comments = company.comments.filter(active=True)
    if new_comments is None:
        new_comments = Comment.objects.none()

    images = company.images.all()
    ratings = CompanyRating.objects.filter(company=company)
    job_location = geocoder.osm(company.location)
    if job_location.lat is not None and job_location.lng is not None:
        job_map = folium.Map(location=[job_location.lat, job_location.lng], zoom_start=10)
        folium.Marker([job_location.lat, job_location.lng], popup=company.name).add_to(job_map)
        job_map = job_map._repr_html_()
    else:
        job_map = None
    context = {
        'form': form,
        'ratings': ratings,
        'images_form': images_form,
        'company': company,
        'comments': comments,
        'comment_form': comment_form,
        'new_comments': new_comments,
        'images': images,
        'user_already_rated': user_already_rated,
        'job_map': job_map,
    }

    return render(request, 'skilled_company_details.html', context)





def Delete(request, id):
    obj = skilled_companies.objects.get(id=id)
    obj.delete()
    return redirect('skilled_company')


from django.http.request import HttpRequest
from django.http.response import HttpResponse


def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment: Payment = payment_form.save(commit=False)
            if request.user.is_authenticated:
                payment.email = request.user.email
            payment.amount = 50
            payment.save()
            return render(request, 'make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email
        initial['amount'] = 50
        payment_form = PaymentForm(initial=initial)
    return render(request, "initiate_payment.html", {"payment_form": payment_form,})




def verify_payment(request, ref: str):
    trxref = request.GET["trxref"]
    if trxref != ref:
        messages.error(
            request,
            "The transaction reference passed was different from the actual reference. Please do not modify data during transactions",
        )
    payment: Payment = get_object_or_404(Payment, ref=ref)
    if payment.verify_payment():
        messages.success(
            request, f"Payment Completed Successfully, GH₵ {payment.amount}."
        )
        messages.success(
            request, f"Your new credit balance is GH₵ {payment.user.credit}."
        )
        return redirect('index')

    else:
        messages.warning(request, "Sorry, your payment could not be confirmed.")
    return redirect("initiate-payment")






