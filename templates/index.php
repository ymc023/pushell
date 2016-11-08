<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Pushell Token</title>
        <link rel="shortcut icon" href="/static/img/pushell.ico">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- CSS -->
        <link rel="stylesheet" href="/static/css/reset.css">
        <link rel="stylesheet" href="/static/css/supersized.css">
        <link rel="stylesheet" href="/static/css/loginstyle.css">
        <link rel="stylesheet" href="/static/css/xcConfirm.css">
	<link rel="stylesheet" href="/static/css/style4.css" />     
        <!-- Javascript -->
        <script src="/static/js/jquery-1.9.1.js" type="text/javascript" charset="utf-8"></script>
        <script src="/static/js/xcConfirm.js" type="text/javascript" charset="utf-8"></script>
        <script src="/static/js/jquery-1.8.2.min.js"></script>
        <script src="/static/js/supersized.3.2.7.min.js"></script>
        <script src="/static/js/supersized-init.js"></script>
        <script src="/static/js/scripts.js"></script>
    </head>
 <body>
    <div style="position:fixed; right:0; bottom:0" id="time"></div>  
       <script type="text/javascript">  
            function get_obj(time){  
            return document.getElementById(time);  
            }  
            var ts='.(round(microtime(true)*1000)).';  
            function getTime(){  
              var t=new Date(ts);  
              with(t){  
              var _time=""+getFullYear()+"-" + (getMonth()+1)+"-"+getDate()+" " + (getHours()<10 ? "0" :"") + getHours() + ":" + (getMinutes()<10 ? "0" :"") + getMinutes() + ":" + (getSeconds()<10 ? "0" :"") + getSeconds();  
                }  
              get_obj("time").innerHTML=_time;  
              setTimeout("getTime()",1000);  
              ts+=1000;  
            }  
            getTime();  
    </script>';  
 <div class="page-container">
  <h1>Pushell Token</h>
     <script type="text/javascript"> 
      function auth_check(){
        var objusername=document.forms['auth_form'].username;
        var auth_code=objusername.value;
      //document.write(auth_code);
      if (auth_code=="" ){
          return false;
        }
      else
         { document.forms[0].submit(); }
     }
    </script>
  <form id="auth_form" name="auth_form" action="" method="post">
   <input type="text" name="username" class="username" placeholder="Authentication Code"/>
    <button id="auth_button" type="submit" class="a-btn" name="auth_button" onclick="auth_check" /> 
               <span class="a-btn-text" onclick="auth_check()">Enter</span>
               <span class="a-btn-slide-text" onclick="auth_check()">Sign in!</span>
	       <span class="a-btn-icon-right" onclick="auth_check()"></span>
        </button>
	<div class="error"><span>+</span></div>	 
        </form> 
        </div>
</body>
</html>

