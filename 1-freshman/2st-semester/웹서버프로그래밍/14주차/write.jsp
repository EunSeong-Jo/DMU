<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
    <title>�� �ۼ�</title>
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
            color: #555;
        }
        .form-group input[type="text"],
        .form-group textarea,
        .form-group input[type="file"] {
            width: 100%;
            padding: 8px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .form-group textarea {
            resize: vertical;
        }
        .form-actions {
            text-align: center;
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
        .navigation {
            text-align: right;
            margin-bottom: 20px;
        }
        .navigation a {
            text-decoration: none;
            color: #007bff;
            font-size: 14px;
        }
        .navigation a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
<%
    // �α��� ���� Ȯ��
    String userId = (String) session.getAttribute("user");
    if (userId == null || userId.trim().isEmpty()) {
        response.sendRedirect("member.jsp"); // �α��� �������� �����̷�Ʈ
        return;
    }
%>
<h1>�� �ۼ�</h1>

<div class="navigation">
    <a href="listboard.jsp">[�Խ��� ���]</a>
</div>

<div class="container">
    <form action="write_input.jsp" method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label for="name">�ۼ���:</label>
            <input type="text" id="name" name="name" value="<%= userId %>" readonly>
        </div>
        <div class="form-group">
            <label for="title">����:</label>
            <input type="text" id="title" name="title" required>
        </div>
        <div class="form-group">
            <label for="contents">����:</label>
            <textarea id="contents" name="contents" rows="5" required></textarea>
        </div>
        <div class="form-group">
            <label for="userFile">÷������:</label>
            <input type="file" id="userFile" name="userFile">
        </div>
        <div class="form-actions">
            <input type="submit" value="�ۼ�">
        </div>
    </form>
</div>
</body>
</html>
