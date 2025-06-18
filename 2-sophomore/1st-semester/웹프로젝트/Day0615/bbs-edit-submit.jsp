<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.BoardDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.BoardServiceImpl" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.BoardService" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // POST 데이터 한글 인코딩 처리
    request.setCharacterEncoding("utf-8");

    // 사용자가 폼에서 보낸 수정된 데이터 읽기
    long boardId = Long.parseLong(request.getParameter("id"));   // 수정 대상 게시글 ID
    String writer = request.getParameter("writer");              // 수정된 작성자
    String subject = request.getParameter("subject");            // 수정된 제목
    String contents = request.getParameter("contents");          // 수정된 내용
    String ipAddr = request.getRemoteAddr();                     // 작성자의 IP 주소

    // 수정된 데이터를 기반으로 BoardDto 객체 생성
    BoardDto board = BoardDto.builder()
            .id(boardId)
            .writer(writer)
            .subject(subject)
            .contents(contents)
            .ipAddr(ipAddr)
            .build();

    // 서비스 객체 생성 후 게시글 수정 요청
    BoardService boardService = new BoardServiceImpl();
    boolean result = boardService.updateBoard(board); // 수정 결과 확인
%>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
    <script>
        // 수정 완료 후 게시글 목록 페이지로 자동 이동
        location.href = 'bbs-list.jsp';
    </script>
</head>
<body>
</body>
</html>
