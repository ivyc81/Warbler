from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditProfileForm(FlaskForm):
    """Edit user profile"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Header Image URL')
    bio = TextAreaField('(Optional) Bio')
    show_location = BooleanField('Show location?')
    location = StringField("(Optional) Location")
    password = PasswordField('Password', validators=[DataRequired()])
    time_zone = SelectField('Timezone', choices=[
                                                ("Etc/GMT-12","GMT+12: Auckland, American Samoa"),
                                                ("Etc/GMT-11", "GMT+11: New Caledonia, Solomon Is."),
                                                ("Etc/GMT-10", "GMT+10: Melbourne, Brisbane, Sydney"),
                                                ("Etc/GMT-9", "GMT+9: Osaka, Seoul, Tokyo"),
                                                ("Etc/GMT-8", "GMT+8: Beijing, Singapore, Taipei"),
                                                ("Etc/GMT-7", "GMT+7: Bangkok, Jakarta, Hanoi"),
                                                ("Etc/GMT-6", "GMT+6: Sri Lanka"),
                                                ("Etc/GMT-5", "GMT+5: New Dehli, Calcutta"),
                                                ("Etc/GMT-4", "GMT+4: Abu Dhabi, Muscat, Tehran"),
                                                ("Etc/GMT-3", "GMT+3: Baghdad, Moscow, Kuwait"),
                                                ("Etc/GMT-2", "GMT+2: Cairo, Helsinki, Athens"),
                                                ("Etc/GMT-1", "GMT+1: Burlin, Amsterdam, Paris"),
                                                ("Etc/GMT-0", "GMT: Dublin, London, Portugal"),
                                                ("Etc/GMT+1", "GMT-1: Cape Verde Is."),
                                                ("Etc/GMT+2", "GMT-2: Mid-Atlantic"),
                                                ("Etc/GMT+3", "GMT-3: Buenos Aires, Standard Time Canada"),
                                                ("Etc/GMT+4", "GMT-4: Santiago, Atlantic Standard Time"),
                                                ("Etc/GMT+5", "GMT-5: Montreal, New York, EST"),
                                                ("Etc/GMT+6", "GMT-6: Dallas, Mexico City, CST"),
                                                ("Etc/GMT+7", "GMT-7: Alberta, Salt Lake City, MST"),
                                                ("Etc/GMT+8", "GMT-8: Los Angeles, Tijuana, PST"),
                                                ("Etc/GMT+9", "GMT-9: Alaska"),
                                                ("Etc/GMT+10", "GMT-10: Hawaii"),
                                                ("Etc/GMT+11", "GMT-11: Midway Island"),
                                                ("Etc/GMT+12", "GMT-12: Eniwetok, Kwaialein")])



