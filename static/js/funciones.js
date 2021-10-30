function crear_usuario(){
    document.getElementById("formulario_signup").action ='/register';
}

function iniciar_sesion(){
    document.getElementById("formulario_login").action ='/login';
}

function buscar_usuario(){
    document.getElementById("formulario_search_home").action ='/search/'+document.getElementById("search-field").value;
}

function actualizar_perfil(){
    document.getElementById("formulario_update").action ='/profile';
}

function entrar_perfil(){
    document.getElementById("formulario_update").action ='/home';
}

function enviar_mensaje(){
    document.getElementById("form_message").action ='/mensaje_send';
}

/*function comentar_post(){
    document.getElementById("form_comment").action ='/publicacion_comment';
}*/

function comentar_post(){
    document.getElementById("form_comment").action ='/comment/create/' + postID;
}

function eliminar_comentario(){    
    document.getElementById("eliminar_post").action ='/comentario_delete/' + commentID;
}

function crear_post(){    
    document.getElementById("form_post").action ='/post/create';
}