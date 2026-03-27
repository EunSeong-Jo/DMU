<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<%-- 
<%@ page import = "java.net.URLEncoder" %>
<%@ page import = "java.net.URLDecoder" %>

<%
Cookie cookie1 = new Cookie("Name","kim");
Cookie cookie2 = new Cookie("Job", "student");
response.addCookie(cookie1);
response.addCookie(cookie2);
%>

<%
Cookie[] cs = request.getCookies();

if (cs != null) {
	for (Cookie cook : cs) {
	out.println(cook.getValue() + "<br>");
	}
}
%>
--%>

<br> ---------------------------------------- <br>

<%
Cookie C = new Cookie("lang", "java"); 

response.addCookie(C);

Cookie[] cs = request.getCookies();

for (int i = 0; i < cs.length; ++i){
	out.println("쿠키의 이름 : " + cs[i].getName());
	out.println("쿠키의 값 : " + cs[i].getValue());
}

for (Cookie each_cs : cs){
	out.println("쿠키의 이름 : " + each_cs.getName());
	out.println("쿠키의 값 : " + each_cs.getValue());
}

// session.invalidate();

session.setAttribute("id", "apple");

session.removeAttribute("id");

session.getAttribute("id");
%>

<br> ---------------------------------------- <br>

<%! int application = 0; %>	
<%! int count = 0; %>	

<%	
	String scount = (String) application.getAttribute("count");
	
	if (scount != null) {
		count = Integer.parseInt(scount);
	} else {
		count = 0;
	}
		
	application.setAttribute("count", Integer.toString(++count));
	application.log("현재까지 조회 수 : " + count);
%>
	서버 컨테이너 정보 : <%=application.getServerInfo() %> <p>
	현재까지 조회 수 : <%=count %>

</body>
</html>