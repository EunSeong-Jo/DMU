<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%@ page import = "java.sql.*" %>
<!DOCTYPE html>
<html>
<head>
    <title>게시글 수정</title>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
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
            margin-bottom: 20px;
        }
        .container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 14px;
        }
        .form-group input[type="text"],
        .form-group textarea,
        .form-group input[type="file"] {
            width: 100%;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .form-group textarea {
            resize: vertical;
            height: 150px;
        }
        .form-actions {
            text-align: right;
        }
        .form-actions input[type="submit"] {
            padding: 10px 20px;
            font-size: 14px;
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .form-actions input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
<%
    // num 파라미터 검증
    String num = request.getParameter("num");
    if (num == null || num.isEmpty()) {
        out.println("<script>alert('유효하지 않은 게시글 번호입니다.'); history.back();</script>");
        return;
    }

    try {
        // 데이터베이스 연결 설정
        String driverName = "com.mysql.jdbc.Driver";
        String dbURL = "jdbc:mysql://localhost:3306/webdb";

        Class.forName(driverName);
        Connection conn = DriverManager.getConnection(dbURL, "root", "asus");

        // 게시글 조회
        PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM tblboard WHERE num = ?");
        pstmt.setInt(1, Integer.parseInt(num));
        ResultSet rs = pstmt.executeQuery();

        if (!rs.next()) {
            out.println("<script>alert('해당 게시글을 찾을 수 없습니다.'); history.back();</script>");
            rs.close();
            pstmt.close();
            conn.close();
            return;
        }

        // 게시글 데이터 가져오기
        String title = rs.getString("title");
        String contents = rs.getString("contents");
        String filename = rs.getString("filename");

        rs.close();
        pstmt.close();
        conn.close();
%>
<h1>게시글 수정</h1>
<div class="container">
    <form action="modify_process.jsp" method="post" enctype="multipart/form-data">
        <input type="hidden" name="num" value="<%= num %>">
        <div class="form-group">
            <label for="title">제목</label>
            <input type="text" id="title" name="title" value="<%= title %>">
        </div>
        <div class="form-group">
            <label for="contents">내용</label>
            <textarea id="contents" name="contents"><%= contents %></textarea>
        </div>
        <div class="form-group">
            <label>현재 파일</label>
            <p><%= filename != null ? filename : "첨부 파일 없음" %></p>
        </div>
        <div class="form-group">
            <label for="userFile">파일 변경</label>
            <input type="file" id="userFile" name="userFile">
        </div>
        <div class="form-actions">
            <input type="submit" value="수정">
        </div>
    </form>
</div>
<%
    } catch (Exception e) {
        e.printStackTrace();
        out.println("<script>alert('오류가 발생했습니다. 관리자에게 문의하세요.'); history.back();</script>");
    }
%>
</body>
</html>
