<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<h2>시간을 쿠키에 저장</h2>
<%
	Cookie cookie2 = new Cookie("user2", "kang2");
	cookie2.setMaxAge(2 * 60);
	response.addCookie(cookie2);
%>
<hr><a href=getcookies.jsp>쿠키 조회</a>

</body>
</html>