<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href='/static/form.css' type="text/css"/>
</head>
<body>

<h1>Create User</h1><br>

<div>
  <form action="/create-user" method="post" enctype="multipart/form-data">
    <label>Name</label>
    <input type="text" name="name">

    <label>Email</label>
    <input type="text" name="email">

    <label>Password</label>
    <input type="text" name="password">

    <hr>

    <label>Street No</label>
    <input type="text" name="street_no"><br>

    <label>Street Name</label>
    <input type="text" name="street_name"><br>

    <label>City</label>
    <input type="text" name="city"><br>

    <label>Province</label>
    <input type="text" name="province"><br>

    <label>Postal Code</label>
    <input type="text" name="postal_code"><br>

    <label>Country</label>
    <input type="text" name="country"><br>


    <input type="checkbox" name="babysitter" value="1" > I would like to be a babysitter<br><br>
    <input type="submit" value="Submit">
  </form>
</div>

</body>
</html>