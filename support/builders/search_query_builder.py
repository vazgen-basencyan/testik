from enum import Enum


class SearchQueryBuilder:
    def __init__(self, object_name=None, full_path=None):
        self.full_path = f'/{object_name}/' if object_name else full_path
        self.additional_columns = []
        self.disable_aggregation_flag = True
        self.conditions = []
        self.select_columns = [
            "name",
            "size",
            "service"
        ]
        self.default_columns = [
            "objectId",
            "instanceId",
            "classId",
            "name",
            "size",
            "createTime",
            "modifyTime",
            "accessTime",
            "storeTime",
            "osOwner",
            "service",
            "serviceType",
            "serviceMode",
            "storageCost",
            "retrievalCost",
            "retrievalTime",
            "metadataObject",
            "searchHits",
            "classificationObjects",
            "isDeleted",
            "userTags"
        ]

    def select(self, *columns):
        self.default_columns.extend(columns)
        return self

    def add_default_columns(self, value=True):
        self.additional_columns.append(f'SET @@DEFAULT_COLUMNS={",".join(self.default_columns)};')
        self.additional_columns.append(f'SET @@ADD_DEFAULT_COLUMNS={str(value).upper()};')
        return self

    def disable_aggregation(self, value=True):
        self.additional_columns.append(f'\nSET @@DISABLE_AGGREGATION={str(value).upper()};')
        return self

    def where(self, condition):
        if isinstance(condition, Condition):
            self.conditions.append(condition)
        else:
            raise ValueError("Condition must be a Condition object")
        return self

    def build(self, query=''):
        self.add_default_columns()
        self.disable_aggregation()
        if self.additional_columns:
            query += "".join(self.additional_columns)
        if self.select_columns:
            query += f"\nSELECT {','.join(self.select_columns)}"
        query += f" FROM STORE('{self.full_path}')"
        if self.conditions:
            where_conditions = " AND ".join(str(cond) for cond in self.conditions)
            query += f" WHERE {where_conditions};"
        else:
            query += ";"
        return query


class Op(Enum):
    EQUAL = '='


class Condition:
    def __init__(self, field, value, op=Op.EQUAL):
        self.field = field
        self.value = value
        self.op = op

    def __str__(self):
        return f"{self.field} {self.op.value} '{self.value}'"
