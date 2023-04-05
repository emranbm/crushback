from main.data_migrations.data_migration import DataMigration, MigrationsRepository
from main.models import User, Crush


@MigrationsRepository.register
class Migration(DataMigration):
    name = "telegram_username_lowercase"

    def migrate(self):
        for crush in User.objects.all():
            if crush.telegram_username:
                crush.telegram_username = crush.telegram_username.lower()
                crush.save()
        for crush in Crush.objects.all():
            if crush.telegram_username:
                crush.telegram_username = crush.telegram_username.lower()
                crush.save()

    def rollback(self):
        pass
