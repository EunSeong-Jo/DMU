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
<% request.setCharacterEncoding("euc-kr"); %>

<%
String id = request.getParameter("id");
String pass = request.getParameter("pass"); 
String name = request.getParameter("name");
String phone = request.getParameter("phone");
String email = request.getParameter("email");

String check_ok = "yes";

if (id == "")
	check_ok = "no";

if (pass == "")
	check_ok = "no";

if (name == "")
	check_ok = "no";


String driverName = "com.mysql.jdbc.Driver";
String dbURL = "jdbc:mysql://localhost:3306/webdb";

Class.forName(driverName);
Connection conn = DriverManager.getConnection(dbURL,"root","asus");

Statement stmt = conn.createStatement();

String strSQL = "SELECT id FROM tbllogin2 where id='" + id + "'";
ResultSet rs = stmt.executeQuery(strSQL);

if (!rs.next())
	check_ok="yes";
else
	check_ok="no";

if (check_ok == "yes"){
	strSQL = "INSERT INTO tbllogin2(id,pass,name,phone,email)";
	strSQL = strSQL +  "VALUES('" + id + "', '" + pass + "', '" + name + "',  '" + phone + "', '" + email + "')";
	stmt.executeUpdate(strSQL);
%>

<BODY>
<center><font size='3'><b> 회원 가입 성공 </b></font>  

<TABLE border='0' width='600' cellpadding='0' cellspacing='0'>
	<TR>
		<TD><hr size='1' noshade>
		</TD>
 	</TR>
</TABLE>

<TABLE cellSpacing='0' cellPadding='10' align='center' border='0'>
<TR>
	<TD align='center'>
		<font size='2'>회원 가입을 축하합니다.<BR>로그인 하세요.</font>
	</TD>
</TR>

<TR>
	<TD align='center'>
		<font size='2'><a href="member.jsp">[로그인]</a></font>
	</TD>
</TR>
</TABLE>

</BODY>
</HTML>

<%
} else {
%>

<HTML>
<HEAD>

<TITLE> 회원 가입 실패 </TITLE> 

</HEAD>
<BODY>
<center><font size='3'><b> 회원 가입 실패 </b></font>

<TABLE border='0' width='600' cellpadding='0' cellspacing='0'>
	<TR>
		<TD><hr size='1' noshade>
		</TD>
 	</TR>
</TABLE>

<TABLE cellSpacing='0' cellPadding='10' align='center' border='0'>
<TR>
	<TD align='center'>
		<font size='2'>회원 가입에 실패 했습니다. <BR>다시 가입서를 작성해 주세요.</font>
	</TD>
</TR>

<TR>
	<TD align='center'>
		<font size='2'><a href="member_input.jsp">[가입서 작성]</a></font>
	</TD>
</TR>
</TABLE>

</BODY>
</HTML>
<%
}
stmt.close();
conn.close();
%>