from abc import ABC, abstractmethod
from typing import Type, Dict


class DataMigration(ABC):
    name: str

    @abstractmethod
    def migrate(self):
        pass

    @abstractmethod
    def rollback(self):
        pass


class MigrationsRepository:
    _migrations: Dict[str, Type[DataMigration]] = {}

    @staticmethod
    def register(migration_cls: Type[DataMigration]) -> None:
        MigrationsRepository._migrations[migration_cls.name] = migration_cls

    @staticmethod
    def get(migration_name: str) -> DataMigration:
        print(MigrationsRepository._migrations)
        migration_cls = MigrationsRepository._migrations.get(migration_name)
        if migration_cls is None:
            raise Exception(f"Migration {migration_name} not found!")
        return migration_cls()
