import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from datacenter.models import Passcard, Visit


if __name__ == "__main__":
    passcards = Passcard.objects.all()
    print(f'Количество пропусков: {passcards.count()}')
    active_passcards = Passcard.objects.filter(is_active=True)
    print(f'Количество активных пропусков: {active_passcards.count()}')
    passcard = passcards[0]
    print(f'owner_name: {passcard.owner_name}')
    print(f'passcode: {passcard.passcode}')
    print(f'created_at: {passcard.created_at}')
    print(f'is_active: {passcard.is_active}')
    