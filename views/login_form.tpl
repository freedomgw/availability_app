<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href='/static/form.css' type="text/css"/>
<style>
  .errors {
    color: red;
    text-align: center;
  }
</style>

</head>

<body>
<h1>Login</h1>

% if get('errors'):
  <p class="errors">{{ errors }}</p>
% end

<div>
  <form action="/login" method="post" enctype="multipart/form-data">
    <label>Email</label>
    <input type="text" name="email"><br>

    <label>Password</label>
    <input type="text" name="password"><br>

    <input type="submit" value="Login">
  </form><br>

  Don’t have an account?
  <a href="/create-user">Sign up</a>
</div>


</body>
</html>