# coding: utf-8
"""
RESTful API for SampleDB
"""

import flask

from .authentication import multi_auth
from ..utils import Resource
from ...logic.actions import get_action
from ...logic.action_permissions import get_user_action_permissions, get_actions_with_permissions, Permissions
from ...logic import errors, utils
from ...models.actions import ActionType, Action

__author__ = 'Florian Rhiem <f.rhiem@fz-juelich.de>'


def action_to_json(action: Action):
    return {
        'action_id': action.id,
        'instrument_id': action.instrument_id,
        'user_id': action.user_id,
        'type': {
            ActionType.SAMPLE_CREATION: 'sample',
            ActionType.MEASUREMENT: 'measurement',
            ActionType.SIMULATION: 'simulation'
        }.get(action.type_id, 'custom'),
        'type_id': action.type_id,
        'name': utils.get_translated_text(
            action.name,
            language_code='en'
        ) or None,
        'description': utils.get_translated_text(
            action.description,
            language_code='en'
        ) or None,
        'is_hidden': action.is_hidden,
        'schema': action.schema
    }


class Action(Resource):
    @multi_auth.login_required
    def get(self, action_id: int):
        try:
            action = get_action(
                action_id=action_id
            )
        except errors.ActionDoesNotExistError:
            return {
                "message": "action {} does not exist".format(action_id)
            }, 404
        if Permissions.READ not in get_user_action_permissions(action_id=action_id, user_id=flask.g.user.id):
            return flask.abort(403)
        return action_to_json(action)


class Actions(Resource):
    @multi_auth.login_required
    def get(self):
        actions = get_actions_with_permissions(user_id=flask.g.user.id, permissions=Permissions.READ)
        return [
            action_to_json(action)
            for action in actions
        ]
