from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField,SelectField,TextAreaField, DateTimeField, PasswordField, FileField
from wtforms.validators import DataRequired,Length, InputRequired, EqualTo
 
class form_Login(FlaskForm):
    user = StringField("Usuario: ", validators=[InputRequired('Un usuario es requerido!'),DataRequired(message="No Dejar Vacio, Completar")])
    password = StringField("Contraseña: ", validators=[InputRequired('Un usuario es requerido!'), Length(min=8, message='longitud minima 8 caracteres')]) 
    login = SubmitField("Iniciar Sesión", render_kw={"onmouseover":"iniciar_sesion()"})
 
class form_Signup(FlaskForm):
    name = StringField("Nombre: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    user = StringField("Usuario: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    email = StringField("Correo Electronico: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    password = PasswordField("Contraseña: ", validators=[DataRequired(message="No Dejar Vacio, Completar"), Length(min=8), EqualTo('password2', message='Las contraseñas no son iguales')]) 
    date = DateField("Fecha: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    gender = SelectField("Genero: ", choices=[("Masculino"),("Femenino"),("Otro")])
    signup = SubmitField("Crear Cuenta", render_kw={"onmouseover":"crear_usuario()"})

class form_Home(FlaskForm):
    user_search = StringField("", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    search = SubmitField("Buscar Usuario", render_kw={"onmouseover":"buscar_usuario()"})

    name = StringField("Nombre: ")
    user = StringField("Usuario: ")
    email = StringField("Correo Electronico: ")
    date = DateField("Fecha: ")
    gender = StringField("Genero: ")
    description = TextAreaField("Descripción: ")
    localization = StringField("Localización: ")
    picture = FileField("Subir Imagen")
    update = SubmitField("Actualizar Perfil", render_kw={"onmouseover":"actualizar_perfil()"})

    comment_box = TextAreaField("", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    send = SubmitField("Publicar", render_kw={"onmouseover":"comentar_post()"})

class form_Results(FlaskForm):
    user_search = StringField("", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    search = SubmitField("Buscar Usuario", render_kw={"onmouseover":"buscar_usuario()"})

class form_EditProfile(FlaskForm):
    name = StringField("Nombre: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    user = StringField("Usuario: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    email = StringField("Correo Electronico: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    password = StringField("Contraseña: ", validators=[DataRequired(message="No Dejar Vacio, Completar"), Length(min=8)]) 
    date = DateField("Fecha: ", validators=[DataRequired(message="No Dejar Vacio, Completar")], format='%Y-%m-%d')
    gender = SelectField("Genero: ", choices=[("Masculino"),("Femenino"),("Otro")])
    description = TextAreaField("Descripción: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    localization = StringField("Localización: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    picture = FileField("Subir Imagen")
    update = SubmitField("Guardar Cambios", render_kw={"onmouseover":"actualizar_perfil()"})

class form_Message(FlaskForm):
    message_box = TextAreaField("", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    user1 = StringField("Remitente: ")
    user2 = StringField("Destinatario: ") 
    send = SubmitField("Enviar Mensaje", render_kw={"onmouseover":"enviar_mensaje()"})

class form_PublicProfile(FlaskForm):
    name = StringField("Nombre: ")
    user = StringField("Usuario: ")
    email = StringField("Correo Electronico: ")
    date = DateField("Fecha: ")
    gender = StringField("Genero: " )
    description = TextAreaField("Descripción: ")
    localization = StringField("Localización: ")

class form_Post(FlaskForm):
    title = StringField("Titulo: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    description = TextAreaField("Descripción: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    picture = FileField("Imagen")
    post = SubmitField("Publicar Fotos", render_kw={"onmouseover":"crear_post()"})

class form_Dashboad(FlaskForm):
    user_search2 = StringField("Hola: ", validators=[DataRequired(message="No Dejar Vacio, Completar")])
    search2 = SubmitField("Buscar Usuario", render_kw={"onmouseover":"buscar_usuario()"})
    users = StringField("Usuarios: ")
    posts = StringField("Publicaciones: ")
    comments = StringField("Comentarios")
    messages = StringField("Mensajes")    