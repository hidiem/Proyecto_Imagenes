from flask import Flask, render_template as render, redirect, url_for, request, session, flash
from Formularios import form_Home, form_Login, form_Signup, form_Results, form_EditProfile, form_Message, form_EditProfile, form_PublicProfile, form_Post, form_Dashboad
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from base64 import b64encode
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

User_Name = ""
User_Nombre = ""
User_ID = 0
User_Rol = 0 # 0 = Usuario Normal, 1 = Administrador, 2 = SuperAdministrador
User_Search = ""

lista_mensajes = {
  '1': {'Remitente':'Edilberto','Mensaje':"mensaje 1",'Destinatario':'Helen'},
  '2': {'Remitente':'Edilberto','Mensaje':"mensaje 2",'Destinatario':'Lina'}, 
}

lista_comentarios = {
  '1': {'Propietario_Post':'Edilberto','Comentario':"comentario 1",'Comentador':'Helen'},
  '2': {'Propietario_Post':'Edilberto','Comentario':"comentario 2",'Comentador':'Helen'},  
}


#Ruta Inicio/Home de la Aplicacion
@app.route("/", methods = ["GET", "POST"])
def inicio():
  form = form_Home()
  global User_ID
  global User_Rol
  if 'User' in session:
    User_Name = session['User']
    try:
      with sqlite3.connect("DataBase.db") as con:
        con.row_factory=sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from FinalUsers where User = ?",[User_Name])
        row = cur.fetchone()
        form.name.data = row["Name"]
        form.user.data = row["User"]
        form.email.data = row["Email"]
        form.date.data = datetime.strptime(row["Date"], '%Y-%m-%d')
        form.gender.data = row["Gender"]
        form.description.data = row["Description"]
        form.localization.data = row["Localization"]
        image = b64encode(row["Photo"]).decode("utf-8")

        User_Name = row["Name"]
        User_ID = int(row["Id"])
        User_Rol = int(row["Rol"])
         
        cur = con.cursor()
        cur.execute("select * from Posts where Post_authorID = ? order by Post_ID desc limit 10",[User_ID])
        rows = cur.fetchall()
              
        lista_Fotos = {}
        for row in rows:          
          lista_Fotos[ row['Post_ID'] ] = b64encode( row["Post_photo"] ).decode("utf-8") 

        cur = con.cursor()
        cur.execute("select * from Posts order by Post_ID desc limit 40")
        rows2 = cur.fetchall()

        lista_Posts = {}
        for row2 in rows2:          
          lista_Posts[ row2['Post_ID'] ] = b64encode( row2["Post_photo"] ).decode("utf-8")     

        cur = con.cursor()
        cur.execute("select * from FinalUsers")
        rows3 = cur.fetchall()

        lista_FotosPerfil = {}
        for row3 in rows3:          
          lista_FotosPerfil[ row3['Id'] ] = b64encode( row3["Photo"] ).decode("utf-8")

        cur = con.cursor()
        cur.execute("select * from Comments order by Comment_ID desc")
        rows4 = cur.fetchall()
        #for row4 in rows4:
          #print(row4["Comment_content"])

    except:
      con.rollback()
    return render("Home_Page.html", form = form, User_Rol=User_Rol, image = image, User_Name=User_Name, rows3=rows3, lista_FotosPerfil=lista_FotosPerfil, rows2=rows2, lista_Posts=lista_Posts, lista_comentarios = lista_comentarios, rows= rows, rows4=rows4, lista_Fotos = lista_Fotos)
  else:
    return render("Inicio_Page.html")


