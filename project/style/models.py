import os
from django.db import models

class Url(models.Model):
    name = models.CharField(max_length=1024)
        
    def __str__(self):
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=1024)
    logo = models.ImageField(upload_to="images/site/", default='/images/site/not-exist.jpg')
    urls = models.ManyToManyField(Url, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["pk"]

class Style(models.Model):
    name = models.CharField(max_length=1024)
    logo = models.ImageField(upload_to="images/style/", default='/images/style/not-exist.jpg')
    creator = models.ForeignKey('person.Person', on_delete=models.CASCADE, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(default="some description", blank=True)
    source = models.TextField(null=True, blank=True)
    upload_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    subscribed = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name

    @staticmethod
    def get_new_site(site_name, site_urls):
        if site_name != "" and site_urls != "":
            new_urls = site_urls.split(" ")
            new_site = Site.objects.create(name=site_name)
            for new_url in new_urls:
                tmp_url = Url.objects.create(name=new_url)
                tmp_url.save()
                new_site.urls.add(tmp_url)
            return new_site
        else:
            return None

    # def save(self, *args, **kwargs):
    #     try:
    #         this_record = Style.objects.get(id=self.id)
    #         if this_record.logo != self.logo:
    #             os.remove(this_record.logo.path)
    #     except:
    #         pass
    #     super(Style, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     os.remove(self.logo.path)
    #     super(Style, self).delete(*args, **kwargs)
