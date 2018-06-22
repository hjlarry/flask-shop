# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


REFUND_STATUS_PENDING = 'pending'
REFUND_STATUS_APPLIED = 'applied'
REFUND_STATUS_PROCESSING = 'processing'
REFUND_STATUS_SUCCESS = 'success'
REFUND_STATUS_FAILED = 'failed'

SHIP_STATUS_PENDING = 'pending'
SHIP_STATUS_DELIVERED = 'delivered'
SHIP_STATUS_RECEIVED = 'received'
