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
    // 로그인 처리용 서비스 객체 생성 (DB 기반 구현체)
    LoginService loginService = new DbLoginServiceImpl();

    // 로그인 폼에서 전달된 사용자 입력값 읽기
    String userId = request.getParameter("user_id");
    String password = request.getParameter("password");

    // 로그인 검증 요청 (MemberDto 객체가 반환되면 성공)
    MemberDto member = loginService.login(userId, password);
    boolean loginResult = member != null;
%>

<% if (loginResult) { %>
<%
    // 로그인 성공 시, 세션에 로그인 정보 저장
    session.setAttribute("userId", userId);                      // 로그인 ID
    session.setAttribute("userName", member.getUserName());     // 사용자 이름

    // 메인 페이지(index.jsp 또는 '/')로 이동
    response.sendRedirect("/");
%>
<% } else { %>
<!-- 로그인 실패 시, 경고 메시지 출력 후 이전 페이지로 이동 -->
<script>
    alert('로그인에 실패했습니다.');
    history.back(-1); // 뒤로 가기
</script>
<% } %>

</body>
</html>