@app.route('/comment/create/<postID>', methods = ["GET", "POST"])
def comentario(postID):
  global User_Name
  User_Name = session['User']
  form = form_Home()
  comentario = form.comment_box.data

  date_now=datetime.now()
  date_format=date_now.strftime('%d/%m/%Y, %H:%M')  

  try:
    with sqlite3.connect("DataBase.db") as con:
      print("Hizo la coneccion")
      con.row_factory=sqlite3.Row
      cur = con.cursor()
      cur.execute("select * from FinalUsers where User = ?",[User_Name])
      row = cur.fetchone()
      user_id = row["Id"]
      user_name = row["Name"]   
      #form.date.data = datetime.strptime(row["Date"], '%Y-%m-%d')
          
      cur = con.cursor()
      if comentario != None:
        cur.execute("insert into Comments(Comment_postID, Comment_content, Comment_author, Comment_date) values (?, ?, ?, ?)", (postID, comentario, user_name, date_format))
      con.commit()
      #return render('EditProfile_Page.html', form = form, User_Name = User_Name)
      flash("Comentario Creado Exitosamente", "primary") 
      
      return redirect('/')
        
  except:
    con.rollback()
    
  return redirect('/')


#RUTA Eliminar comentario
@app.route("/comentario_delete/<commentID>", methods = ["GET","POST"])
def eliminar_comentario(commentID):
  try:
      with sqlite3.connect("DataBase.db") as con:
        cur = con.cursor()
        cur.execute("delete from Comments where Comment_ID = ?",[commentID])
        con.commit()
        if con.total_changes > 0:
          flash("Comentario Borrado Exitosamente", "primary")

          return redirect("/")            
  
  except:
    con.rollback()
  
  return redirect("/")


#RUTA Eliminar comentario
@app.route("/post_delete/<postID>", methods = ["GET","POST"])
def eliminar_post(postID):
  try:
      with sqlite3.connect("DataBase.db") as con:
        cur = con.cursor()
        cur.execute("delete from Posts where Post_ID = ?",[postID])
        con.commit()
        if con.total_changes > 0:
          flash("Post Borrado Exitosamente", "primary")

          return redirect("/")            
  
  except:
    con.rollback()
  
  return redirect("/")


#Ruta Pagina de Inicio (cerrar sesion)
@app.route("/logout", methods = ["POST"])
def salir():
  if "User" in session:
    session.pop("User", None)
    #session["name"] = None
    flash("Sesion Cerrada", "primary")
    return redirect("/")    
  else:
    return redirect("/")


