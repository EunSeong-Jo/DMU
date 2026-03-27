<%@ page import="kr.ac.dongyang.website.jspwebsite.service.BoardService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.BoardServiceImpl" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.BoardDto" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <!-- 외부 CSS 적용 -->
    <link rel="stylesheet" href="/main.css"/>
</head>
<body>

<!-- 상단 메뉴 삽입 -->
<jsp:include page="../include_menu.jsp"/>

<%
    // 게시글 ID를 URL 파라미터에서 받아옴 (예: ?id=5)
    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 받기 → 시험 출제 가능
    long boardId = Long.parseLong(request.getParameter("id"));

    // 게시글 조회를 위한 서비스 객체 생성
    // 📝 서비스 객체 생성 (`new BoardServiceImpl()`) → 시험 출제 가능
    BoardService boardService = new BoardServiceImpl();

    // ID에 해당하는 게시글 조회
    // 📝 게시글 단건 조회 메서드 호출 (`getBoard(...)`) → 시험 출제 가능
    BoardDto board = boardService.getBoard(boardId);
%>

// 📝 게시글이 존재하지 않을 경우 예외 처리 → 시험 출제 가능
<% if (board == null) { %>
<!-- 해당 ID의 게시글이 없을 경우 알림 표시 후 이전 페이지로 이동 -->
<script>
    alert('회원 정보가 존재하지 않습니다.');
    history.back(-1);
</script>
<% } else { %>

<h1>게시글 수정</h1>

<div class="member-add">
    <!-- 게시글 수정 폼: 기존 값들을 미리 채워둠 -->
    // 📝 수정 처리 페이지 지정 (`action="bbs-edit-submit.jsp"`) → 시험 출제 가능
    <form action="/게시판%20관리/bbs-edit-submit.jspubmit.jsp" method="post">
        <!-- 게시글 ID는 숨겨진 값으로 함께 보냄 -->
        <input type="hidden" name="id" value="<%=board.getId()%>"/>

        <!-- 작성자 입력란 -->
        <div>
            <label for="writer">작성자</label>
            <input type="text" id="writer" name="writer" value="<%=board.getWriter()%>" required/>
        </div>

        <!-- 제목 입력란 -->
        <div>
            <label for="subject">제목</label>

            // 📝 input의 value로 기존 데이터 출력 (`value="<%=...%>"`) → 시험 출제 가능
            <input type="text" id="subject" name="subject" value="<%=board.getSubject()%>" required/>
        </div>

        <!-- 내용 입력란 -->
        <div>
            <label for="contents">내용</label>

            // 📝 textarea 안에 기존 내용 출력 (`<%=...%>`) → 시험 출제 가능
            <textarea id="contents" name="contents" cols="60" rows="10"><%=board.getContents()%></textarea>
        </div>

        <!-- 수정 버튼 -->
        <div>
            <button type="submit">게시글 수정</button>
        </div>
    </form>
</div>

<% } %>

</body>
</html>
