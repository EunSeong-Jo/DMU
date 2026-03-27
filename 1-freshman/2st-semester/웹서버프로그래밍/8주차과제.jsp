<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>

<%= "1. request" %> <br>
<%= "2. response" %> <br>
<%= "3. out" %> <br>
<% out.clear(); %>
<%= "4. application" %> <br>
<%= "5. exception" %> <br>

<br> ---------------------------------------- <br>

<% 
String id = request.getParameter("id"); 
String pwd = request.getParameter("pwd");

out.println("아이디 : " + id + "<BR>");
out.println("암호 : " + pwd);
%>

<br> ---------------------------------------- <br>

<%
String id2 = request.getParameter("strID");
String pwd2 = request.getParameter("strPwd");

out.println("아이디 : " + id2 + "<BR>");
out.println("암호 : " + pwd2);
%>

<br> ---------------------------------------- <br>

<%
String strSite = request.getParameter("download");

switch(Integer.parseInt(strSite))
{
	case 1:
		// response.sendRedirect("http://www.daum.net");
		out.println("daum");
		break;	
	case 2:
		// response.sendRedirect("http://www.naver.com");
		out.println("naver");
		break;
	case 3:
		// response.sendRedirect("http://www.google.com");
		out.println("google");
		break;
	default:
		// response.sendRedirect("http://www.yahoo.com");
		out.println("yahoo");
		break;
}
%>

<br> ---------------------------------------- <br>

<%
String msg = request.getParameter("msg");

int number = Integer.parseInt(request.getParameter("number"));
int count = 0;

while(number>count){
	%>
	<b><%= msg%></b><br>
	<%
		count++;
}
%>

</body>
</html>