<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html lang="ko">
<head>
    <title>Title</title>
</head>
<body>
<%
    String userId = request.getParameter("userId");
    String userPw = request.getParameter("userPassword");

    boolean isLogin = false;

    if ("a".equals(userId) && "1".equals(userPw)){
        isLogin = true;
    }
%>



<% if (!isLogin){ %>

<script>
    alert("로그인 정보 없음");
    location.href = 'exam01.jsp';
</script>

<% } else {%>

<script>
    alert("<%=userId%> 로그인 완료");
</script>

<% } %>


<h1>POST!</h1>

</body>
</html>
