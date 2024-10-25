<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<!-- request : 클라이언트 >> 서버 , response : 서버 >> 클라이언트 -->

<h2>요청 정보</h2>
요청 방식 : <%= request.getMethod() + "<br>"%>
요청 URL : <%= request.getRequestURL() + "<br>"%>
요청 URI : <%= request.getRequestURI() + "<br>"%>
클라이언트 주소 : <%= request.getRemoteAddr() + "<br>"%>
클라이언트 호스트 : <%= request.getRemoteHost() + "<br>"%>
프로토콜 방식 : <%= request.getProtocol() + "<br>"%>
서버 이름 : <%= request.getServerName() + "<br>"%>
서버 포트 번호 : <%= request.getServerPort() %>

<br> ---------------------------------------- <br>

<%
/*
String strSite = request.getParameter("download");

switch(Integer.parseInt(strSite)){
	case 1:
		response.sendRedirect("https://www.daum.net");
		break;
	case 2:
		response.sendRedirect("https://www.naver.com");
		break;
	case 3:
		response.sendRedirect("https://www.google.com");
		break;
	default:
		response.sendRedirect("https://www.yahoo.com");
}
*/
%>

<br> ---------------------------------------- <br>

<%
/*
String URL = "https://search.naver.com/search.naver?where=nexearch";
String keyword = request.getParameter("word");
URL = URL + "&" + "query=" + keyword;

response.sendRedirect(URL);
*/%>

<br> ---------------------------------------- <br>

<%
/*
out.println("출력 X");
out.clear();
*/
%>

<!-- 
<h2>현재 페이지 버퍼 상태</h2>
<p>초기 출력 버퍼 크기 : <%= out.getBufferSize() %> byte
<p>남은 출력 버퍼 크기 : <%= out.getRemaining() %> byte
<p>autoFlush : <%= out.isAutoFlush() %> 
-->

<br> ---------------------------------------- <br>

<%
// request.setCharacterEncoding("euc-kr");

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