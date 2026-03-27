<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.MemberDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.MemberService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.MemberServiceImpl" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // POST 방식으로 전송된 한글 데이터를 올바르게 처리
    request.setCharacterEncoding("utf-8");

    // 폼에서 전달된 수정 대상 회원 정보 가져오기
    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String userId = request.getParameter("user_id");

    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String userName = request.getParameter("user_name");

    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String password = request.getParameter("password");

    // 전달받은 정보로 MemberDto 객체 생성
    // 📝 DTO 빌더 패턴 시작 (`MemberDto.builder()`) → 시험 출제 가능
    MemberDto member = MemberDto.builder()
            .userId(userId)
            .userName(userName)
            .password(password)
            // 📝 DTO 빌더 완료 (`.build()`) → 시험 출제 가능
            .build();

    // 회원 정보 수정 수행
    // 📝 서비스 객체 생성 (`new MemberServiceImpl()`) → 시험 출제 가능
    MemberService memberService = new MemberServiceImpl();

    // 📝 회원 수정 메서드 호출 (`updateMember(...)`) → 시험 출제 가능
    boolean result = memberService.updateMember(member);
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
