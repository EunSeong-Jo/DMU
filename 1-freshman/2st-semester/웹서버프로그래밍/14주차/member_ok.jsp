<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
    <title>ȸ�� ����</title>
</head>
<body>
    <center><font size='3'><b>ȸ�� ����</b></font></center>
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
                <font size="2">ID�� ��й�ȣ�� �Է��ϼ���.</font>
            </td>
        </tr>
        <tr>
            <td align="center">
                <a href="member.jsp">[�α���]</a>
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
                <font size="2">ȸ�� ID�� �ƴմϴ�.</font>
            </td>
        </tr>
        <tr>
            <td align="center">
                <a href="member.jsp">[�α���]</a>
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
                <font size="2">��й�ȣ�� ��ġ���� �ʽ��ϴ�.</font>
            </td>
        </tr>
        <tr>
            <td align="center">
                <a href="member.jsp">[�α���]</a>
            </td>
        </tr>
        <%
                    } else {
                        // �α��� ����: ���ǿ� ����� ID ����
                        session.setAttribute("user", logid);
                        response.sendRedirect("listboard.jsp"); // �Խ��� ȭ������ �̵�
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
                <font size="2">������ �߻��߽��ϴ�. �����ڿ��� �����ϼ���.</font>
            </td>
        </tr>
        <%
            }
        }
        %>
    </table>
</body>
</html>
