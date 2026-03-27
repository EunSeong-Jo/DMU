<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>

<%
   String name3 = request.getParameter("name3");
   String color = request.getParameter("color");

   if(color.equalsIgnoreCase("etc")){
		color = "gray";
	}
%>

이름 : <%= name3 + "<br>"%>
색 : <%= color%>

<br> ---------------------------------------- <br>

</head>
<body bgcolor = <%= color %>>
<%
String ID = request.getParameter("strID"); 
String pass = request.getParameter("strPwd");

out.println("아이디 : " + ID + "<BR>");
out.println("비밀번호 : " + pass);
%>

<br> ---------------------------------------- <br>

<% request.setCharacterEncoding("euc-kr"); %>
<%
	String name = request.getParameter("name");
	String studentNum = request.getParameter("studentNum");
	String mw = request.getParameter("mw");
	String country = request.getParameter("country");
	
	if(mw.equalsIgnoreCase("man")){
		mw = "남자";
	}
	else{
		mw = "여자";
	}
%>

<h2> 학생 정보 입력 결과</h2>
성명 : <%= name%><p>
학번 : <%= studentNum%><p>
성별 : <%= mw%><p>
국적 : <%= country%><p>

<br> ---------------------------------------- <br>

<%
String name2= request.getParameter("name2");
String studentNum2 = request.getParameter("studentNum2");
%>

<h2> 학생 정보 입력 결과</h2>
성명 : <%= name2%><p>
학번 : <%= studentNum2%><p>

<br> ---------------------------------------- <br>

<!-- head영역과 body태그 -->
 
</body>
</html>