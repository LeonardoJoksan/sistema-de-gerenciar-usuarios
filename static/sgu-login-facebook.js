function loginfb()
{
  $(".login-facebook").html("<img src=\"/static/carregando.gif\" alt=\"Carregando a conexão com facebook\">");
  FB.login(function(response)
  {
    if (response.status === 'connected')
    {
      if (response.authResponse)
      {
          FB.api('/me?fields=id,name,email,permissions', function(response)
          {
            $.ajax({
                type: 'POST',
                url: '/entrar-facebook',
                data: {"uid": response.id, "name": response.name, "email": response.email},
                success: function(data) {
                    $(".login-facebook").html("Login com Facebook");

                    if(data=="loginOK")
                    {
                        window.location.href = "/logado"; 
                    }else
                    {
                        alert(data);
                    }
                }
            });
            /* 
                $(".logado-com-facebook").show();
                $(".login-facebook").hide();
                $(".login-facebook").html("Login com Facebook");
                $(".foto-facebook").html("<img src=\"http://graph.facebook.com/"+response.id+"/picture?type=large\" alt=\"Foto do facebook\">");
                $(".uid-facebook").html("UID: " + response.id);
                $(".nome-facebook").html("Nome: " + response.name);
                $(".email-facebook").html("E-mail: " + response.email); 
            */
          });
      }
      else{
          $(".login-facebook").html("Login com Facebook");
          alert('Usuário cancelou a autorização de login. :(');
      }
    }
    else{
      $(".login-facebook").html("Login com Facebook");
      alert("Conectou não, zé mané...");
    }
  },{scope: 'public_profile,email'});
}