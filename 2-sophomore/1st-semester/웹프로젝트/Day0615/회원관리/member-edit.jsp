<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.MemberDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.MemberService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.MemberServiceImpl" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
</head>
<body>

<!-- 공통 메뉴 삽입 -->
<jsp:include page="../include_menu.jsp"/>

<h1>회원 수정</h1>

<%
    // URL 파라미터에서 수정 대상 회원 ID 추출
    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String userId = request.getParameter("user_id");

    // 회원 서비스 객체를 통해 회원 정보 조회
    // 📝 서비스 객체 생성 (`new MemberServiceImpl()`) → 시험 출제 가능
    MemberService memberService = new MemberServiceImpl();

    // 📝 단건 조회 메서드 호출 (`getMember(...)`) → 시험 출제 가능
    MemberDto member = memberService.getMember(userId);
%>

// 📝 조건문 비교 (`==`) → 시험 출제 가능
<% if (member == null) { %>
<!-- 회원이 존재하지 않을 경우 -->
<script>
    alert('회원 정보가 존재하지 않습니다.');
    history.back(-1); // 이전 페이지로 이동
</script>
<% } else { %>

<!-- 회원 정보가 존재하면 수정 폼 표시 -->
<div class="member-add">
    <form action="/member-edit-submit.jsp" method="post">

        <!-- 이름 입력 필드 -->
        <div>
            <label for="userName">이름</label>

            // 📝 input 태그 name 속성 → request.getParameter(...)에서 사용됨 → 시험 출제 가능
            <input type="text" id="userName" name="user_name" value="<%=member.getUserName()%>" required/>

        </div>

        <!-- 아이디는 수정 불가(readonly) -->
        <div>
            <label for="userId">아이디</label>

            // 📝 input 태그 name 속성 → request.getParameter(...)에서 사용됨 → 시험 출제 가능
            <input type="text" id="userId" name="user_id" value="<%=member.getUserId()%>" readonly required/>

        </div>

        <!-- 비밀번호 수정 가능 -->
        <div>
            <label for="password">비밀번호</label>

            // 📝 input 태그 name 속성 → request.getParameter(...)에서 사용됨 → 시험 출제 가능
            <input type="password" id="password" name="password" value="<%=member.getPassword()%>" required/>

        </div>

        <!-- 가입일자 표시는 수정 불가 -->
        <div>
            <label for="password">가입일</label>
            <%=member.getCreateDt()%>
        </div>

        <!-- 제출 버튼 -->
        <div>
            <button type="submit">회원 수정</button>
        </div>
    </form>
</div>
<% } %>

</body>
</html>
