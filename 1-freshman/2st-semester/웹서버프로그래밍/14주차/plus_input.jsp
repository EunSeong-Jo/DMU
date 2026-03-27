<%@ page language="java" contentType="text/html; charset=EUC-KR"
    pageEncoding="EUC-KR"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
<title>Insert title here</title>
</head>
<body>
<%@ page import = "java.sql.*, java.util.*" %>
<% request.setCharacterEncoding("euc-kr"); %>

<%
String num = request.getParameter("num");
String name = request.getParameter("plus_name");  
String contents = request.getParameter("plus_contents");
int num_plus = 0;

String driverName = "com.mysql.jdbc.Driver";
String dbURL = "jdbc:mysql://localhost:3306/webdb";

Class.forName(driverName);
Connection conn = DriverManager.getConnection(dbURL,"root","asus");

Statement stmt = conn.createStatement();

String strSQL = "SELECT num FROM tblboardplus ORDER BY num DESC";
ResultSet rs = stmt.executeQuery(strSQL);

if(num==null)  
	num_plus = 1;
else {
    	strSQL = "SELECT Max(num) FROM tblboardplus";
    	rs = stmt.executeQuery(strSQL);
    	rs.next();
    	num_plus = rs.getInt(1) + 1;
}

Calendar dateIn = Calendar.getInstance();
String indate = Integer.toString(dateIn.get(Calendar.YEAR)) + "-";
indate = indate + Integer.toString(dateIn.get(Calendar.MONTH)+1) + "-";
indate = indate + Integer.toString(dateIn.get(Calendar.DATE)) + " ";
indate = indate + Integer.toString(dateIn.get(Calendar.HOUR_OF_DAY)) + ":";
indate = indate + Integer.toString(dateIn.get(Calendar.MINUTE)) + ":";
indate = indate + Integer.toString(dateIn.get(Calendar.SECOND));

strSQL ="INSERT INTO tblboardplus (num, id, name, contents, writedate)";
strSQL = strSQL +  "VALUES('" + num_plus + "', '" + num + "', '" + name + "',";
strSQL = strSQL +  "'" + contents + "', '" + indate + "')";
stmt.executeUpdate(strSQL);

stmt.close();
conn.close();

response.sendRedirect("write_output.jsp?num=" + num); 
%>


</body>
</html>