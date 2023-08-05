from dbt.adapters.base.relation import BaseRelation, Column
from dbt.utils import filter_null_values

class MSSQLColumn(Column):
    TYPE_LABELS = {
        'TEXT': 'VARCHAR(max)',
    }

    @classmethod
    def create_from_field(cls, field):
        return MSSQLColumn(
            field.name
            , cls.translate_type(field.field_type)
            , field.fields
            , field.mode
        )
