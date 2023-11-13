from unittest import TestCase
from datetime import datetime, timedelta, date, time

from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MAElementDescription_class import MAElementDescription
from descriptions.MADateDescription_class import MADateDescription
from descriptions.MATimeDescription_class import MATimeDescription
from descriptions.MAIntDescription_class import MAIntDescription
from descriptions.MABooleanDescription_class import MABooleanDescription
from descriptions.MAFloatDescription_class import MAFloatDescription
from descriptions.MADurationDescription_class import MADurationDescription
from descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from descriptions.MAReferenceDescription_class import MAReferenceDescription


class TestPerson():
    def __init__(
            self, 
            first_name, 
            age, 
            dob, 
            height, 
            alive, 
            active, 
            last_acitve,
            period_active,
            current_time
    ):
        self.first_name = first_name
        self.dob = dob
        self.age = age
        self.height = height
        self.alive = alive
        self.active = active

        self.last_active = last_acitve
        self.period_active = period_active
        self.current_time = current_time


class MAStringWriterVisiorTest(TestCase):
    def setUp(self):
        self.model = TestPerson(
            first_name="Bob", 
            dob=date(1990, 1, 1), 
            age=33.8, 
            height=180, 
            alive=True,
            active=False,
            last_acitve=datetime(2023, 1, 1, 10, 10, 10),
            period_active=datetime(2023,2,1,14,0)-datetime(2023,3,8,16,1),
            current_time=time(18, 4, 12)
        )

    def test_str(self):
        first_name_desc = MAStringDescription(
            accessor='first_name', 
            label='First name', 
            required=False
        )

        self.assertEqual(first_name_desc.readString(self.model), "Bob")

    def test_date(self):
        date_of_birth = MADateDescription(
            accessor='dob', 
            label='Birth date', 
            required=False
        )

        self.assertEqual(date_of_birth.readString(self.model), 
                         str(date(1990, 1, 1))
        )

    def test_datetime(self):
        last_active = MADateAndTimeDescription(
            accessor='last_active', 
            label='Last time active', 
            required=False
        )

        self.assertEqual(last_active.readString(self.model), 
                         str(datetime(2023, 1, 1, 10, 10, 10))
        )

    def test_time(self):
        current_time = MATimeDescription(
            accessor='current_time', 
            label='Current time', 
            required=False
        )

        self.assertEqual(current_time.readString(self.model), 
                         str(time(18, 4, 12))
        )

    def test_int(self):
        height = MAIntDescription(
            accessor='height', 
            label='height', 
            required=False
        )

        self.assertEqual(height.readString(self.model), "180")

    def test_float(self):
        age = MAFloatDescription(accessor='age', label='age', required=False)
        self.assertEqual(age.readString(self.model), "33.8")

    def test_bool(self):
        alive = MABooleanDescription(
            accessor='alive', 
            label='alive', 
            required=False
        )
        active = MABooleanDescription(
            accessor='active', 
            label='active', 
            required=False
        )

        self.assertEqual(alive.readString(self.model), "True")
        self.assertEqual(active.readString(self.model), "False")
    
    def test_period(self):
        period_active = MADurationDescription(
            accessor='period_active', 
            label='period_active', 
            required=False
        )

        self.assertEqual(
            period_active.readString(self.model), 
            str(datetime(2023,2,1,14,0)-datetime(2023,3,8,16,1))
        )
    
    def test_relation(self):
        ref = MAReferenceDescription(
            accessor = "obj", 
            reference = self.model, 
            required = False
        )

        with self.assertRaises(TypeError):
            MAReferenceDescription.readString(ref)
    
    def test_undefined(self):
        height_desc = MAIntDescription(
            accessor = "height", 
            required = False, 
            undefined='-'
        )

        self.model.height = None
        self.assertEqual(
            height_desc.readString(self.model), '-'
        )
    
    def test_undefined_value(self):
        height_desc = MAIntDescription(
            accessor = "height", 
            required = False, 
            undefinedValue=-1, 
            undefined='-'
        )

        self.model.height = -1
        self.assertEqual(
            height_desc.readString(self.model), '-'
        )

        with self.assertRaises(TypeError):
            self.model.height = None
            height_desc.readString(self.model), None

        height_desc = MAIntDescription(
            accessor = "height", 
            required = False, 
            undefinedValue=-1, 
            undefined='NaN'
        )

        self.model.height = -1
        self.assertEqual(
            height_desc.readString(self.model), 'NaN'
        )

    def test_wrong_value(self):
        height_desc = MAIntDescription(
            accessor = "height", 
            required = False, 
            undefined='-'
        )
        
        with self.assertRaises(TypeError):
            MAIntDescription.readString(height_desc)


