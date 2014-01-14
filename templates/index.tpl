<html>
<head>
	<title>Some awesome page</title>
</head>
<body>
{% if username %}
	Hi there, {{ username }}<br />
	<a href="/logout">Log Out</a>
{% else %}
	<a href="/login">Log In To Twitter</a>
{% endif %}

</body>
</html
