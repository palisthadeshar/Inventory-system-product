from django.db import models
from utils.models import CommonInfo, Address
from utils.validations import validate_mobile_number


# Create your models here.
class Warehouse(CommonInfo, Address):
    name = models.CharField(max_length=100)
    phone = models.CharField(
         unique=True, validators=[validate_mobile_number]
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name 


#rough codeee..............



class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.headline
    

# Entry.objects.update(pub_date=F("pub_date")+timedelta(days=365*30))
#Entry.objects.annotate(pub_date=F("date")-date(2025,1,1))  
#auth = Author.objects.annotate(author_code=Concat(F("name"),v(" "),F("name"))) 
#Entry.objects.aggregate(first_published_year=Max("pub_date__year")) 
#Entry.objects.dates('pub_date','day',order='DESC') 
# entry = Entry.objects.select_related('blog').get(id=1)
# entry.blog.name
#entry = Entry.objects.prefetch_related('authors').all()
# entry = Entry.objects.prefetch_related('authors').all()
# >>> for x in entry:              
# ...     for author in x.authors.all():
# ...             print(author.name) #get the name of all author

# with transcation.atomic():
# ...     blog_name=Blog.objects.create(name="hiii")
# ...     author1=Author.objects.create(name="author1",email="author1@gmail.com")
# ...     author2=Author.objects.create(name="author2",email="author2@gmail.com")
# ...     new_entry=Entry.objects.create(blog=blog_name,headline="some text",body_text="text",pub_date="2023-10-12")
# ...     new_entry.authors.add(author1,author2)

# Blog.objects.raw("SELECT * FROM Author") 
#Entry.objects.latest('pub_date') 
#Entry.objects.latest('-pub_date') 