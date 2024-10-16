<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<% // request.setCharacterEncoding("euc-kr"); %>
<%
	String studentNum = request.getParameter("studentNum");
	String[] majors = request.getParameterValues("major");
%>
<h2> 학생 정보 입력 결과</h2>
학번 : <%= studentNum %><p>
전공 : <% 
			if (majors == null) {
     			out.println("전공 없음.");				
			} else {
				for (String eachmajor : majors) 
	     			     out.println(eachmajor + " ");
			}
	  %>

<br> ---------------------------------------- <br>

<%@page import="java.util.Enumeration" %>
<% //request.setCharacterEncoding("euc-kr"); %>

<h2> 취미와 가보고 싶은 국가 결과</h2>
<%
	Enumeration<String> e = request.getParameterNames();

   	while ( e.hasMoreElements() ) {
   		String name = e.nextElement();
   		String [] data = request.getParameterValues(name);
		if (data != null) {
			for ( String eachdata : data ) 
     			out.println(eachdata + " ");
		}
		out.println("<p>");
   	}
%>

<br> ---------------------------------------- <br>

<h2>기술정보 이력서</h2>
	<% // request.setCharacterEncoding("euc-kr"); %>
	이름 : <%= request.getParameter("name") %><br>
	주민번호 : <%= request.getParameter("jnum1") %> - <%= request.getParameter("jnum2") %><br>
	학력 : <%= request.getParameter("graduate") %><br>
	전공 : <%= request.getParameter("major1") %><br>
	경험 플랫폼 : 
	<% 
		for ( String platform : request.getParameterValues("platform")) {
			out.println("[" + platform + "] ");
		}
	%>

<br> ---------------------------------------- <br>

<%@ page import="java.util.Enumeration" %>
<% // request.setCharacterEncoding("euc-kr"); %>

<h2>기술정보 이력서 - Enumeration</h2>
<%
	Enumeration<String> e1 = request.getParameterNames();

   	while ( e1.hasMoreElements() ) {
  		String name1 = e1.nextElement();
   		String [] data1 = request.getParameterValues(name1);
		if (data1 != null) {
			for ( String eachdata1 : data1 ) 
     			out.println(eachdata1 + " ");
		}
		out.println("<p>");
   	}
%>

<br> ---------------------------------------- <br>

<%
int num1 = Integer.parseInt(request.getParameter("num1"));
int num2 = Integer.parseInt(request.getParameter("num2"));

out.println(num1 + " + " + num2 + " = " + (num1+num2) + "<br>");
out.println(num1 + " / " + num2 + " = " + ((double)num1/num2) + "<br>");
%>

</body>
</html>