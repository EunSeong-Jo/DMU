<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.MemberDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.MemberService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.MemberServiceImpl" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // POST 방식으로 전송된 한글 데이터를 올바르게 처리
    request.setCharacterEncoding("utf-8");

    // 폼에서 전달된 수정 대상 회원 정보 가져오기
    String userId = request.getParameter("user_id");
    String userName = request.getParameter("user_name");
    String password = request.getParameter("password");

    // 전달받은 정보로 MemberDto 객체 생성
    MemberDto member = MemberDto.builder()
            .userId(userId)
            .userName(userName)
            .password(password)
            .build();

    // 회원 정보 수정 수행
    MemberService memberService = new MemberServiceImpl();
    boolean result = memberService.updateMember(member); // DB update
%>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>

    <!-- 수정 완료 후 목록 페이지로 이동 -->
    <script>
        location.href = 'member-list.jsp';
    </script>
</head>
<body>
</body>
</html>
