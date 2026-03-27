<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>

<h1>GET!</h1>

<%
    String methodName = request.getMethod();
    String ip = request.getRemoteAddr();
%>

<ul>
    <li>
        데이터 전송 방식 : <%= methodName %>
    </li>
    <li>
        클라이언트 ip : <%= ip %>
    </li>
</ul>

</body>
</html>
