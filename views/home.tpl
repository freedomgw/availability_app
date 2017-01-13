<html>
<head>
<script src='/static/lib/jquery.min.js'></script>
<script>
  $(document).ready(function() {
    document.cookie = "user_id=" + {{user_id}} + ";";
  });
</script>

<body>
<b>Welcome Back, {{name}}!</b><br><br>
% if is_babysitter:
  <a href="/availabilities/host/{{user_id}}">Manage Availability!</a><br><br>
% end
<a href="/availabilities/host">View All Available Babysitters</a>
</body>

</head>



