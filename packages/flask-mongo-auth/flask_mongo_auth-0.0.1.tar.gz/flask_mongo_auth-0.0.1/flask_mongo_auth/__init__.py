from enum import Enum
from functools import wraps
from typing import Mapping, Any, Dict

from nezha.hash import hash_hmac
from pymongo import MongoClient


class Accounts(Enum):
    account_name = 'account_name'
    company_uuid = 'company_uuid'
    password = 'password'
    real_name = 'real_name'
    unique_field = 'account_name'


class BlockPermission(Enum):
    unique_field = 'unique_field'
    block_name = 'block_name'


def check_condition(condition_index: int):
    def decorate(func):
        @wraps(func)
        def wrap(self, *args, **kwargs):
            condition = args[condition_index]
            if not set(condition.keys()).issubset(set(map(lambda x: x.value, Accounts))):
                raise ValueError(f'condition {condition} keys not match to Accounts')
            return func(self, *args, **kwargs)

        return wrap

    return decorate


class Authentication:

    def __init__(self,
                 mongo_client: MongoClient,
                 mongo_db: str,
                 cache_obj: Any,
                 collection_account: str = 'accounts',
                 collection_permission: str = 'permission',
                 unique_field: str = 'account_name'):
        """

        :param mongo_client:
        :param mongo_db:
        :param cache_obj:
        :param collection_account:
        :param collection_permission:
        :param unique_field: unique filed in accounts used to join other collections
        """
        self.mongo_client = mongo_client
        self.mongo_db = mongo_db
        self.collection_account = collection_account
        self.collection_permission = collection_permission
        self.cache_obj = cache_obj
        self.unique_field = unique_field

    @check_condition(0)
    def can_login(self, condition: Mapping) -> bool:
        return self.mongo_client[self.mongo_db][self.collection_account].find_one(condition) is not None

    @staticmethod
    def generate_token(condition: Mapping, salt: str = '') -> str:
        return hash_hmac(salt, ''.join(str(v) for k, v in locals().items() if k != 'self'))

    @check_condition(1)
    def cache_token(self, token: str, condition: Mapping):
        self.cache_obj.set(token, condition)

    def check_cache(self, token: str)->bool:
        pass

    def get_cache(self, token: str) -> Dict:
        return self.cache_obj.get(token)

    def has_permission(self, token: str, block: str) -> bool:
        cache_condition = self.get_cache(token)
        condition = {
            BlockPermission.unique_field.value: cache_condition[self.unique_field],
            BlockPermission.block_name: block
        }
        return self.mongo_client[self.mongo_db][self.collection_account].find_one(condition) is not None


if __name__ == '__main__':
    print(set(map(lambda x: x.value, Accounts)))
