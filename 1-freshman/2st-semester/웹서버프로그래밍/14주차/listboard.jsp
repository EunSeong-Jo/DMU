<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
    <title>앨범 게시판</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .top-bar {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-bottom: 20px;
        }
        .top-bar a {
            display: inline-block;
            padding: 8px 12px;
            background-color: #007bff;
            color: #fff;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            margin-left: 10px;
        }
        .top-bar a:hover {
            background-color: #0056b3;
        }
        .board {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            border-spacing: 10px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
        }
        .board-item {
            text-align: center;
            vertical-align: top;
            width: 100%;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        .board-item img {
            width: 160px;
            height: 160px;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 10px;
        }
        .board-item-title {
            font-size: 16px;
            font-weight: bold;
            color: #555;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        .board-item-date {
            font-size: 12px;
            color: #888;
        }
        .pagination {
            text-align: center;
            margin-top: 20px;
        }
        .pagination a {
            margin: 0 5px;
            text-decoration: none;
            color: #007bff;
        }
        .pagination a:hover {
            text-decoration: underline;
        }
        .pagination span {
            margin: 0 5px;
            font-weight: bold;
        }
    </style>
</head>
<body>
<%
    // 로그인 여부 확인
    String userId = (String) session.getAttribute("user");
    if (userId == null || userId.trim().isEmpty()) {
        response.sendRedirect("member.jsp"); // 로그인 페이지로 리다이렉트
        return;
    }
%>

<h1>앨범 게시판</h1>

<div class="top-bar">
    <a href="write.jsp">글 작성</a>
    <a href="logout.jsp">로그아웃</a>
</div>

<%@ page import = "java.sql.*" %>
<%
    request.setCharacterEncoding("euc-kr");
    String pageNum = request.getParameter("pageNum");
    if (pageNum == null) {
        pageNum = "1";
    }

    int listSize = 3; // 한 페이지당 표시할 게시글 수 (3개 고정)
    int currentPage = Integer.parseInt(pageNum);
    int startRow = (currentPage - 1) * listSize;
    int totalPosts = 0;

    String driverName = "com.mysql.jdbc.Driver";
    String dbURL = "jdbc:mysql://localhost:3306/webdb";
    Class.forName(driverName);
    Connection conn = DriverManager.getConnection(dbURL, "root", "asus");
    Statement stmt = conn.createStatement();

    // 게시글 총 개수 가져오기
    String countSQL = "SELECT COUNT(*) FROM tblboard";
    ResultSet rs = stmt.executeQuery(countSQL);
    if (rs.next()) {
        totalPosts = rs.getInt(1);
    }
    rs.close();

    // 게시글 데이터 가져오기
    String listSQL = "SELECT * FROM tblboard ORDER BY num DESC LIMIT " + startRow + ", " + listSize;
    rs = stmt.executeQuery(listSQL);
%>

<!-- 게시글 목록 출력 -->
<div class="board">
<%
    boolean hasPosts = totalPosts > 0;

    if (hasPosts) {
        while (rs.next()) {
            int listnum = rs.getInt("num");
            String title = rs.getString("title");
            String writedate = rs.getString("writedate");
            String filename = rs.getString("filename");
%>
    <div class="board-item">
        <a href="write_output.jsp?num=<%= listnum %>">
            <img src="<%="C:\\Users\\asus\\eclipse-workspace\\WebServer-DBv9\\src\\main\\webapp\\db\\img\\" + filename %>" alt="이미지 없음">
        </a>
        <div class="board-item-title"><%= title %></div>
        <div class="board-item-date"><%= writedate %></div>
    </div>
<%
        }
    } else {
%>
    <div class="board-item">게시글이 없습니다.</div>
<%
    }
    rs.close();
    stmt.close();
    conn.close();
%>
</div>

<!-- 페이지 네비게이션 -->
<div class="pagination">
<%
    if (totalPosts > 0) {
        int totalPages = (totalPosts % listSize == 0) ? totalPosts / listSize : totalPosts / listSize + 1;
        int blockSize = 5; // 한번에 표시할 페이지 번호 수
        int currentBlock = (currentPage - 1) / blockSize; // 현재 블록 계산
        int startPage = currentBlock * blockSize + 1; // 블록 시작 페이지
        int endPage = Math.min(startPage + blockSize - 1, totalPages); // 블록 끝 페이지

        // 이전 블록으로 이동
        if (currentBlock > 0) {
%>
<a href="listboard.jsp?pageNum=<%= startPage - 1 %>">[이전]</a>
<%
        }

        // 페이지 번호 출력
        for (int i = startPage; i <= endPage; i++) {
            if (i == currentPage) {
%>
<span>[<%= i %>]</span>
<%
            } else {
%>
<a href="listboard.jsp?pageNum=<%= i %>">[<%= i %>]</a>
<%
            }
        }

        // 다음 블록으로 이동
        if (endPage < totalPages) {
%>
<a href="listboard.jsp?pageNum=<%= endPage + 1 %>">[다음]</a>
<%
        }
    }
%>
</div>

</body>
</html>
