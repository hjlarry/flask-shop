# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from .models import User


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=25),
            Regexp(
                "^[a-zA-Z0-9]*$",
                message="The username should contain only a-z, A-Z and 0-9.",
            ),
        ],
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username Or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        if "@" in self.username.data:
            self.user = User.query.filter_by(email=self.username.data).first()
        else:
            self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.is_active:
            self.username.errors.append("User not activated")
            return False
        return True


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField(
        "Verify password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
        self.user = current_user

    def validate(self):
        """Validate the form."""
        initial_validation = super().validate()
        if not initial_validation:
            return False

        if not self.user.check_password(self.old_password.data):
            self.old_password.errors.append("Invalid password")
            return False

        return True


class AddressForm(FlaskForm):
    """Address form."""

    province = StringField("Province", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    district = StringField("District", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    contact_name = StringField("Contact name", validators=[DataRequired()])
    contact_phone = StringField(
        "Contact Phone", validators=[DataRequired(), Length(min=11, max=11)]
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
