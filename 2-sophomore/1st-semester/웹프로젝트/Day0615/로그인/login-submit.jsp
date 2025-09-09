<%@ page import="kr.ac.dongyang.website.jspwebsite.service.LoginService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.MemberDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.DbLoginServiceImpl" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
</head>
<body>
<%
    // 📝 서비스 객체 생성 (`new DbLoginServiceImpl()`) → 시험 출제 가능
    LoginService loginService = new DbLoginServiceImpl();

    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String userId = request.getParameter("user_id");
    String password = request.getParameter("password");

    // 📝 로그인 서비스 메서드 호출 (`login(...)`) → 시험 출제 가능
    MemberDto member = loginService.login(userId, password);
    boolean loginResult = member != null;
%>

<%if (loginResult) {%>
<%
    // 📝 session 객체 (`session.setAttribute(...)`) → 로그인 정보 저장 → 시험 출제 가능
    session.setAttribute("userId", userId);

    // 📝 session 객체 (`session.setAttribute(...)`) → 사용자 이름 저장 → 시험 출제 가능
    session.setAttribute("userName", member.getUserName());

    // 📝 response 객체 (`response.sendRedirect(...)`) → 메인으로 이동 → 시험 출제 가능
    response.sendRedirect("/");
%>
<%} else {%>
<script>
    alert('로그인에 실패했습니다.');
    history.back(-1);
</script>
<%}%>
</body>
</html>
