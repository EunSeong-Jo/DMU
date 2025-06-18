<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.MemberDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.MemberService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.MemberServiceImpl" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // POST 방식으로 전송된 한글 데이터 처리
    request.setCharacterEncoding("utf-8");

    // 회원 등록 폼에서 전달된 값 받기
    String userId = request.getParameter("user_id");
    String userName = request.getParameter("user_name");
    String password = request.getParameter("password");

    // 전달받은 데이터를 기반으로 DTO 생성
    MemberDto member = MemberDto.builder()
            .userId(userId)
            .userName(userName)
            .password(password)
            .build();

    // 회원 등록 서비스 실행
    MemberService memberService = new MemberServiceImpl();
    boolean result = memberService.addMember(member); // DB에 insert
%>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
    <script>
        // 회원 등록 성공 후 목록 페이지로 자동 이동
        location.href = 'member-list.jsp';
    </script>
</head>
<body>
<!-- 공통 메뉴 삽입 -->
<jsp:include page="include_menu.jsp"/>
</body>
</html>
