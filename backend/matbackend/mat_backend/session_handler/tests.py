from datetime import datetime
from django.db import models
from django.test import TestCase
from session_handler.models import Session, Participant
from datetime import datetime
from ml_handler.models import MLModel
from account.models import User

class SetUpHelper():
    '''
    Helper class for creating and saving objects necessary for model test.
    '''
    def setUpUser():
        return User.objects.create( email = "usertest@gmail.com",
        username = "usertest", first_name= "usertest", last_name="usertest",
        password = "somePASS")

    def setUpModel(user):
        return MLModel.objects.create(name = "test model",
        creation_date = "2021-12-11",
        model_parameters_json = "one param",
        owner = user)

    def setUpParticipant():
        user= SetUpHelper.setUpUser()
        model= SetUpHelper.setUpModel(user)
        return Participant.objects.create(user = user, model = model)

class AssertHelper():
    '''
    Helper class for creating and saving objects necessary for model test.
    '''
    def dummyUser():
        return User( email = "usertest@gmail.com",
        username = "usertest", first_name= "usertest", last_name="usertest",
        password = "somePASS")

    def dummyModel(user):
        return MLModel(name = "test model",
        creation_date = "2021-12-11",
        model_parameters_json = "one param",
        owner = user)

    def dummyParticipant():
        user= AssertHelper.dummyUser()
        model= AssertHelper.dummyModel(user)
        return Participant(user = user, model = model)

    def dummySession():
        return Session(name="Test Session",
        min_num_of_participants=2, max_num_of_participants=10,
        actual_num_of_participants=0, start_date=datetime(2021,12,22),
        founder = SetUpHelper.setUpParticipant()
        )

class ParticipantTestCase(TestCase):
    def setUp(self):
        # Given
        user= SetUpHelper.setUpUser()
        model= SetUpHelper.setUpModel(user)
        # When
        Participant.objects.create(user = user, model = model)

    def test_participant_model(self):
        user = User.objects.get(username = "usertest")
        participant = Participant.objects.get(user = user)
        # Then
        self.assertEqual(participant.user.username, "usertest")

class SessionTestCase(TestCase):
    def setUp(self):
        # Given
        _name="Test Session"
        _min_num_of_participants = 2
        _max_num_of_participants = 10
        _actual_num_of_participants = 0
        _start_date = datetime(2021,12,22)
        _founder = SetUpHelper.setUpParticipant()
        # When
        Session.objects.create(
            name=_name,
            min_num_of_participants =_min_num_of_participants,
            max_num_of_participants =_max_num_of_participants,
            actual_num_of_participants =_actual_num_of_participants,
            start_date = _start_date,
            founder = _founder
        )

    def test_session_model(self):
        user = User.objects.get(username = "usertest")
        participant = Participant.objects.get(user_id = user.id )
        session = Session.objects.get(founder_id = participant.participant_id)
        # Then
        self.assertEqual(session.founder.user.username, participant.user.username )
