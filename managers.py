from django.db import models


class NoneManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def filter_or_none(self, **kwargs):
        try:
            return self.filter(**kwargs)
        except self.model.DoesNotExist:
            return None
