# coding: utf-8
"""

"""

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FloatField, TextAreaField, HiddenField, FileField, StringField, BooleanField
from wtforms.validators import InputRequired, ValidationError

from ...logic import errors
from ...models import Permissions
from ...logic.publications import simplify_doi
from ...logic.errors import InvalidDOIError

from ..validators import ObjectIdValidator
from ...logic.utils import parse_url


class ObjectForm(FlaskForm):  # type: ignore[misc]
    pass


class ObjectVersionRestoreForm(FlaskForm):  # type: ignore[misc]
    pass


class CommentForm(FlaskForm):  # type: ignore[misc]
    content = TextAreaField(validators=[InputRequired()])


class FileForm(FlaskForm):  # type: ignore[misc]
    file_source = HiddenField(validators=[InputRequired()])
    file_names = HiddenField()
    local_files = FileField()

    def validate_file_source(form, field: StringField) -> None:
        if field.data not in ['local']:
            raise ValidationError('Invalid file source')


def _validate_url(url: str) -> None:
    try:
        parse_url(url)
    except errors.InvalidURLError:
        raise ValidationError(0)
    except errors.URLTooLongError:
        raise ValidationError(1)
    except errors.InvalidIPAddressError:
        raise ValidationError(2)
    except errors.InvalidPortNumberError:
        raise ValidationError(3)


class ExternalLinkForm(FlaskForm):  # type: ignore[misc]
    url = StringField()

    def validate_url(form, field: StringField) -> None:
        _validate_url(field.data)


class FileInformationForm(FlaskForm):  # type: ignore[misc]
    title = StringField()
    url = StringField()
    description = TextAreaField()

    def validate_url(form, field: StringField) -> None:
        if field.data is not None:
            _validate_url(field.data)


class FileHidingForm(FlaskForm):  # type: ignore[misc]
    reason = TextAreaField()


class ObjectLocationAssignmentForm(FlaskForm):  # type: ignore[misc]
    location = SelectField(validators=[InputRequired()])
    responsible_user = SelectField(validators=[InputRequired()])
    description = StringField()


class ObjectPublicationForm(FlaskForm):  # type: ignore[misc]
    doi = StringField()
    title = StringField()
    object_name = StringField()

    def validate_doi(form, field: StringField) -> None:
        try:
            field.data = simplify_doi(field.data)
        except InvalidDOIError:
            raise ValidationError('Please enter a valid DOI')


class CopyPermissionsForm(FlaskForm):  # type: ignore[misc]
    object_id = SelectField(validators=[ObjectIdValidator(Permissions.GRANT), InputRequired()], validate_choice=False)


class ObjectNewShareAccessForm(FlaskForm):  # type: ignore[misc]
    component_id = IntegerField(validators=[InputRequired()])

    data = BooleanField()
    action = BooleanField()
    users = BooleanField()
    files = BooleanField()
    comments = BooleanField()
    object_location_assignments = BooleanField()


class ObjectEditShareAccessForm(FlaskForm):  # type: ignore[misc]
    component_id = IntegerField(validators=[InputRequired()])

    data = BooleanField()
    action = BooleanField()
    users = BooleanField()
    files = BooleanField()
    comments = BooleanField()
    object_location_assignments = BooleanField()


class UseInActionForm(FlaskForm):  # type: ignore[misc]
    action_type_id = HiddenField()
    action_id = HiddenField()
    objects = HiddenField(validators=[InputRequired()])


class GenerateLabelsForm(FlaskForm):  # type: ignore[misc]
    form_variant = SelectField(validators=[InputRequired()], choices=[('mixed-formats', lazy_gettext('Mixed label formats')), ('fixed-width', lazy_gettext('Fixed-width labels')), ('minimal-height', lazy_gettext('Minimal-height labels'))])
    objects = HiddenField(validators=[InputRequired()])
    paper_size = SelectField(validators=[InputRequired()], choices=[("DIN A4 (Portrait)", lazy_gettext('DIN A4 (Portrait)')), ("DIN A4 (Landscape)", lazy_gettext('DIN A4 (Landscape)')), ("Letter (Portrait)", lazy_gettext('Letter / ANSI A (Portrait)')), ("Letter (Landscape)", lazy_gettext('Letter / ANSI A (Landscape)'))])
    label_width = FloatField()
    min_label_width = FloatField()
    min_label_height = FloatField()
    labels_per_object = IntegerField()
    center_qr_ghs = BooleanField()
    qr_ghs_side_by_side = BooleanField()
    include_qr = BooleanField()
