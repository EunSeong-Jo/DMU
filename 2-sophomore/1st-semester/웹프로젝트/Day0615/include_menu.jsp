<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // 세션에서 로그인 상태 확인
    boolean isLogin = session.getAttribute("userId") != null;

    // 로그인된 사용자의 이름 가져오기
    String userName = (String) session.getAttribute("userName");
%>

<div>
    <% if (isLogin) { %>
    <!-- 로그인된 경우, 우측 상단에 사용자 이름 표시 -->
    <p style="text-align: right"><%= userName %>님 환영합니다.</p>
    <% } %>

    <hr/>

    <!-- 공통 메뉴 리스트 -->
    <ul class="menu">

        <!-- 대시보드 메뉴 -->
        <li>
            <h2>대시보드</h2>
            <a href="/">대시보드</a>
        </li>

        <!-- 회원 관리 메뉴 -->
        <li>
            <h2>회원 관리</h2>
            <a href="/member-list.jsp">회원 목록</a>
            |
            <a href="/member-add.jsp">회원 추가</a>
        </li>

        <!-- 게시판 관리 메뉴 -->
        <li>
            <h2>게시판 관리</h2>
            <a href="/bbs-list.jsp">게시글 목록</a>
            |
            <a href="/bbs-add.jsp">게시글 추가</a>
        </li>

        <!-- 로그인 상태에 따라 로그인/로그아웃 링크 표시 -->
        <li>
            <% if (isLogin) { %>
            <a href="/logout.jsp">로그아웃</a>
            <% } else { %>
            <a href="/login.jsp">로그인</a>
            <% } %>
        </li>
    </ul>

    <hr/>
</div>
