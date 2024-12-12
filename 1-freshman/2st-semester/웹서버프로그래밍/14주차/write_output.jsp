<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%@ page import="java.sql.*, java.util.*" %>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
    <title>�Խñ� ����</title>
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
        .info {
            font-size: 14px;
            color: #555;
            margin-bottom: 20px;
        }
        .info .details {
            display: flex;
            justify-content: space-between;
        }
        .content {
            margin-bottom: 20px;
        }
        .content img {
            width: 100%;
            max-width: 400px;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 20px;
        }
        .buttons {
            display: flex;
            justify-content: flex-end;
            margin-top: 20px;
        }
        .buttons a {
            text-decoration: none;
            padding: 8px 12px;
            background-color: #007bff;
            color: #fff;
            border-radius: 4px;
            font-size: 14px;
            margin-left: 10px; /* ���� �߰� */
        }
        .buttons a:first-child {
            margin-left: 0; /* ù ��° ��ư�� ���� ���� */
        }
        .buttons a:hover {
            background-color: #0056b3;
        }
        .comments {
            margin-top: 30px;
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
        .form-group textarea {
            width: 100%;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .form-group textarea {
            resize: vertical;
        }
        .form-actions {
            text-align: right; /* ��� ��� ��ư ������ ���� */
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
        .comment-list {
            margin-top: 20px;
        }
        .comment-item {
            background-color: #f5f5f5;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .comment-item b {
            color: #333;
        }
        .comment-item .date {
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
<%
    // �����ͺ��̽� ���� �� �Խñ� ��������
    String driverName = "com.mysql.jdbc.Driver";
    String dbURL = "jdbc:mysql://localhost:3306/webdb";
    Class.forName(driverName);
    Connection conn = DriverManager.getConnection(dbURL, "root", "asus");

    String num = request.getParameter("num");
    PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM tblboard WHERE num = ?");
    pstmt.setInt(1, Integer.parseInt(num));
    ResultSet rs = pstmt.executeQuery();
    rs.next();

    String name = rs.getString("name");
    String title = rs.getString("title");
    String contents = rs.getString("contents").trim();
    String writedate = rs.getString("writedate");
    int readcount = rs.getInt("readcount");
    String filename = rs.getString("filename");
%>

<h1>�Խñ� ����</h1>

<div class="container">
    <!-- �Խñ� ���� -->
    <div class="info">
        <div class="details">
            <span>�ۼ���: <%= name %></span>
            <span>�ۼ���: <%= writedate %>, ��ȸ��: <%= readcount %></span>
        </div>
        <div>���� �̸�: <%= filename != null ? filename : "����" %></div>
    </div>

    <!-- �Խñ� ���� -->
    <div class="content">
        <h2><%= title %></h2>
        <% if (filename != null && !filename.isEmpty()) { %>
        <img src="<%="C:\\Users\\asus\\eclipse-workspace\\WebServer-DBv9\\src\\main\\webapp\\db\\img\\" + filename %>" alt="�̹��� ����">
        <% } %>
        <p><%= contents %></p>
    </div>

    <!-- ����, ���� ��ư -->
    <div class="buttons">
        <a href="modify.jsp?num=<%= num %>">�����ϱ�</a>
        <a href="delete.jsp?num=<%= num %>">�����ϱ�</a>
    </div>
</div>

<!-- ��� ���� -->
<div class="container comments">
    <h3>���</h3>
    <form class="comment-form" action="plus_input.jsp" method="post">
        <input type="hidden" name="num" value="<%= num %>">
        <div class="form-group">
            <label for="plus_name">�ۼ���</label>
            <input type="text" id="plus_name" name="plus_name" placeholder="�ۼ���">
        </div>
        <div class="form-group">
            <label for="plus_contents">���</label>
            <textarea id="plus_contents" name="plus_contents" placeholder="����� �Է��ϼ���" rows="3"></textarea>
        </div>
        <div class="form-actions">
            <input type="submit" value="��� ���">
        </div>
    </form>

    <div class="comment-list">
        <% 
        Statement stmt = conn.createStatement();
        ResultSet commentRs = stmt.executeQuery("SELECT * FROM tblboardplus WHERE id = " + num);
        while (commentRs.next()) { 
        %>
        <div class="comment-item">
            <b><%= commentRs.getString("name") %>:</b> <%= commentRs.getString("contents") %>
            <div class="date">(<%= commentRs.getString("writedate") %>)</div>
        </div>
        <% 
        } 
        commentRs.close();
        stmt.close();
        %>
    </div>
</div>

<%
    // ��ȸ�� ���� ó��
    pstmt = conn.prepareStatement("UPDATE tblboard SET readcount = readcount + 1 WHERE num = ?");
    pstmt.setInt(1, Integer.parseInt(num));
    pstmt.executeUpdate();

    rs.close();
    pstmt.close();
    conn.close();
%>

</body>
</html>
