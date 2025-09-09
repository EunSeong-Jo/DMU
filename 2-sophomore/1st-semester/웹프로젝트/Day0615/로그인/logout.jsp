<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
</head>
<body>
<%
    // 📝 session 객체 (`session.invalidate()`) → 로그아웃 처리 → 시험 출제 가능
    session.invalidate();

    // 📝 response 객체 (`response.sendRedirect(...)`) → 메인으로 이동 → 시험 출제 가능
    response.sendRedirect("/");
%>
</body>
</html>
