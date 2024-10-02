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
String id = request.getParameter("strID");
String pass = request.getParameter("strPwd");

out.println("아이디 : " + id + "<br>");
out.println("비밀번호 : " + pass + "<br>");
%>
</body>
</html>