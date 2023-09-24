from django.contrib import admin
from .models import User,contact,skilled_ind_Comment, Message ,MultipleImages,CompanyRating, IndividualRating, apply_job,Comment,Comments, post_job,Payment, sectioned, Category, skilled_individuals, job_time, report_job, CompanyProfile, skilled_companies
from django.contrib.auth.models import Group


admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(contact)
admin.site.register(post_job)
admin.site.register(sectioned)
admin.site.register(apply_job)
admin.site.register(Category)
admin.site.register(job_time)
admin.site.register(report_job)
admin.site.register(CompanyProfile)
admin.site.register(skilled_companies)
admin.site.register(skilled_individuals)
admin.site.register(Payment)
admin.site.register(Comment)
admin.site.register(Comments)
admin.site.register(MultipleImages)
admin.site.register(Message)
admin.site.register(IndividualRating)
admin.site.register(CompanyRating)
admin.site.register(skilled_ind_Comment)




