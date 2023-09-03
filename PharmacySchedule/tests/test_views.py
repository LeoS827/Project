import datetime
import pytest

from django.contrib.auth.models import User, Group
from schedule.models import Schedule, Person, TITLE_CHOICES, Shift
from django.urls import reverse, resolve


@pytest.mark.django_db
def test_login_redirect(client):
    response = client.get('')
    assert response.status_code == 302
    assert response.url == '/schedule/login/?next=/'


@pytest.mark.django_db
def test_schedule_user_view(client, user):
    url = '/schedule/all/'
    response = client.get(url)
    assert response.url == f'/accounts/login/?next={url}'
    client.login(username='test2', password='t2', email='t2@t.pl')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_schedule_superuser_view(client, superuser):
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get('/schedule/all/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_schedule_correct(client, superuser):
    client.login(username='test', password='t', email='t@t.pl')
    data = {
        'name': 'testowy terminarz',
        'start_day': datetime.datetime(2023, 8, 1).date(),
        'end_date': datetime.datetime(2023, 8, 31).date()
    }
    client.post('/schedule/add/', data)
    assert Schedule.objects.get(name='testowy terminarz').start_day == datetime.datetime(2023, 8, 1).date()


@pytest.mark.django_db
def test_add_schedule_incorrect(client, superuser):
    client.login(username='test', password='t', email='t@t.pl')
    data = {
        'start_day': datetime.datetime(2023, 8, 1).date(),
        'end_date': datetime.datetime(2023, 8, 31).date()
    }
    client.post('/schedule/add/', data)
    assert len(Schedule.objects.all()) == 0


@pytest.mark.django_db
def test_schedule_detail_view(client, user, user_with_permissions,  superuser, schedule_test):
    schedule_id = schedule_test.id
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get(f'/schedule/detail/{schedule_id}/')
    assert response.status_code == 200
    client.logout()
    client.login(username='test2', password='t2', email='t2@t.pl')
    response = client.get(f'/schedule/detail/{schedule_id}/')
    assert response.status_code == 403
    client.logout()
    client.login(username='test3', password='t3', email='t3@t.pl')
    response = client.get(f'/schedule/detail/{schedule_id}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_schedule_edit_view(client, user, user_with_permissions,  superuser, schedule_test):
    schedule_id = schedule_test.id
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get(f'/schedule/edit/{schedule_id}/')
    assert response.status_code == 200
    client.logout()
    client.login(username='test2', password='t2', email='t2@t.pl')
    response = client.get(f'/schedule/edit/{schedule_id}/')
    assert response.status_code == 403
    client.logout()
    client.login(username='test3', password='t3', email='t3@t.pl')
    response = client.get(f'/schedule/edit/{schedule_id}/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_schedule_checkout_view(client, user, user_with_permissions,  superuser, schedule_test):
    schedule_id = schedule_test.id
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get(f'/schedule/checkout/{schedule_id}/')
    assert response.status_code == 200
    client.logout()
    client.login(username='test2', password='t2', email='t2@t.pl')
    response = client.get(f'/schedule/checkout/{schedule_id}/')
    assert response.status_code == 403
    client.logout()
    client.login(username='test3', password='t3', email='t3@t.pl')
    response = client.get(f'/schedule/checkout/{schedule_id}/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_person_correct(client, superuser):
    client.login(username='test', password='t', email='t@t.pl')
    data = {
        'username': 'nowy',
        'password': 'gHyT56T4%%6m',
        'name': 'nowyuzytkownik',
        'title': TITLE_CHOICES[0][0]
    }
    response = client.post('/schedule/person/add/', data)
    assert response.status_code == 302
    assert len(User.objects.filter(username='nowy')) == 1
    assert Person.objects.get(name='nowyuzytkownik').title == TITLE_CHOICES[0][0]


@pytest.mark.django_db
def test_add_person_incorrect(client, superuser):
    client.login(username='test', password='t', email='t@t.pl')
    data = {
        'username': 'nowy',
        'password': 'gHyT56T4%%6m',
        'name': 'nowyuzytkownik',
        'title': 'tytul'
    }
    response = client.post('/schedule/person/add/', data)
    assert response.status_code == 200
    assert len(User.objects.filter(username='nowy')) == 0
    assert len(Person.objects.all()) == 0


@pytest.mark.django_db
def test_person_all_view(client, user, user_with_permissions,  superuser):
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get(f'/schedule/person/all')
    assert response.status_code == 200
    client.logout()
    client.login(username='test2', password='t2', email='t2@t.pl')
    response = client.get(f'/schedule/person/all')
    assert response.status_code == 403
    client.logout()
    client.login(username='test3', password='t3', email='t3@t.pl')
    response = client.get(f'/schedule/person/all')
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_group_correct(client, superuser):
    client.login(username='test', password='t', email='t@t.pl')
    data = {
        'name': 'nowa_grupa',
    }
    response = client.post('/schedule/group/add/', data)
    assert response.status_code == 302
    assert len(Group.objects.filter(name='nowa_grupa')) == 1


@pytest.mark.django_db
def test_add_group_incorrect(client, superuser):
    client.login(username='test', password='t', email='t@t.pl')
    data = {
        'name': True,
    }
    response = client.post('/schedule/group/add/', data)
    assert response.status_code == 302
    assert len(Group.objects.filter(name='nowa_grupa')) == 0


@pytest.mark.django_db
def test_group_view_all(client, user, user_with_permissions, superuser):
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get(f'/schedule/group/all/')
    assert response.status_code == 200
    client.logout()
    client.login(username='test2', password='t2', email='t2@t.pl')
    response = client.get(f'/schedule/group/all/')
    assert response.status_code == 403
    client.logout()
    client.login(username='test3', password='t3', email='t3@t.pl')
    response = client.get(f'/schedule/group/all/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_shift_add_correct(client, superuser, schedule_test):
    client.login(username='test', password='t', email='t@t.pl')
    data = {
        'schedule': schedule_test.id,
        'name': 'nowa_zmiana',
        'capacity': 3,
        'shift_type': 'Main'
    }
    response = client.post('/schedule/shift/add/', data)
    assert response.status_code == 302
    assert len(Shift.objects.all()) == 1


@pytest.mark.django_db
def test_shift_add_incorrect(client, superuser, schedule_test):
    client.login(username='test', password='t', email='t@t.pl')
    data = {
        'schedule': 2,
        'name': 'nowa_zmiana',
        'capacity': 3,
        'shift_type': 'Main'
    }
    response = client.post('/schedule/shift/add/', data)
    assert response.status_code == 302
    assert len(Shift.objects.all()) == 0



@pytest.mark.django_db
def test_shift_delete_view(client, superuser, shift_test):
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get(f'/schedule/shift/delete/{shift_test.id}/')
    assert response.status_code == 302
    assert len(Shift.objects.all()) == 0


@pytest.mark.django_db
def test_schedule_delete_view(client, superuser, schedule_test):
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get(f'/schedule/delete/{schedule_test.id}/')
    assert response.status_code == 302
    assert len(Schedule.objects.all()) == 0


@pytest.mark.django_db
def test_user_delete_view(client, superuser, user):
    client.login(username='test', password='t', email='t@t.pl')
    response = client.get(f'/schedule/user/delete/{user.id}/')
    assert response.status_code == 302
    assert len(User.objects.all()) == 1
