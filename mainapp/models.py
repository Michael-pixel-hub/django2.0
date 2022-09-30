from django.db import models


class News(models.Model):
    title = models.CharField(max_length=256, verbose_name='title')
    preambule = models.TextField(verbose_name='preambule')
    body = models.TextField(verbose_name='body')
    body_as_markdown = models.BooleanField(default=False, verbose_name='body_as_markdown')
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    updated = models.DateTimeField(auto_now=True, verbose_name='update')
    deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.title


class Courses(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    description = models.TextField(verbose_name='description')
    description_as_markdown = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='cost')
    cover = models.ImageField(upload_to='images/', verbose_name='image')
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    updated = models.DateTimeField(auto_now=True, verbose_name='update')
    deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='course')
    num = models.DecimalField(max_digits=30, decimal_places=0, verbose_name='num')
    title = models.CharField(max_length=256, verbose_name='title')
    description = models.TextField(verbose_name='description')
    description_as_markdown = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    updated = models.DateTimeField(auto_now=True, verbose_name='update')
    deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.title


class CourseTeachers(models.Model):
    name_first = models.CharField(max_length=256, verbose_name='name_first')
    name_second = models.CharField(max_length=256, verbose_name='name_second')
    day_birth = models.DateField(blank=False, null=False, verbose_name='birth')
    course = models.ManyToManyField(Courses, verbose_name='course')

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.name_first
