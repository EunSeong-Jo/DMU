<%@ page import="java.time.LocalDateTime" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" trimDirectiveWhitespaces="true" %>

<!doctype html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<%
    LocalDateTime now = LocalDateTime.now();
%>

<h1>JSP 문서</h1>
<h2>학번 : 20232678, 이름 : 조은성</h2>
<p>현재 시간 : <%=now%> </p>

</body>
</html>