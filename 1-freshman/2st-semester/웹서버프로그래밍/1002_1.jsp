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
request.setCharacterEncoding("euc-kr");
%>

<%
String name = request.getParameter("name");
String addr = request.getParameter("addr");
String tel = request.getParameter("tel");
%>

<h2>학생 정보 입력 결과</h2>
성명 : <%= name %> <br>
주소 : <%= addr %> <br>
연락처 : <%= tel %> <br>

</body>
</html>