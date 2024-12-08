<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%@ page import="com.oreilly.servlet.MultipartRequest, com.oreilly.servlet.multipart.DefaultFileRenamePolicy, java.sql.*, java.util.*, java.io.*" %>
<%
    try {
        // ���� ���ε带 ���� ����
        String savePath = "C:\\Users\\asus\\eclipse-workspace\\WebServer-DBv9\\src\\main\\webapp\\db\\img\\";
        String encType = "euc-kr";
        int sizeLimit = 5 * 1024 * 1024;

        // MultipartRequest�� ���� ���� ���ε� �� �Ķ���� ó��
        MultipartRequest multi = new MultipartRequest(request, savePath, sizeLimit, encType, new DefaultFileRenamePolicy());

        // MultipartRequest�κ��� �Ķ���� �б�
        String num = multi.getParameter("num");
        String title = multi.getParameter("title");
        String contents = multi.getParameter("contents");
        String fileName = multi.getFilesystemName("userFile");

        // num �� ����
        if (num == null || num.isEmpty()) {
            out.println("<script>alert('�Խñ� ��ȣ�� �����ϴ�. ��ȿ�� ��û�� �ƴմϴ�.'); history.back();</script>");
            return;
        }

        // �����ͺ��̽� ����
        Class.forName("com.mysql.jdbc.Driver");
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/webdb", "root", "asus");

        // SQL ������Ʈ ���� ����
        PreparedStatement pstmt = conn.prepareStatement(
            "UPDATE tblboard SET title = ?, contents = ?, filename = ? WHERE num = ?"
        );
        pstmt.setString(1, title);
        pstmt.setString(2, contents);
        pstmt.setString(3, fileName);
        pstmt.setInt(4, Integer.parseInt(num));

        pstmt.executeUpdate();
        pstmt.close();
        conn.close();

        // ���� �� �����̷�Ʈ
        response.sendRedirect("write_output.jsp?num=" + num);
    } catch (NumberFormatException e) {
        out.println("<script>alert('�߸��� �Խñ� ��ȣ�Դϴ�.'); history.back();</script>");
    } catch (Exception e) {
        e.printStackTrace();
        out.println("<script>alert('������ �߻��߽��ϴ�. �����ڿ��� �����ϼ���.'); history.back();</script>");
    }
%>
