<%@ page language="java" contentType="text/html; charset=EUC-KR"
    pageEncoding="EUC-KR"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
<title>Insert title here</title>
</head>
<body>
<%@ page import = "java.sql.*" %>
<%@page import="com.oreilly.servlet.MultipartRequest, com.oreilly.servlet.multipart.DefaultFileRenamePolicy,java.util.*, java.io.*" %>

<%
String realFolder = "";
String savePath ="C:\\Users\\asus\\eclipse-workspace\\WebServer-DBv9\\src\\main\\webapp\\db\\img\\";
//String savePath = "C:\\Users\\kim\\eclipse-workspace\\adb4\\src\\main\\webapp\\img\\";
int sizeLimit = 5 * 1024 * 1024; // 최대 업로드 파일 크기 5MB(메가)로 제한

String encType = "euc-kr";

ServletContext context = getServletContext();

String driverName = "com.mysql.jdbc.Driver";
String dbURL = "jdbc:mysql://localhost:3306/webdb";

Class.forName(driverName);
Connection conn = DriverManager.getConnection(dbURL,"root","asus");

MultipartRequest multi = null;
multi = new MultipartRequest(request, savePath, sizeLimit, encType, new DefaultFileRenamePolicy());

String userName = multi.getParameter("userName");
String fileName = multi.getFilesystemName("userFile");
String originFileName = multi.getOriginalFileName("userFile");

File file = multi.getFile("userFile");

String name   = multi.getParameter("name");  
String pass   = multi.getParameter("pass"); 
String email  = multi.getParameter("email");
String title  = multi.getParameter("title");
String contents  = multi.getParameter("contents");

Statement stmt = conn.createStatement();
	
Calendar dateIn = Calendar.getInstance();
String indate = Integer.toString(dateIn.get(Calendar.YEAR)) + "-";
indate = indate + Integer.toString(dateIn.get(Calendar.MONTH)+1) + "-";
indate = indate + Integer.toString(dateIn.get(Calendar.DATE)) + " ";
indate = indate + Integer.toString(dateIn.get(Calendar.HOUR_OF_DAY)) + ":";
indate = indate + Integer.toString(dateIn.get(Calendar.MINUTE)) + ":";
indate = indate + Integer.toString(dateIn.get(Calendar.SECOND));

String strSQL = "SELECT Max(num) FROM tblboard";
ResultSet rs = stmt.executeQuery(strSQL);
int num = 0;

if (num==0){
	rs.next();
	num = rs.getInt(1) + 1;	
}
	
strSQL ="INSERT INTO tblboard (num, name, pass, email, title, contents, writedate, readcount, filename)";
strSQL = strSQL +  "VALUES('" + num + "', '" + name + "', '" + pass + "', '" + email + "',";
strSQL = strSQL +  "'" + title + "', '" + contents + "', '" + indate + "', ' 0 ', '" + fileName + "')";
stmt.executeUpdate(strSQL);

stmt.close();                	
conn.close();

response.sendRedirect("listboard.jsp"); 
%>


</body>
</html>