class MAStringReaderVisiorTest(TestCase):
    def setUp(self):
        self.model = TestPerson(
            first_name="Bob", 
            dob=str(date(1990, 11, 14)), 
            age="33.8", 
            height="180", 
            alive="True",
            active="False",
            last_acitve=str(datetime(2023, 10, 30, 10, 10, 10)),
            period_active="30 days, 0:00:00",
            current_time="18:04:12"
        )

    def test_str(self):
        first_name_desc = MAStringDescription(
            accessor='first_name', 
            label='First name', 
            required=False
        )

        self.assertEqual(first_name_desc.writeString(self.model), "Bob")

    def test_date(self):
        date_of_birth = MADateDescription(
            accessor='dob', 
            label='Birth date', 
            required=False
        )

        self.assertEqual(date_of_birth.writeString(self.model), 
                         date(1990, 11, 14)
        )
    
    def test_datetime(self):
        last_active = MADateAndTimeDescription(
            accessor='last_active',
            label='Last time active',
            required=False
        )

        self.assertEqual(last_active.writeString(self.model), 
                         datetime(2023, 10, 30, 10, 10, 10)
        )
    
    def test_time(self):
        current_time = MATimeDescription(
            accessor='current_time',
            label='Current time',
            required=False
        )

        self.assertEqual(current_time.writeString(self.model), 
                         time(18, 4, 12)
        )
    
    def test_int(self):
        height = MAIntDescription(
            accessor='height', 
            label='height', 
            required=False
        )

        self.assertEqual(height.writeString(self.model), 180)
    
    def test_float(self):
        age = MAFloatDescription(accessor='age', label='age', required=False)
        self.assertEqual(age.writeString(self.model), 33.8)
    
    def test_bool(self):
        alive = MABooleanDescription(
            accessor='alive', 
            label='alive', 
            required=False
        )
        active = MABooleanDescription(
            accessor='active', 
            label='active', 
            required=False
        )

        self.assertEqual(alive.writeString(self.model), True)
        self.assertEqual(active.writeString(self.model), False)
    
    def test_period(self):
        period_active = MADurationDescription(
            accessor='period_active', 
            label='period_active', 
            required=False
        )

        self.assertEqual(
            period_active.writeString(self.model), 
            timedelta(days=30)
        )

        self.model.period_active="36 days, 8:30:00"

        self.assertEqual(
            period_active.writeString(self.model), 
            datetime(2023,3,9,8,30)-datetime(2023,2,1,0,0)
        )
    
    def test_relation(self):
        ref = MAReferenceDescription(
            accessor = "obj", 
            reference = self.model, 
            required = False
        )

        with self.assertRaises(TypeError):
            MAReferenceDescription._validateKind(ref)
    
    def test_undefined(self):
        height_desc = MAIntDescription(
            accessor = "height", 
            required = False, 
            undefined='-'
        )

        self.model.height = '-'
        self.assertEqual(
            height_desc.writeString(self.model), None
        )
    
    def test_undefined_value(self):
        height_desc = MAElementDescription(
            accessor = "height", 
            required = False, 
            undefinedValue=-1, 
            undefined='-'
        )

        self.model.height = '-'
        self.assertEqual(
            height_desc.writeString(self.model), -1
        )

        self.model.height = 'None'
        self.assertEqual(
            height_desc.writeString(self.model), 'None'
        )

        height_desc = MAElementDescription(
            accessor = "height", 
            required = False, 
            undefinedValue=None, 
            undefined='-'
        )

        self.model.height = '-'
        self.assertEqual(
            height_desc.writeString(self.model), None
        )
