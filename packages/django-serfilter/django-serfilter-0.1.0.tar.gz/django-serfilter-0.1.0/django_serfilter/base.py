from functools import partial

from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend


class SerializerBackend(BaseFilterBackend):
    def filter_queryset(self, request=None, queryset=None, view=None):
        serializer_class = getattr(view, 'serializer_filter_class', None)
        if not serializer_class:
            serializer_class = view.serializer_class

        if not issubclass(serializer_class, FilterMixin):
            namespaces = {}
            if getattr(serializer_class, 'Meta', None):
                namespaces['Meta'] = serializer_class.Meta
            serializer_class = type(
                'DefaultSerializerFilter', (FilterMixin, serializer_class),
                namespaces)

        serializer = serializer_class(data=request.GET)
        if isinstance(serializer._filter_fields, dict):
            try:
                f = serializer.filter_backend
            except AttributeError:
                # TODO: Check wording of the following:
                raise AttributeError(
                    'Serializer filter with `Meta.filter_fields` as a dict '
                    'must define fields for "backend", e.g. '
                    '`filter_fields = {\'backend\': (\'field1\',)}')
            return f(queryset)
        else:
            return serializer.filter(queryset)


class FilterMixin(object):
    class Meta:
        filter_fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self._filter_fields
        if isinstance(fields, dict):
            for name, fields in fields.items():
                f = partial(self.filter, name=name, fields=fields)
                setattr(self, 'filter_{}'.format(name), f)
        elif isinstance(fields, (list, tuple)):
            f = partial(self.filter, name=None, fields=fields)
            setattr(self, 'filter', f)

    def filter(self, qs, name=None, fields=None, raise_exception=True):
        if isinstance(self._filter_fields, dict) and not name:
            raise NotImplementedError(
                'Cannot call `filter` directly if `Meta.filter_fields` is '
                'a dict')

        if not self.is_valid(raise_exception=raise_exception):
            return qs

        g = self.validated_data.items()
        if fields is not None:
            g = ((k, v) for k, v in self.validated_data.items() if k in fields)

        name_list = ['filter_']
        if name:
            name_list.insert(0, 'filter_{}_by_'.format(name))

        for k, v in g:
            for name in name_list:
                func = getattr(self, name + k, None)
                if func:
                    qs = func(qs, v)
                    break
            else:
                funcs = ', '.join([(n + k) for n in name_list])
                raise AttributeError(
                    'Implement one of the following: ' + funcs)
        return qs

    @property
    def _filter_fields(self):
        meta = getattr(self, 'Meta', None)
        if meta:
            return getattr(meta, 'filter_fields', None)
