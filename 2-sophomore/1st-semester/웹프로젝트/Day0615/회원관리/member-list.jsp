<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.MemberDto" %>
<%@ page import="java.util.List" %>
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
<jsp:include page="include_menu.jsp"/>

<!-- 제목 -->
<h1>회원 목록</h1>

<!-- 회원 목록 테이블 -->
<table border="1">
    <thead>
    <tr>
        <th>NO</th>
        <th>ID</th>
        <th>이름</th>
        <th>비밀번호</th>
        <th>등록일자</th>
        <th>수정일자</th>
        <th>비고</th>
    </tr>
    </thead>
    <tbody>

    <%
        // 서비스 객체를 통해 회원 목록 조회
        // 📝 서비스 객체 생성 (`new MemberServiceImpl()`) → 시험 출제 가능
        MemberService memberService = new MemberServiceImpl();

        // 📝 회원 목록 조회 메서드 호출 (`getMemberList()`) → 시험 출제 가능
        List<MemberDto> memberList = memberService.getMemberList();

        // 출력 순서를 위해 총 개수 저장
        int totalCount = memberList.size();
        int i = 0;

        // 회원 목록 반복 출력
        // 📝 향상된 for문 (`for (MemberDto member : memberList)`) → 시험 출제 가능
        for (MemberDto member : memberList) {
    %>
    <tr>
        <!-- 번호: 최신 회원이 위로 오도록 역순 출력 -->
        <td><%= totalCount - i++ %></td>

        <!-- 회원 ID (수정 페이지 링크로 연결) -->
        <td>
            // 📝 수정 링크에 회원 ID를 파라미터로 전달 (`member-edit.jsp?user_id=...`) → 시험 출제 가능
            <a href="member-edit.jsp?user_id=<%= member.getUserId() %>">
                <%= member.getUserId() %>
            </a>
        </td>

        <!-- 이름 출력 -->
        <td><%= member.getUserName() %></td>

        <!-- 비밀번호 출력 (보안상 실제 서비스에서는 마스킹 처리 필요) -->
        <td><%= member.getPassword() %></td>

        <!-- 등록일자 -->
        <td><%= member.getCreateDt() %></td>

        <!-- 수정일자 (널일 경우 빈 문자열 출력) -->
        <td><%= member.getUpdateDt() != null ? member.getUpdateDt() : "" %></td>

        <!-- 삭제 버튼: 클릭 시 confirm 창 띄운 후 삭제 페이지로 이동 -->
        <td>
            // 📝 삭제 버튼에 회원 ID를 파라미터로 전달 (`member-delete.jsp?user_id=...`) → 시험 출제 가능
            <button
                    onclick="return confirm('삭제하시겠습니까?') ? location.href =
                            'member-delete.jsp?user_id=<%=member.getUserId()%>' : false;" type="button">
            삭제
            </button>
        </td>
    </tr>
    <%
        } // end for
    %>

    </tbody>
</table>

</body>
</html>
