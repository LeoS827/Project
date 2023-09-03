import pytest
from schedule.models import Person


@pytest.mark.django_db
def test_person_model(person):
    assert len(Person.objects.all()) == 1
    assert Person.objects.get(name='Test') == person
