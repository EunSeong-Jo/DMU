<%@ page import="java.util.List" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.BoardService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.BoardServiceImpl" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.BoardDto" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
    <script>
        // 2초마다 자동 새로고침 (테스트용 또는 실시간 반영용)
        setTimeout(function () {
            location.reload();
        }, 2000);
    </script>
</head>
<body>

<!-- 공통 메뉴 삽입 -->
<jsp:include page="include_menu.jsp"/>

<h1>게시글 목록</h1>

<table border="1">
    <thead>
    <tr>
        <th>NO</th>
        <th>제목</th>
        <th>작성자</th>
        <th>IP</th>
        <th>등록일자</th>
        <th>수정일자</th>
        <th>비고</th>
    </tr>
    </thead>
    <tbody>

    <%
        // 게시글 목록을 가져오는 서비스 객체 생성
        BoardService boardService = new BoardServiceImpl();
        List<BoardDto> boardList = boardService.getBoardList(); // DB에서 게시글 목록 조회

        int totalCount = boardList.size(); // 전체 글 수
        int i = 0;

        // 게시글 리스트 반복 출력
        for (BoardDto board : boardList) {
    %>
    <tr>
        <!-- 글 번호 (최신글이 위로 오도록 역순 출력) -->
        <td><%= totalCount - i++ %></td>

        <!-- 제목: 클릭하면 수정 페이지로 이동 -->
        <td>
            <a href="bbs-edit.jsp?id=<%=board.getId()%>">
                <%= board.getSubject() %>
            </a>
        </td>

        <!-- 작성자 출력 -->
        <td><%= board.getWriter() %></td>

        <!-- 작성자 IP 주소 출력 -->
        <td><%= board.getIpAddr() %></td>

        <!-- 작성일자 출력 -->
        <td><%= board.getCreateDt() %></td>

        <!-- 수정일자 출력 (null인 경우 빈 문자열) -->
        <td><%= board.getUpdateDt() != null ? board.getUpdateDt() : "" %></td>

        <!-- 삭제 버튼: 클릭 시 확인창 띄우고, 확인 누르면 삭제 페이지로 이동 -->
        <td>
            <button
                    onclick="return confirm('삭제하시겠습니까?') ? location.href='board-delete.jsp?id=<%=board.getId()%>' : false;"
                    type="button">
                삭제
            </button>
        </td>
    </tr>
    <%
        } // for문 끝
    %>

    </tbody>
</table>

</body>
</html>
