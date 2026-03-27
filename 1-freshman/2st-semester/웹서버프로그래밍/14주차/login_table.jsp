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
		String driverName = "com.mysql.jdbc.Driver";
		String dbURL = "jdbc:mysql://localhost:3306/webdb";
		String user = "root";
	    String pwd = "asus";
		Connection con = null;
		Statement stmt = null ;
	  
		String sql = "create table tbllogin2( ";
		 sql = sql+ "id varchar(20), ";
	     sql = sql+ "name varchar(20), ";
	     sql = sql+ "pass varchar(20), ";
	     sql = sql+ "phone varchar(20), ";
	     sql = sql+ "email varchar(30)) ";
		try{  	
			Class.forName(driverName);
			con = DriverManager.getConnection(dbURL, user, pwd); 
			stmt= con.createStatement();
			stmt.executeUpdate(sql) ;
			out.print("데이터베이스 연결 성공!");
		}
		catch(Exception e){
			out.print("데이터베이스 연결 실패!"+e);
		}
		finally{
			try{
				if(con != null) con.close();
				if(stmt != null) stmt.close();
			}
			catch(Exception e){ 
	  			out.println( e.getMessage());
			}
		}
		%>



</body>
</html>