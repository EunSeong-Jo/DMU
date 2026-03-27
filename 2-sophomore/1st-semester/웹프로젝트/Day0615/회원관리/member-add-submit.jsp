<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.MemberDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.MemberService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.MemberServiceImpl" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%
    request.setCharacterEncoding("utf-8");

    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String userId = request.getParameter("user_id");

    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리
    String userName = request.getParameter("user_name");

    String password = request.getParameter("password");

    // 📝 DTO 빌더 패턴 시작 (`MemberDto.builder()`) → 시험 출제 가능
    MemberDto member = MemberDto.builder()
            .userId(userId)
            .userName(userName)
            .password(password)

            // 📝 DTO 빌더 완료 (`.build()`) → 시험 출제 가능
            .build();

    // 📝 서비스 객체 생성 (`new MemberServiceImpl()`) → 시험 출제 가능
    MemberService memberService = new MemberServiceImpl();

    // 📝 회원 추가 메서드 호출 (`addMember(...)`) → 시험 출제 가능
    boolean result = memberService.addMember(member);
%>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
    <script>
        location.href = 'member-list.jsp';
    </script>
</head>
<body>
<jsp:include page="../include_menu.jsp"/>
</body>
</html>
