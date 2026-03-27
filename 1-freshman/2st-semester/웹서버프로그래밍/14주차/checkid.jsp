<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%@ page import="java.sql.*" %>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
    <title>ID 중복 확인</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 400px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            font-size: 18px;
            color: #333;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        table td {
            padding: 15px;
            text-align: center;
            font-size: 14px;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
        }
        table td.bg-gray {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        a {
            display: inline-block;
            text-decoration: none;
            padding: 8px 12px;
            font-size: 14px;
            color: #fff;
            background-color: #007bff;
            border-radius: 4px;
            margin-top: 10px;
        }
        a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ID 중복 확인</h1>
        <form>
            <table>
                <%
                String id = request.getParameter("id");
                if (id == null || id.trim().isEmpty()) {
                %>
                <tr>
                    <td class="bg-gray">ID를 입력하세요.</td>
                </tr>
                <tr>
                    <td><a href="javascript:close()">닫기</a></td>
                </tr>
                <%
                } else {
                    String driverName = "com.mysql.jdbc.Driver";
                    String dbURL = "jdbc:mysql://localhost:3306/webdb";

                    Class.forName(driverName);
                    Connection conn = DriverManager.getConnection(dbURL, "root", "asus");

                    Statement stmt = conn.createStatement();
                    String strSQL = "SELECT id FROM tbllogin2 WHERE id='" + id + "'";
                    ResultSet rs = stmt.executeQuery(strSQL);

                    if (!rs.next()) {
                %>
                <tr>
                    <td class="bg-gray">ID: <%= id %><br>사용할 수 있는 아이디입니다.</td>
                </tr>
                <tr>
                    <td><a href="javascript:close()">닫기</a></td>
                </tr>
                <%
                    } else {
                %>
                <tr>
                    <td class="bg-gray">ID: <%= id %><br>사용할 수 없는 아이디입니다.</td>
                </tr>
                <tr>
                    <td><a href="javascript:close()">닫기</a></td>
                </tr>
                <%
                    }
                    rs.close();
                    stmt.close();
                    conn.close();
                }
                %>
            </table>
        </form>
    </div>
</body>
</html>
