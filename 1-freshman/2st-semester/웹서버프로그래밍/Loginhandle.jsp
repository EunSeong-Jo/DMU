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
	if(userid.equals("guest")){
		out.println("회원이 아닙니다.<br>");
		out.println("다음으로 로그인.<br>");
	}
	else{
		out.println("회원입니다.<hr>");
	}
%>

아이디 : <%=userid %>,
암호 : <%=passwd %>

</body>
</html>