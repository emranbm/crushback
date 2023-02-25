from typing import Union, Type

from django.db.models import Model
from django.db.models.query_utils import DeferredAttribute
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


def get_table_name(model: Type[Model]) -> str:
    return model._meta.db_table

def get_column_name(field: Union[DeferredAttribute, ForwardManyToOneDescriptor]) -> str:
    if isinstance(field, DeferredAttribute):
        return field.field.name
    elif isinstance(field, ForwardManyToOneDescriptor):
        return f"{field.field.name}_id"
    else:
        raise AssertionError(f"Unsupported field type: {type(field)}")
