from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    name = StringField("Your Name", validators=[
                       DataRequired(), Length(max=1000)])
    email = EmailField("Email", validators=[
                       DataRequired(), Email(), Length(max=100)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(max=100)])
    submit = SubmitField("Register me")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[
                       DataRequired(), Email(), Length(max=100)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(max=100)])
    submit = SubmitField("Log me in")


class CommentForm(FlaskForm):
    comment = StringField("Comment", validators=[
                          DataRequired(), Length(max=1000)])
    submit = SubmitField("Send Comment")
