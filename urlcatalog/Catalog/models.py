from django.db import models
from datetime import datetime

# Create your models here.
class category(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

class url(models.Model):
    title = models.CharField(max_length=60)
    category = models.ForeignKey(category)
    url = models.URLField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images", blank=True)
    thumbnail = models.ImageField(upload_to="images/thumbs", blank=True)
    #date = models.DateTimeField(auto_now_add=True, blank=False)
    date = models.DateTimeField(default=datetime.now,blank=True)

    def __unicode__(self):
        return self.title

    def getImage(self):
        if not self.image:
            img = self.image._get_url()
        else:
            img = ''
        return img

    def getUrl(self):
        cleanedurl = self.url.replace('http://', '')
        cleanedurl = cleanedurl.replace('/', '')
        return cleanedurl

    def create_thumbnail(self):
        '''
	    original code for this method came from
        http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
        '''
        if not self.image:
            return

        from cStringIO import StringIO
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        # set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (250, 141)

        # open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))
        image_type = image.format.lower()

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, image_type, quality=100)
        temp_handle.seek(0)

        # save image to a SimpleUploadedFile which can be saved into ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
            temp_handle.read(), content_type='image/%s' % (image_type))
        # save SimpleUploadedFile into image field
        self.thumbnail.save('%s_thumbnail.%s' %
                                  (os.path.splitext(suf.name)[0], image_type), suf, save=False)

    def save(self):
        # create a thumbnail
        self.create_thumbnail()

        super(url, self).save()