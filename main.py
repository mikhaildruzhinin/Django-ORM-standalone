import os
import sys
import django

from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from datacenter.models import Passcard, Visit

def get_duration(visit):
    now = timezone.now()
    if not visit.leaved_at:
        duration = now - visit.entered_at
    else:
        duration = visit.leaved_at - visit.entered_at
    return duration

def is_visit_long(duration):
    if duration > 60 and duration != 1438:
        return True

def format_duration(visit):
    duration = visit.get_duration()
    seconds = int(duration.total_seconds())
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int((seconds % 3600) % 60)
    if hours == 0:
        hours = '00'
    elif hours < 10:
        hours = f'0{hours}'
    if minutes == 0:
        minutes = '00'
    elif minutes < 10:
        minutes = f'0{minutes}'
    if seconds == 0:
        seconds = '00'
    elif seconds < 10:
        seconds = f'0{seconds}'
    formatted_duration = f'{hours}:{minutes}:{seconds}'
    return formatted_duration

def main():
    now = timezone.now()
    active_passcards = Passcard.objects.filter(is_active=True)
    print(f'Количество активных пропусков: {active_passcards.count()}')

    owner_id = 0
    passcard = active_passcards[owner_id]
    print(f'owner_name: {passcard.owner_name}')
    print(f'passcode: {passcard.passcode}')
    print(f'created_at: {passcard.created_at}')
    print(f'is_active: {passcard.is_active}')

    visits = Visit.objects.filter(passcard=passcard)
    for visit in visits:
        duration = get_duration(visit)
        duration = int(duration.total_seconds() // 60)
        if is_visit_long(duration):
            print(visit, duration)

    active_visits = Visit.objects.filter(leaved_at=None)
    for active_visit in active_visits:
        print(active_visit.passcard.owner_name)
        print(f'Зашёл в хранилище, время по Москве: {active_visit.entered_at}')
        delta = now - active_visit.entered_at
        print(f'Находится в хранилище: {delta}')

if __name__ == '__main__':    
    main()
