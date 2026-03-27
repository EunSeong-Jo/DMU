<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%@ page import = "java.sql.*" %>
<!DOCTYPE html>
<html>
<head>
    <title>게시글 삭제</title>
</head>
<body>
<%
    String num = request.getParameter("num");
    String driverName = "com.mysql.jdbc.Driver";
    String dbURL = "jdbc:mysql://localhost:3306/webdb";

    Class.forName(driverName);
    Connection conn = DriverManager.getConnection(dbURL, "root", "asus");

    PreparedStatement pstmt = conn.prepareStatement("DELETE FROM tblboard WHERE num = ?");
    pstmt.setInt(1, Integer.parseInt(num));
    pstmt.executeUpdate();

    pstmt.close();
    conn.close();

    response.sendRedirect("listboard.jsp");
%>
</body>
</html>
