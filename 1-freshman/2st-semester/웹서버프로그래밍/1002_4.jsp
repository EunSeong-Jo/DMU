<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<%
String name = request.getParameter("name");
String color = request.getParameter("color");

if(color.equalsIgnoreCase("etc")){
	out.println(color);
	color = "gray";
}
%>
<body bgcolor = <%= color %>>

</body>
</html>