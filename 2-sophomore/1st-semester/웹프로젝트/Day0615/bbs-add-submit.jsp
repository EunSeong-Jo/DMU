<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.BoardDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.BoardServiceImpl" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.BoardService" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // 폼 데이터 인코딩 설정 (한글 깨짐 방지)
    request.setCharacterEncoding("utf-8");

    // 폼에서 전송된 값 읽기
    String writer = request.getParameter("writer");
    String subject = request.getParameter("subject");
    String contents = request.getParameter("contents");
    String ipAddr = request.getRemoteAddr(); // 클라이언트의 IP 주소 가져오기

    // 입력값을 기반으로 게시글 객체 생성
    BoardDto board = BoardDto.builder()
            .writer(writer)
            .subject(subject)
            .contents(contents)
            .ipAddr(ipAddr)
            .build();

    // 서비스 객체를 생성해 DB에 게시글 추가 요청
    BoardService boardService = new BoardServiceImpl();
    boolean result = boardService.addBoard(board); // DB 저장 결과
%>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
    <script>
        // 저장이 완료되면 게시글 목록 화면으로 이동
        location.href = 'bbs-list.jsp';
    </script>
</head>
<body>
</body>
</html>
