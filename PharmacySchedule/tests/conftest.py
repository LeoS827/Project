import datetime

import pytest
from django.test import Client
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from schedule.models import Person, Schedule, Shift
from django.conf import settings


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def person():
    person = Person.objects.create(name='Test', title='Mgr')
    return person


@pytest.fixture
def user():
    user = User.objects.create_user(username='test2', password='t2', email='t2@t.pl')
    return user


@pytest.fixture
def user_with_permissions():
    user = User.objects.create_user(username='test3', password='t3', email='t3@t.pl')
    p = Permission.objects.get(codename='view_schedule')
    user.user_permissions.add(p)
    return user


@pytest.fixture
def superuser():
    user = User.objects.create_superuser(username='test', password='t', email='t@t.pl')
    return user


@pytest.fixture
def schedule_test():
    test_schedule = Schedule.objects.create(name='test schedule', start_day=datetime.datetime(2023, 8, 1).date(),
                                            end_date=datetime.datetime(2023, 8, 1).date())
    return test_schedule


@pytest.fixture
def group_test():
    group = Group.objects.create(name='group test')
    return group


@pytest.fixture
def shift_test():
    test_schedule = Schedule.objects.create(name='test schedule2', start_day=datetime.datetime(2023, 8, 1).date(),
                                            end_date=datetime.datetime(2023, 8, 1).date())
    shift_test = Shift.objects.create(schedule=test_schedule, name='st', capacity=1, shift_type='Main')
    return shift_test