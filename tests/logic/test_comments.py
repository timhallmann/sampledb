# coding: utf-8
"""

"""

import datetime
import pytest

import sampledb
from sampledb.models import User, UserType, Action, ActionType, Objects, Object
from sampledb.logic import comments

from ..test_utils import app_context


@pytest.fixture
def user():
    user = User(name='User', email="example@fz-juelich.de", type=UserType.PERSON)
    sampledb.db.session.add(user)
    sampledb.db.session.commit()
    # force attribute refresh
    assert user.id is not None
    return user


@pytest.fixture
def action():
    action = Action(
        action_type=ActionType.SAMPLE_CREATION,
        name='Example Action',
        schema={
            'title': 'Example Object',
            'type': 'object',
            'properties': {
                'name': {
                    'title': 'Sample Name',
                    'type': 'text'
                }
            },
            'required': ['name']
        },
        description='',
        instrument_id=None
    )
    sampledb.db.session.add(action)
    sampledb.db.session.commit()
    # force attribute refresh
    assert action.id is not None
    return action


@pytest.fixture
def object(user: User, action: Action):
    data = {'name': {'_type': 'text', 'text': 'Object'}}
    return Objects.create_object(user_id=user.id, action_id=action.id, data=data, schema=action.schema)


def test_comments(user: User, object: Object):
    start_datetime = datetime.datetime.utcnow()
    assert len(comments.get_comments_for_object(object_id=object.object_id)) == 0
    comments.create_comment(object_id=object.object_id, user_id=user.id, content="Test 1")
    assert len(comments.get_comments_for_object(object_id=object.object_id)) == 1
    comment = comments.get_comments_for_object(object_id=object.object_id)[0]
    assert comment.user_id == user.id
    assert comment.author == user
    assert comment.object_id == object.object_id
    assert comment.content == "Test 1"
    assert comment.utc_datetime >= start_datetime
    assert comment.utc_datetime <= datetime.datetime.utcnow()
    comment_datetime = start_datetime-datetime.timedelta(days=1)
    comments.create_comment(object_id=object.object_id, user_id=user.id, content="Test 2", utc_datetime=comment_datetime)
    assert len(comments.get_comments_for_object(object_id=object.object_id)) == 2
    comment1, comment2 = comments.get_comments_for_object(object_id=object.object_id)
    assert comment1.content == "Test 2"
    assert comment1.utc_datetime == comment_datetime
    assert comment2.content == "Test 1"
    assert comment2.utc_datetime >= start_datetime
    assert comment2.utc_datetime <= datetime.datetime.utcnow()
