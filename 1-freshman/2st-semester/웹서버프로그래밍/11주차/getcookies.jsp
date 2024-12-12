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
Cookie[] cookies = request.getCookies();

if (cookies == null){
	out.println("쿠키가 없습니다");
}
else{
	for(Cookie c : cookies){
		out.println("쿠키이름 : " + c.getName() + ", ");
		out.println("쿠키값 : " + c.getValue() + "<br>");
	}
}
	/*
	for(int i = 0; i < cookies.length; ++i){
		out.prntln("쿠키이름 : " + cookies[i].getName() + ", ");
		out.prntln("쿠키값 : " + cookies[i].getValue() + "<br>");
	}
}*/
%>

</body>
</html>