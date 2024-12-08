<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%@ page import="com.oreilly.servlet.MultipartRequest, com.oreilly.servlet.multipart.DefaultFileRenamePolicy, java.sql.*, java.util.*, java.io.*" %>
<%
    try {
        // 파일 업로드를 위한 설정
        String savePath = "C:\\Users\\asus\\eclipse-workspace\\WebServer-DBv9\\src\\main\\webapp\\db\\img\\";
        String encType = "euc-kr";
        int sizeLimit = 5 * 1024 * 1024;

        // MultipartRequest를 통해 파일 업로드 및 파라미터 처리
        MultipartRequest multi = new MultipartRequest(request, savePath, sizeLimit, encType, new DefaultFileRenamePolicy());

        // MultipartRequest로부터 파라미터 읽기
        String num = multi.getParameter("num");
        String title = multi.getParameter("title");
        String contents = multi.getParameter("contents");
        String fileName = multi.getFilesystemName("userFile");

        // num 값 검증
        if (num == null || num.isEmpty()) {
            out.println("<script>alert('게시글 번호가 없습니다. 유효한 요청이 아닙니다.'); history.back();</script>");
            return;
        }

        // 데이터베이스 연결
        Class.forName("com.mysql.jdbc.Driver");
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/webdb", "root", "asus");

        // SQL 업데이트 쿼리 실행
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

        // 성공 후 리다이렉트
        response.sendRedirect("write_output.jsp?num=" + num);
    } catch (NumberFormatException e) {
        out.println("<script>alert('잘못된 게시글 번호입니다.'); history.back();</script>");
    } catch (Exception e) {
        e.printStackTrace();
        out.println("<script>alert('오류가 발생했습니다. 관리자에게 문의하세요.'); history.back();</script>");
    }
%>
