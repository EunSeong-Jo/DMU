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
String name = "aaa";
%>

<%@ include file="Top.jsp" %><br>

include 지시자의 Body 부분 <br>

<%@ include file="Bottom.jsp" %>

<br> ---------------------------------------- <br>

<h2>include 액션 태그</h2>
sub.jsp 파일 red 부분.<br>
<jsp:include page="Sub.jsp"/>
main 파일 부분.

<br> ---------------------------------------- <br>

<% int i = 12; %>
<% int days = 365; %>
1년은 <%= i %>달 입니다.

<!-- 중복선언 조심 -->
<!-- 파일을 가져옴 -->
<%@ include file = "Includesub.jsp" %>
1년은 <%=days %>일 입니다.

<br> ---------------------------------------- <br>

<% //int nm = 365; %>
1년은 <%= i %>달 입니다.

<!-- 결과만 출력 -->
<jsp:include page="Includesub.jsp"/>
1년은 <%=nm %>일 입니다.

<br> ---------------------------------------- <br>

<h2>forward 액션태그</h2>
Forwardsub.jsp 파일 시작 부분입니다.<br>

<%-- <jsp:forward page="Forwardsub.jsp"/>  --%>

Forwardsub.jsp 파일 끝 부분. 제어권 넘어감.

<br> ---------------------------------------- <br>

<h2>로그인 </h2>

<form method="post" action="Login.jsp">
아이디 : <input type="text" name="userid"><br>
암호 : <input type="text" name="passwd"><p>
<input type="submit" value="로그인">
<input type="reset" value="다시입력">
</form>

</body>
</html>