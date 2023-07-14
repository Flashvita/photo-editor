"""
ManagerPlus:

    Don't raising error on MyModel.DoesNotExists exception and returns None
    >>> MyModel.objects.get_or_none(pk=100)


    Aviods DoesNotExists or MultipleObjectsReturned exceptions,
    returns first/last object or None
    >>> MyModel.objects.none_of_first(username="Tahiro")
    >>> MyModel.objects.none_of_last(username="Motoyuki")
    (The methods trying to use .get() before .first() or .last() call)


    Checks is at least one object exists, then returns True or False
    >>> MyModel.objects.has_any(model="Ford", age__gte=5)


ModelPlus:
    - Including ManagerPlus by default
    - Has method to_dict() which returns object as a dictionary


ModelStat:
    - Including created_at and updated_at by default
    - Including "created by" info fields


Example:

    >>> from enhanced_models import ModelPlus, ModelStat

    >>> class MyModel(ModelPlus, ModelStat):
    >>>     ...

    >>> if my_obj := MyModel.objects.last_or_none(tracking_number="23456"):
    >>>     return json_dumps(my_obj.to_dict())

"""

import os

from itertools import chain
from pathlib import Path
from typing import Any, Sequence, Optional

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from django.db import connection, models


def get_env_username():
    """
    Returns username connected to DB server in OS environment
    """
    try:
        return os.getlogin()
    except OSError:
        return "docker_root"


def get_db_username():
    """
    Returns username for connection session in DB server environment
    """
    return connection._connections.settings[connection._alias]["USER"]


class ManagerPlus(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def has_any(self, **kwargs) -> bool:
        """
        `True` if `self.filter(**kwargs)` is not empty, else `False`
        """
        return bool(self.filter(**kwargs).all)

    def none_or_first(self, **kwargs):
        """
        Analogue of queryset.first(), but works faster if get() is successful
        """
        try:
            return self.get(**kwargs)
        except MultipleObjectsReturned:
            return self.filter(**kwargs).first()
        except ObjectDoesNotExist:
            return None

    def none_or_last(self, **kwargs):
        """
        Analogue of queryset.last(), but works faster if get() is successful
        """
        try:
            return self.get(**kwargs)
        except MultipleObjectsReturned:
            return self.filter(**kwargs).last()
        except ObjectDoesNotExist:
            return None

    def random(self):
        """
        Random table row.
        """
        return self.order_by("?").first()


class ModelPlus(models.Model):
    """
    Adds extendend objects Manager and some methods.
    Hasn't apply any extra model fields.
    """

    objects = ManagerPlus()

    @property
    def _allfields(self):
        """Iterable with all fields in the model"""
        return chain(
                getattr(self._meta, "concrete_fields", []),
                self._meta.private_fields,
            )

    def to_dict(self, fields: Optional[Sequence] = None) -> dict[str, Any]:
        """
        Returns model object as a dictionary. If `fields` is specified,
        returns a precised fields only.

        Unexistent fields are ignored with no exception raise.
        """
        return {
            field.name: field.value_from_object(self)
            for field in self._allfields if fields is None or field in fields
        }

    def update_fields(self, skip_extra: bool = True, **kwargs):
        """
        Updates and saves instance according to `kwargs`.

        If `skip_extra` is `True`, fields not in model are skpipped,
        otherwise AttributeError will raise.
        """
        fieldnames = {i.name for i in self._allfields}
        kwnames = set(kwargs.keys())
        if not kwnames.issubset(fieldnames) and not skip_extra:
            raise AttributeError(
                f'Wrong field(s) {", ".join(kwnames.difference(fieldnames))}'
            )
        fields2update = ()
        for k, v in kwargs.items():
            if k in fieldnames:
                setattr(self, k, v)
                fields2update += (k,)
        self.save(update_fields=fields2update)
        return self

    class Meta:
        abstract = True


class ModelStat(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Time created",
        auto_now_add=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Time updated",
        auto_now=True,
        null=True,
    )
    created_env_uname = models.CharField(
        verbose_name="OS User",
        max_length=32,
        default=get_env_username,
    )
    created_db_uname = models.CharField(
        verbose_name="DB User",
        max_length=32,
        default=get_db_username,
    )

    class Meta:
        abstract = True


class EnchancedModel(ModelStat, ModelPlus):
    class Meta:
        abstract = True



def upload_by_models(instanse, filename):
    """
    Generic function for `upload_to` parameter. Creates path for `MEDIA_ROOT`
    folder as `'ClassName/instanse_slug/filename'`

    The `instans_slug` is the slugified string representation from `__str__()`
    or 'Unknown' if `__str__()` is inaccessible. If path already exists,
    the `instanse_slug` will be updated with unique digits postfix.

    """
    import time

    import slugify

    instanse_title = slugify.slugify(str(instanse)) or "Unknown"
    path_builder = (
        lambda instanse, filename, unifier: Path(instanse.__class__.__name__)
        / f"{instanse_title}{unifier}"
        / filename
    )
    path_to_save = path_builder(instanse, filename, "")
    while path_to_save.exists():
        path_to_save = path_builder(instanse, filename, f"_{time.monotonic_ns()}")
    return path_to_save
