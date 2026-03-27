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
	//request.setCharacterEncoding("euc-kr");
	String userid = request.getParameter("userid");
	String passwd = request.getParameter("passwd");
%>
<%
	if(userid.equals("")){
%>
	<jsp:include page="Loginhandle.jsp">
		<jsp:param name = "userid" value="guest"/>
		<jsp:param name = "passwd" value="anonymous"/>
	</jsp:include>
<%
	}
	else{
%>
	<jsp:include page="Loginhandle.jsp"/>
<% 
	}
%>

</body>
</html>