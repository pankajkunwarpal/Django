from django.db import models
from django.utils import timezone

from datetime import datetime
# Create your models here.

class PersonDetails(models.Model):
    
    gender = models.CharField(
        verbose_name="Gender", 
        choices=[('f', 'Female'), ('m', 'Male')], 
        max_length=1, default='f'
    )
    age  = models.PositiveIntegerField(verbose_name='Age', default=0)
    dob = models.DateField(verbose_name='Date of Birth', default=timezone.now)

    # def save(self, *args, **kwargs):
    #     age = (datetime.now().date() - self.dob).days//365

    #     self.age == age
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'Id: {self.id}, Age: {self.age}, dob: {self.dob}'


class Person(models.Model):
    person = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    detail = models.ForeignKey(PersonDetails, on_delete=models.CASCADE)

    def _age(self):
        return self.detail.age
        
    def _gender(self):
        return self.detail.gender

    def __str__(self):
        return self.person.get_full_name()


class Blog(models.Model):
    title = models.CharField(
        verbose_name='Blog Title',
        max_length=100,
    )
    blog = models.TextField(
        verbose_name='Write whatever your what to say',
    )

    
    def __str__(self, ):
        return  self.title.title()


class Blogs(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        verbose_name='Date Posted',
        auto_now=True
    )

    def __str__(self, ):
        return self.blog.title

    def _blog_title(self):
        return self.blog.title
    def _blog_content(self):
        return self.blog.blog
    def _person_name(self):
        return self.person.person.get_full_name()
    def _date_created(self,):
        return self.date_created.isoformat()
    def _id(self,):
        return self.person.person.id
    def _blog(self):
        return {'title': self._blog_title() , 'post': self._blog_content()}
    def _person(self):
        return {'person': self._person_name}

    
#     def _number_of_blogs(self,):
#         return _blogs_counter(self._id())


# def _blogs_counter(id):
#     return Blogs.objects.filter(person__id=id).count()