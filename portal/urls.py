from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='index'), 
    path('about', views.about, name='about'), 
    path('job_list', views.job_list, name='job_list'), 
    path('job_detail/<int:post_id>/', views.job_detail, name='job_detail'),
    path('testimonial', views.testimonial, name='testimonial'), 
    path('profile', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('post_a_job', views.post_a_job, name='post_a_job'), 
    path('login', views.login_view, name='logins'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('employer/', views.employer, name='employer'),
    path('employee/', views.employee, name='employee'),
    path('employer_job_post/', views.employer_job_post, name='employer_job_post'),
    path('employer_job_post/<int:post_id>/', views.employer_job_post, name='employer_job_post'),
    path('map', views.map, name='map'),
    path('all_jobs', views.all_jobs, name='all_jobs'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
    path('delete_job_post/<int:pk>/', views.delete_job_post, name='delete_job_post'),
    path('logout/', views.logout_user, name='logout'),
    path('search_results/', views.search_results, name='search_results'),
    path('category_view/<int:category_id>/', views.category_view, name='category_view'),
    path('category', views.category, name='category'), 
    path('find_a_talent', views.find_a_talent, name='talent'), 
    path('all_applicants', views.all_applicants, name='all_applicants'),
    path('privacy', views.privacy, name='privacy'),
    path('rating_statistics/', views.rating_statistics, name='rating_statistics'),
    path('terms', views.terms, name='terms'),
    path('add_category', views.add_category, name='add_category'),
    path('skilled_individual', views.skilled_individual, name='skilled_individual'),
    path('skilled_company', views.skilled_company, name='skilled_company'),
    path('skilled-company-details/<int:id>/', views.skilled_company_details, name='skilled_company_details'),
    path('skilled_individual_details/<int:id>/', views.skilled_individual_details, name='skilled_individual_details'),
    path('delete/<int:id>', views.Delete, name='delete'),
    path('initiate-payment/', views.initiate_payment, name="initiate-payment"),
    path('verify-payment/<str:ref>/', views.verify_payment, name="verify-payment"),
    path('update_job_post/<int:job_post_id>/', views.update_job_post, name='update_job_post'),



]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


