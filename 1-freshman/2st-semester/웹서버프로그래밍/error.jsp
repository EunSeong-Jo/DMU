<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<%@ page isErrorPage = "true" %>
<h1>예외처리 페이지</h1>
오류 문자열 : <%= exception.toString() %><br>
오류 메시지 : <%= exception.getMessage() %><br>
</body>
</html>