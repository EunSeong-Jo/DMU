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
String name = request.getParameter("name");
String tym = request.getParameter("studentNum");
String sex = request.getParameter("mw");
String country = request.getParameter("country");

if(sex.equalsIgnoreCase("man")){
	sex = "남자";
}
else{
	sex = "여자";
}
%>

<h2>학생 정보 입력 결과</h2>
성명 : <%= name %> <br>
학번 : <%= tym %> <br>
성별 : <%= sex %> <br>
국가 : <%= country %>

</body>
</html>