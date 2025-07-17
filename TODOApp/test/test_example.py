import pytest

def test_equal_or_not_equal():
    assert 3!=2
    assert 3==3
def test_is_instance():
    assert isinstance('this is a string',str)
    assert not isinstance('10',int)
def test_boolean():
    validated=True
    assert validated is True
    assert ('hello'=='world')is False
def test_type():
    assert type('hello') == str
    assert type('hello' is not int)
def test_greater_and_less_than():
    assert 7 < 8
    assert 4 < 10

def test_list():
    num_list = [1,2,3,4,5]
    any_list=[False,False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self,firstname:str,last_name:str,major:str,years:int):
        self.firstname = firstname
        self.lastname = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student('aman','gupta',"Computer Science",3)

def test_person_intialization(default_employee):
    assert default_employee.firstname == 'aman'
    assert default_employee.lastname == 'gupta'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 3

