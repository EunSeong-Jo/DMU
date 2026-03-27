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
// application객체 생성 : setAttribute()
// application객체 이름의 값삭제 : removeAttribute()
// application객체 반환: getAttribute()

application.setAttribute("job", "programmer");
application.setAttribute("taste", "독서");
%>
직업 : <%=application.getAttribute("job") %><br>
취미 : <%=application.getAttribute("taste") %><br>

<%
application.removeAttribute("job");
%> 

직업 : <%=application.getAttribute("job") %><br>
취미 : <%=application.getAttribute("taste") %><br>

<br> ---------------------------------------- <br>

<%-- !전역변수 (최초 시작시 값 초기화) --%>
<%! int count = 0; %>
<%
	String scount = (String) application.getAttribute("count");
	if (scount != null){
		count = Integer.parseInt(scount);
	}
	else {
		count = 0;
	}
	
	application.setAttribute("count" , Integer.toString(++count));
	application.log("count : " + count);
%>

조회 수 : <%=count %>

<br> ---------------------------------------- <br>

<%@ page import = "java.util.Enumeration" %>

<h1>세션 예제</h1><hr>

<h2>세션 만들기</h2>

<%
session.setAttribute("id", "아이디");
session.setAttribute("pwd", "비밀번호");
%>

<hr><h2>세션 조회</h2>

세션 id : <%=session.getId() %><br>
<%-- 세션 유지시간 <% session.setMaxInactiveInterval(3); %><br> --%>
<%-- 세션 삭제 <% session.removeAttribute("id"); %><br> --%>

<%
Enumeration<String> e = session.getAttributeNames();

while (e.hasMoreElements()){
	String name = e.nextElement();
	String value = (String) session.getAttribute(name);
	out.println("세션 name : " + name + ",,, ");
	out.println("세션 value : " + value + "<br>");
}
%>
<br>
세션 invalidate : <% session.invalidate(); %>

<br> ---------------------------------------- <br>

<%
	Cookie cookie1 = new Cookie("user", "kang");
	cookie1.setMaxAge(2 * 60);
	response.addCookie(cookie1);
%>
<hr><a href=addtimecookie.jsp>시간을 쿠키에 저장</a>

</body>
</html>