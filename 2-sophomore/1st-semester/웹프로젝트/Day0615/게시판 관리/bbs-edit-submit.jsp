<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.BoardDto" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.BoardServiceImpl" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.BoardService" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // POST 데이터 한글 인코딩 처리
    request.setCharacterEncoding("utf-8");  // 📝 request 객체 (`request.setCharacterEncoding(...)`) → 한글 처리 → 시험 출제 가능

    // 사용자가 폼에서 보낸 수정된 데이터 읽기
    long boardId = Long.parseLong(request.getParameter("id"));   // 수정 대상 게시글 ID  // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String writer = request.getParameter("writer");              // 수정된 작성자  // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String subject = request.getParameter("subject");            // 수정된 제목  // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String contents = request.getParameter("contents");          // 수정된 내용  // 📝 request 객체 (`request.getParameter(...)`) → 입력값 처리 → 시험 출제 가능
    String ipAddr = request.getRemoteAddr();                     // 작성자의 IP 주소  // 📝 request 객체 (`request.getRemoteAddr()`) → IP 주소 획득 → 시험 출제 가능

    // 수정된 데이터를 기반으로 BoardDto 객체 생성
    BoardDto board = BoardDto.builder()  // 📝 DTO 빌더 패턴 시작 (`BoardDto.builder()`) → 시험 출제 가능
            .id(boardId)
            .writer(writer)
            .subject(subject)
            .contents(contents)
            .ipAddr(ipAddr)
            .build();  // 📝 DTO 빌더 완료 (`.build()`) → 시험 출제 가능

    // 서비스 객체 생성 후 게시글 수정 요청
    BoardService boardService = new BoardServiceImpl();  // 📝 서비스 객체 생성 (`new BoardServiceImpl()`) → 시험 출제 가능
    boolean result = boardService.updateBoard(board); // 수정 결과 확인  // 📝 게시글 수정 메서드 호출 (`updateBoard(...)`) → 시험 출제 가능
%>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
    <script>
        // 수정 완료 후 게시글 목록 페이지로 자동 이동
        location.href = 'bbs-list.jsp';  // 📝 자바스크립트 페이지 이동 (`location.href = ...`) → 시험 출제 가능
    </script>
</head>
<body>
</body>
</html>
