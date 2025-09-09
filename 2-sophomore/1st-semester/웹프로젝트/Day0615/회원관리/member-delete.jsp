<%@ page import="kr.ac.dongyang.website.jspwebsite.dao.MemberDao" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.MemberService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.MemberServiceImpl" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // POST/GET 방식 한글 인코딩 처리
    request.setCharacterEncoding("utf-8");

    // 삭제할 회원의 ID 값을 파라미터로 전달받음
    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String userId = request.getParameter("user_id");

    // 회원 서비스 객체 생성
    // 📝 서비스 객체 생성 (`new MemberServiceImpl()`) → 시험 출제 가능
    MemberService memberService = new MemberServiceImpl();

    // 삭제 요청 수행
    // 📝 회원 삭제 메서드 호출 (`deleteMember(...)`) → 시험 출제 가능
    boolean result = memberService.deleteMember(userId);
%>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>

    <!-- 삭제 처리 후 목록 페이지로 이동 -->
    <script>
        location.href = 'member-list.jsp';
    </script>

</head>
<body>
</body>
</html>
