<head>
  <script src="/static/lib/jquery.cookie.min.js"></script>
  <script>
    $(document).ready(function() {
      if ($.cookie("user_id")) {
        $("#logged_in_logged_out").attr("href", "/logout");
      } else {
        $("#logged_in_logged_out").attr("href", "/login");
      }
      // if ($.cookie("user_id"))
    });
  </script>
</head>

<a id="logged_in_logged_out">hello</a>

