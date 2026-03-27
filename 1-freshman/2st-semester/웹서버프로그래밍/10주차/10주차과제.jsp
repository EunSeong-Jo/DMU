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
	String name = "include";
%>

<%@include file="10주차과제_red.jsp"%>
include 지시자의 green 부분입니다.
<%@include file="10주차과제_blue.jsp"%>


<br> ---------------------------------------- <br>

<%--
<% int i = 12; %>
<% int n = 365; %>
1 년은 <%=i %>달 입니다.
<     (1)                (2)     ="paramsub.jsp" >
	<   (3)      name="weeks" value="52"    (4)     >
</jsp:include>
1 년은 <%=n %>일 입니다.
--%>

<br> ---------------------------------------- <br>


<% int i = 12; %>
<% int n = 365; %>
1 년은 <%=i %>달 입니다.

<%-- 
<jsp:forward page="10주차과제_paramsub.jsp" >
	<jsp:param name="weeks" value="52" />
</jsp:forward>
--%>

1 년은 <%=n %>일 입니다.
 

<br> ---------------------------------------- <br>


1. 태그 param이 없는 태그 include <p> 
<jsp:include page="10주차과제_includesub.jsp" />

2. 태그 param이 있는 태그 include <p> 
<jsp:include page="10주차과제_includesub.jsp" >
	<jsp:param name="programming" value="jsp" />
</jsp:include>


<br> ---------------------------------------- <br>

<%-- 
<% response.sendRedirect("10주차과제_hobbysub.jsp");%>
--%>

<br> ---------------------------------------- <br>

<%-- 
<% response.sendRedirect("10주차과제_hobbysub.jsp?hobby=golf"); %>
--%>

<br> ---------------------------------------- <br>

<%--
<jsp:forward page="10주차과제_hobbysub.jsp">
	<jsp:param name="hobby" value="golf"/>
</jsp:forward>
 --%>
 
<br> ---------------------------------------- <br>



</body>
</html>