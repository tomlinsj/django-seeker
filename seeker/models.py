from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class SavedSearch (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seeker_searches', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, db_index=True)
    querystring = models.TextField(blank=True)
    default = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'saved searches'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '%s?%s%s%s%d' % (self.url, self.querystring, ('&' if self.querystring else ''), 'saved_search=', self.pk)

@python_2_unicode_compatible
class SearchResultsRecord (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='search_results_records', null=True, on_delete=models.CASCADE)
    querystring = models.TextField(blank=True)
    displayed_columns = models.TextField(blank=True)
    url = models.CharField(max_length=200, db_index=True)
    result_count = models.BigIntegerField()
    date_searched = models.DateTimeField(default=timezone.now, editable=False)
    
    class Meta:
        ordering = ('-date_searched', 'user')

    def __str__(self):
        return '%s - %s' % (date_searched, user)