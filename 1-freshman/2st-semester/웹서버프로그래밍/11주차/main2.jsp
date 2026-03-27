<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>

<%
String s_name = "";

if (session.getAttribute("name") == null){
	response.sendRedirect("login2.html");
}

s_name = (String)session.getAttribute("name");
%>

<form method="post" action="login2.jsp">

<%= s_name %>님 안녕하세요. <br>
welcome my page <br>
plz enjoy it <br>

<input type="submit" value="로그아웃">
</form>

</body>
</html>