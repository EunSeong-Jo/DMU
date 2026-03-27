<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.BoardDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.BoardServiceImpl" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.BoardService" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // 폼 데이터 인코딩 설정 (한글 깨짐 방지)
    // 📝 request 객체 (`request.setCharacterEncoding(...)`) → 한글 처리 → 시험 출제 가능
    request.setCharacterEncoding("utf-8");

    // 폼에서 전송된 값 읽기
    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String writer = request.getParameter("writer");

    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String subject = request.getParameter("subject");

    // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String contents = request.getParameter("contents");

    // 클라이언트의 IP 주소 가져오기
    // 📝 request 객체 (`request.getRemoteAddr()`) → IP 주소 획득 → 시험 출제 가능
    String ipAddr = request.getRemoteAddr();

    // 입력값을 기반으로 게시글 객체 생성
    // 📝 DTO 빌더 패턴 시작 (`BoardDto.builder()`) → 시험 출제 가능
    BoardDto board = BoardDto.builder()
            .writer(writer)
            .subject(subject)
            .contents(contents)
            .ipAddr(ipAddr)
            .build();  // 📝 DTO 빌더 완료 (`.build()`) → 시험 출제 가능

    // 서비스 객체를 생성해 DB에 게시글 추가 요청
    // 📝 서비스 객체 생성 (`new BoardServiceImpl()`) → 시험 출제 가능
    BoardService boardService = new BoardServiceImpl();

    // DB 저장 결과
    // 📝 게시글 추가 메서드 호출 (`addBoard(...)`) → 시험 출제 가능
    boolean result = boardService.addBoard(board);
%>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
    <script>
        // 저장이 완료되면 게시글 목록 화면으로 이동
        // 📝 자바스크립트 페이지 이동 (`location.href = ...`) → 시험 출제 가능
        location.href = 'bbs-list.jsp';
    </script>
</head>
<body>
</body>
</html>
