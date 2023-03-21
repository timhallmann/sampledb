# coding: utf-8
"""
Add the show_linked_object_data column to the instruments table.
"""

import os

import flask_sqlalchemy

from .instruments_add_object_id import MIGRATION_INDEX as PREVIOUS_MIGRATION_INDEX
from .utils import table_has_column

MIGRATION_INDEX = PREVIOUS_MIGRATION_INDEX + 1
MIGRATION_NAME, _ = os.path.splitext(os.path.basename(__file__))


def run(db: flask_sqlalchemy.SQLAlchemy) -> bool:
    # Skip migration by condition
    if table_has_column('instruments', 'show_linked_object_data'):
        return False

    # Perform migration
    db.session.execute(db.text("""
        ALTER TABLE instruments
        ADD show_linked_object_data BOOLEAN DEFAULT TRUE NOT NULL
    """))
    return True
