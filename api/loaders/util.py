from collections import defaultdict

from django.apps import apps
from promise import Promise
from promise.dataloader import DataLoader as BaseDataLoader


def get_bulk_lookup(values, key_fn, many):
    default = list if many else lambda: None
    bulk_lookup = defaultdict(default)
    for value in values:
        key = getattr(value, key_fn)
        if many:
            bulk_lookup[key].append(value)
        else:
            bulk_lookup[key] = value
    return dict(bulk_lookup)


def batch_values(bulk_lookup, batched_keys, many):
    default = [] if many else None
    batched_values = [bulk_lookup.get(key, default) for key in batched_keys]
    return batched_values


def batch_load_model_by_field(app_name, model_name, field_name):
    model_to_load = apps.get_model(app_name, model_name)
    field = model_to_load._meta.get_field(field_name)  # pylint: disable=protected-access
    many = field.many_to_one

    def get_values(batched_keys):
        condition = {f'{field.column}__in':batched_keys}
        return model_to_load.objects.filter(**condition)

    def get_batched_values(batched_keys):
        values = get_values(batched_keys)
        bulk_lookup = get_bulk_lookup(values, field.column, many)
        batched_values = batch_values(bulk_lookup, batched_keys, many)
        return batched_values
    return get_batched_values


def batch_load_primary_key(app_name, model_name):
    model_to_load = apps.get_model(app_name, model_name)
    def load(primary_keys):
        return model_to_load.objects.filter(id__in=primary_keys)

    def batch_load_fn(model_ids):
        model_records = load(model_ids)
        model_map = {}
        for model_record in model_records:
            model_map[model_record.id] = model_record
        return [model_map.get(model_id) for model_id in model_ids]
    return batch_load_fn


def batch_load_foreign_key(app_name, model_name, foreign_key_name):
    model_to_load = apps.get_model(app_name, model_name)
    # key_field = model_to_load._meta.get_field(foreign_key_name)
    def load(foreign_keys):
        condition = {f'{foreign_key_name}_id__in':foreign_keys}
        return model_to_load.objects.filter(**condition)

    def batch_load_fn(model_ids):
        model_records = load(model_ids)
        model_map = defaultdict(list)
        for model in model_records:
            foreign_key_id = getattr(model, f'{foreign_key_name}_id')
            model_map[foreign_key_id].append(model)
        return [model_map[model_id] for model_id in model_ids]
    return batch_load_fn


class DataLoader(BaseDataLoader):
    def __init__(self, *args, **kwargs):
        load_fn = kwargs.pop('batch_load_fn', None)
        if not load_fn:
            load_fn = args[0]
            args = (None,) + args[1:]
        self.load_fn = load_fn

        super().__init__(*args, **kwargs)

    def batch_load_fn(self, keys): # pylint: disable=method-hidden
        return Promise.resolve(self.load_fn(keys))
