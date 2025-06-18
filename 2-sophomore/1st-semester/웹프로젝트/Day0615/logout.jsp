<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
</head>
<body>

<%
    // 현재 사용자 세션을 무효화 (로그아웃 처리)
    session.invalidate();

    // 메인 페이지(index.jsp 또는 /)로 리디렉션
    response.sendRedirect("/");
%>

</body>
</html>