#Ruta Pagina Registrarse
@app.route("/register", methods = ["GET", "POST"])
def registro():    
  form = form_Signup()
  if request.method=="GET":
    return render("SignUp_Page.html", form = form)
  else:
    name = escape(request.form["name"])
    user = escape(request.form["user"])
    email = escape(request.form["email"])
    password = escape(request.form["password"])
    passwordcript =  generate_password_hash(password) #Cifrar clave
    date = escape(request.form["date"])
    gender = escape(request.form["gender"])

    if gender == "Femenino":
      filename = url_for('static', filename='img/profile_female.jpg')
    else:
      filename = url_for('static', filename='img/profile_male.jpg')
    
    with open(os.path.dirname(os.path.abspath(__file__)) + filename, 'rb') as picture:
      photo = picture.read()    

    try:
      with sqlite3.connect("DataBase.db") as con:
        cur = con.cursor()
        cur.execute("insert into FinalUsers(Name, User, Email, Password, Date, Gender, Description, Localization, Rol, Photo) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, user, email, passwordcript, date, gender, "", "", 0, photo))
        con.commit()
        #flash ("Cuenta Creada")
        return redirect("/login")
    except:
      con.rollback()

  #return "No se puede crear el usuario!"
  return render("SignUp_Page.html", form = form)


#Ruta Pagina Loguearse
@app.route("/login", methods = ["GET", "POST"])
def ingreso():
  form = form_Login()
  global User_Name
  if request.method == "GET":
    return render("LogIn_Page.html", form = form)
  else:
    #user = form.user.data
    #password = form.password.data
    user = escape(request.form["user"])
    password = escape(request.form["password"])
    try:
      with sqlite3.connect("DataBase.db") as con:
        cur = con.cursor()
        #cur.execute("select * from FinalUser where Email = '"+email+"' and Password = '"+password+"' ")
        #cur.execute("select * from FinalUser where Email = ? and Password = ?", [email, password])
        clave = cur.execute("select Password from FinalUsers where User = ?",[user]).fetchone()
        if clave != None:
          clavehash = clave[0]
          if check_password_hash(clavehash, password):
            session['User'] = request.form.get("user")   
            flash("Bienvenido {}".format(user), "primary")    
            return redirect('/', code=307)
            
          else:
            flash("Usuario {} o contraseña incorrecta, por favor verifique sus datos".format(user), "warning")
            render("LogIn_Page.html", form = form)
          
    except:
      con.rollback()

  #return "No se puede crear el usuario!"
  return render("LogIn_Page.html", form = form)   


#Ruta Pagina MI PERFIL
@app.route("/profile", methods = ["GET", "POST"])
def perfil():  
  form = form_EditProfile()

  if request.method == "GET" and 'User' in session:
    User_Name = session['User']
    global User_ID
    global User_Nombre

    try:
      with sqlite3.connect("DataBase.db") as con:
        con.row_factory=sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from FinalUsers where User = ?",[User_Name])
        row = cur.fetchone()
        form.name.data = row["Name"]
        form.user.data = row["User"]
        form.email.data = row["Email"]
        #form.password.data = row["Password"]
        form.date.data = datetime.strptime(row["Date"], '%Y-%m-%d')
        form.gender.data = row["Gender"]
        form.description.data = row["Description"]
        form.localization.data = row["Localization"]
        image = b64encode(row["Photo"]).decode("utf-8")
        User_Nombre = row["Name"]

        cur = con.cursor()
        cur.execute("select * from Posts where Post_authorID = ? order by Post_ID desc limit 10",[User_ID])
        rows = cur.fetchall()
              
        lista_Fotos = {}
        for row in rows:          
          lista_Fotos[ row['Post_ID'] ] = b64encode( row["Post_photo"] ).decode("utf-8")
      
    except:
      con.rollback()
    
    return render('EditProfile_Page.html', form = form, image = image, User_Name = User_Name, User_Nombre = User_Nombre, rows=rows, lista_Fotos=lista_Fotos)
  

  elif request.method == "POST" and 'User' in session:
    picture = request.files['picture']
    #filename = secure_filename(picture.filename)
    #filetype = picture.mimetype

    try:
        with sqlite3.connect("DataBase.db") as con:          
          name = escape(request.form["name"])
          user = escape(request.form["user"])         
          #email = escape(request.form["email"])
          password = escape(request.form["password"])
          passwordcript =  generate_password_hash(password) #Cifrar clave
          date = escape(request.form["date"])
          gender = escape(request.form["gender"])
          description = escape(request.form["description"])
          localization = escape(request.form["localization"])        
          photo = picture.read()  
          cur = con.cursor()
          print("Entro 1")
          if request.files['picture'].filename != '':            
            cur.execute("update FinalUsers set Name=?, Password=?, Date=?, Gender=?, Description=?, Localization=?, Photo=? where User=?",[name, passwordcript, date, gender, description, localization, photo, user]) 
          else:
            cur.execute("update FinalUsers set Name=?, Password=?, Date=?, Gender=?, Description=?, Localization=? where User=?",[name, passwordcript, date, gender, description, localization, user])
          con.commit()
          flash("Cambios Realizados Exitosamente", "primary")
          #return render('EditProfile_Page.html', form = form, User_Name = User_Name)          
          return redirect('/profile')   
          
    except:
      con.rollback() 
    return redirect('/profile')


  else:
    return redirect("/") 


#Ruta Pagina Crear un Post (MIO)
@app.route("/create_post", methods = ["GET", "POST"])
def crear_publicacion():
  form = form_Post()

  return render('Post_Page.html', form = form)


@app.route('/post/create', methods = ["GET", "POST"])
def publicacion():
  form = form_Post()
  if 'User' in session:
      User_Name = session['User']

  picture = request.files['picture']
  #filename = secure_filename(picture.filename)
  #filetype = picture.mimetype
  date_now=datetime.now()
  date_format=date_now.strftime('%d/%m/%Y, %H:%M')  

  try:
    with sqlite3.connect("DataBase.db") as con:
      con.row_factory=sqlite3.Row
      cur = con.cursor()
      cur.execute("select * from FinalUsers where User = ?",[User_Name])
      row = cur.fetchone()
      user_id = row["Id"]
      user_name = row["Name"]     
      #form.date.data = datetime.strptime(row["Date"], '%Y-%m-%d')

      title = escape(request.form["title"])
      description = escape(request.form["description"])
      
      photo = picture.read()        
      cur = con.cursor()
      if request.files['picture'].filename != '':
        cur.execute("insert into Posts(Post_authorID, Post_title, Post_description, Post_author, Post_date, Post_photo) values (?, ?, ?, ?, ?, ?)", (user_id, title, description, user_name, date_format, photo))
      con.commit()
      #return render('EditProfile_Page.html', form = form, User_Name = User_Name)
      flash("Publicacion Creada Exitosamente", "primary") 
      
      return redirect('/profile')
        
  except:
    con.rollback()
    
  return redirect('/create_post')


#Ruta Pagina Perfil Publico OTROS USUARIOS
@app.route("/user/<user>", methods = ["GET", "POST"])
def perfil_usuario(user):
#  global User_Search
  form = form_PublicProfile()
  global User_Nombre
  global User_Name
  global User_ID

  try:
    with sqlite3.connect("DataBase.db") as con:
      con.row_factory=sqlite3.Row
      cur = con.cursor()
      cur.execute("select * from FinalUsers where User = ?",[user])
      row = cur.fetchone()
      form.name.data = row["Name"]
      form.user.data = row["User"]
      form.email.data = row["Email"]
      form.date.data = datetime.strptime(row["Date"], '%Y-%m-%d')
      form.gender.data = row["Gender"]
      form.description.data = row["Description"]
      form.localization.data = row["Localization"]
      image = b64encode(row["Photo"]).decode("utf-8")

      User_ID = row["Id"]
      User_Nombre = row["Name"]
      User_Name = row["User"]      

      cur = con.cursor()
      cur.execute("select * from Posts where Post_authorID = ? order by Post_ID desc limit 10", [User_ID])
      rows = cur.fetchall()      
            
      lista_Fotos = {}
      for row in rows:          
        lista_Fotos[ row['Post_ID'] ] = b64encode( row["Post_photo"] ).decode("utf-8")
        #print(lista_Fotos[ row['Post_ID'] ])        

      return render('PublicProfile_Page.html', image = image, User_Name=User_Name, User_Nombre=User_Nombre, lista_Fotos=lista_Fotos, rows=rows, form=form)
 
  except:
    con.rollback()
 
  return render('PublicProfile_Page.html',form=form)
    

#Ruta Ver un Post de OTRO USUARIO
@app.route("/post/<username>/<id_post>", methods = ["GET"])
def ver_publicacion(username, id_post):
  return render('Post_Page.html')
  

#Ruta Buscar USUARIOS
@app.route("/search/<user>", methods = ["GET", "POST"])
def resultado_busqueda(user):
  global User_Search 
  global User_Rol
  form = form_Results()
  form.user_search.data = user
  User_Search = user+'%'
  images = []  
  try:
    with sqlite3.connect("DataBase.db") as con:
      con.row_factory=sqlite3.Row
      cur = con.cursor()
      cur.execute("select * from FinalUsers where Name like ?", [User_Search])
      rows = cur.fetchall()

      lista_Fotos = {}
      for row in rows:        
        lista_Fotos[ row["User"] ] = b64encode( row["Photo"] ).decode("utf-8")          
        #print( row["User"] )
        #print(lista_Fotos[ row["User"] ])

      return render('Results_Page.html', User_Search=User_Search, images=images, lista_Fotos=lista_Fotos, User_Rol = User_Rol, rows = rows, form = form)

  except:
    con.rollback()
 
  return render('Results_Page.html', form = form)
 
 
#RUTA Eliminar usuario
@app.route("/delete_user/<user>", methods = ["GET", "POST"])
def eliminar_usuario(user):
  try:
    with sqlite3.connect("DataBase.db") as con:
      cur = con.cursor()
      cur.execute("delete from FinalUsers where User = ?",[user])
      con.commit()
      if con.total_changes > 0:
        return redirect("/dashboard")
 
  except:
      con.rollback()
 
  return redirect("/search")


#Ruta Acceder a Dashboard
@app.route("/dashboard", methods = ["GET", "POST"])
def entrar_dashboard():
  form = form_Dashboad
  Usuarios = 0
  Publicaciones = 0
  Comentarios = 0
  Mensajes = 0

  try:
    with sqlite3.connect("DataBase.db") as con:
      con.row_factory=sqlite3.Row
      cur = con.cursor()
      cur.execute("select * from FinalUsers order by Id desc")       
      rows = cur.fetchall()

      lista_FotosPerfil = {}
      for row in rows:          
        lista_FotosPerfil[ row['User'] ] = b64encode( row["Photo"] ).decode("utf-8")    
        Usuarios = Usuarios + 1        

      cur = con.cursor()
      cur.execute("select * from Posts")      
      rows2 = cur.fetchall()      
      for row2 in rows2: 
        Publicaciones = Publicaciones + 1         

      cur = con.cursor()
      cur.execute("select * from Comments")      
      rows3 = cur.fetchall()
      for row3 in rows3: 
        Comentarios = Comentarios + 1

  except:
    con.rollback()    
  
  return render('index.html', form = form, rows = rows, lista_FotosPerfil = lista_FotosPerfil, Usuarios=Usuarios, Publicaciones=Publicaciones, Comentarios=Comentarios)


#Ruta Contactenos
@app.route("/contact", methods = ["GET", "POST"])
def contactar():
  return render('Contact_page.html')


#RUTA Enviar mensaje
@app.route("/mensaje_send/<user>", methods = ["GET", "POST"])
def enviar_mensaje(user):
  global lista_mensajes
  User_Name = session['User']
  form = form_Message()  
  form.user1.data = User_Name
  form.user2.data = user
  mensaje = form.message_box.data
  if mensaje != None:
    key = str(len(lista_mensajes) + 1)
    lista_mensajes[key] = {'Remitente' : User_Name,'Mensaje' : mensaje,'Destinatario' : user}
  return render('Message_Page.html', form = form, lista_mensajes = lista_mensajes)


#RUTA Eliminar mensaje
@app.route("/mensaje_delete/<keymessage>", methods = ["GET", "POST"])
def eliminar_mensaje(keymessage):
  global lista_mensajes
  if keymessage != None:
    del lista_mensajes[keymessage]
    #lista_mensajes.pop(keymessage)
  return redirect("/mensaje_send")


#RUTA Comentar post
@app.route("/publicacion_comment", methods = ["GET", "POST"])
def comentar_publicacion():
  global lista_comentarios
  if 'User' in session:
    User_Name = session['User']
    form = form_Home()
    comentario = form.comment_box.data
    if comentario != None:
      key = str(len(lista_comentarios) + 1)
      lista_comentarios[key] = {'Propietario_Post' : 'Other','Comentario' : comentario,'Comentador' : User_Name}
    return redirect("/")
  else:
    return redirect("/")


#RUTA Eliminar comentario
#@app.route("/comentario_delete/<keycomment>", methods = ["GET","POST"])
#def eliminar_comentario(keycomment):
#  global lista_comentarios
#  del lista_comentarios[keycomment]
#  return redirect("/")

#EJECUCION INICIAL
@app.before_request
def pre_inicio():
  if "User" not in session and request.endpoint in ["perfil","editar_perfil","crear_publicacion","comentar_publicacion","estudiante_edit","entrar_dashboard"]:
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)