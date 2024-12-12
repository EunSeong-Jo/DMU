<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%@ page import = "java.sql.*" %>
<!DOCTYPE html>
<html>
<head>
    <title>�Խñ� ����</title>
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
    // num �Ķ���� ����
    String num = request.getParameter("num");
    if (num == null || num.isEmpty()) {
        out.println("<script>alert('��ȿ���� ���� �Խñ� ��ȣ�Դϴ�.'); history.back();</script>");
        return;
    }

    try {
        // �����ͺ��̽� ���� ����
        String driverName = "com.mysql.jdbc.Driver";
        String dbURL = "jdbc:mysql://localhost:3306/webdb";

        Class.forName(driverName);
        Connection conn = DriverManager.getConnection(dbURL, "root", "asus");

        // �Խñ� ��ȸ
        PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM tblboard WHERE num = ?");
        pstmt.setInt(1, Integer.parseInt(num));
        ResultSet rs = pstmt.executeQuery();

        if (!rs.next()) {
            out.println("<script>alert('�ش� �Խñ��� ã�� �� �����ϴ�.'); history.back();</script>");
            rs.close();
            pstmt.close();
            conn.close();
            return;
        }

        // �Խñ� ������ ��������
        String title = rs.getString("title");
        String contents = rs.getString("contents");
        String filename = rs.getString("filename");

        rs.close();
        pstmt.close();
        conn.close();
%>
<h1>�Խñ� ����</h1>
<div class="container">
    <form action="modify_process.jsp" method="post" enctype="multipart/form-data">
        <input type="hidden" name="num" value="<%= num %>">
        <div class="form-group">
            <label for="title">����</label>
            <input type="text" id="title" name="title" value="<%= title %>">
        </div>
        <div class="form-group">
            <label for="contents">����</label>
            <textarea id="contents" name="contents"><%= contents %></textarea>
        </div>
        <div class="form-group">
            <label>���� ����</label>
            <p><%= filename != null ? filename : "÷�� ���� ����" %></p>
        </div>
        <div class="form-group">
            <label for="userFile">���� ����</label>
            <input type="file" id="userFile" name="userFile">
        </div>
        <div class="form-actions">
            <input type="submit" value="����">
        </div>
    </form>
</div>
<%
    } catch (Exception e) {
        e.printStackTrace();
        out.println("<script>alert('������ �߻��߽��ϴ�. �����ڿ��� �����ϼ���.'); history.back();</script>");
    }
%>
</body>
</html>
