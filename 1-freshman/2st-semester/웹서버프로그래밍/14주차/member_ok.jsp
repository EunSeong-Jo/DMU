<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
    <title>회원 인증</title>
</head>
<body>
    <center><font size='3'><b>회원 인증</b></font></center>
    <hr>
    <table align="center" border="0" cellpadding="30">
        <%@ page import = "java.sql.*" %>
        <%
        String id = request.getParameter("id");
        String pass = request.getParameter("pass");

        if (id == null || id.trim().isEmpty() || pass == null || pass.trim().isEmpty()) {
        %>
        <tr>
            <td align="center">
                <font size="2">ID와 비밀번호를 입력하세요.</font>
            </td>
        </tr>
        <tr>
            <td align="center">
                <a href="member.jsp">[로그인]</a>
            </td>
        </tr>
        <%
        } else {
            try {
                String driverName = "com.mysql.jdbc.Driver";
                String dbURL = "jdbc:mysql://localhost:3306/webdb";

                Class.forName(driverName);
                Connection conn = DriverManager.getConnection(dbURL, "root", "asus");

                String strSQL = "SELECT id, pass FROM tbllogin2 WHERE id = ?";
                PreparedStatement pstmt = conn.prepareStatement(strSQL);
                pstmt.setString(1, id);
                ResultSet rs = pstmt.executeQuery();

                if (!rs.next()) {
        %>
        <tr>
            <td align="center">
                <font size="2">회원 ID가 아닙니다.</font>
            </td>
        </tr>
        <tr>
            <td align="center">
                <a href="member.jsp">[로그인]</a>
            </td>
        </tr>
        <%
                } else {
                    String logid = rs.getString("id");
                    String logpass = rs.getString("pass");

                    if (!pass.equals(logpass)) {
        %>
        <tr>
            <td align="center">
                <font size="2">비밀번호가 일치하지 않습니다.</font>
            </td>
        </tr>
        <tr>
            <td align="center">
                <a href="member.jsp">[로그인]</a>
            </td>
        </tr>
        <%
                    } else {
                        // 로그인 성공: 세션에 사용자 ID 저장
                        session.setAttribute("user", logid);
                        response.sendRedirect("listboard.jsp"); // 게시판 화면으로 이동
                    }
                }
                rs.close();
                pstmt.close();
                conn.close();
            } catch (Exception e) {
                e.printStackTrace();
        %>
        <tr>
            <td align="center">
                <font size="2">오류가 발생했습니다. 관리자에게 문의하세요.</font>
            </td>
        </tr>
        <%
            }
        }
        %>
    </table>
</body>
</html>
