<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>여기에 브라우저 제목이 출력됨</title>
</head>
<body>

<%-- 
<hr><font color=blue>
1 년은 <%=  (5)    .  (6)    ("weeks") %>주 입니다.
</font><hr> --%>

<hr><font color=blue>
1 년은 <%=request.getParameter("weeks") %>주 입니다.
</font><hr>

</body>
</html>