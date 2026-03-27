<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<%
/*
String[] strMember = new String[3];

strMember[0] = new String("김김김");
strMember[1] = new String("이이이");
strMember[2] = new String("임임임");

out.println(strMember[0] + "<br>");
out.println(strMember[1] + "<br>");
out.println(strMember[2] + "<br>");
*/
String[] strMember = {"김김김", "이이이", "임임임"};

/*
for(int i = 0; i < strMember.length; i++)
	out.println(strMember[i] + "<br>");
*/

// for each문
for(String n : strMember)
	out.println(n + "<br>");

%>

<br><br>

<%
int num[] = {10, 20, 30};
for(int n : num){
	out.println(n + "<br>");
};
%>

<br> ---------------------------------------- <br>

<%
request.setCharacterEncoding("euc-kr");
%>

<%
String name = request.getParameter("name");
String addr = request.getParameter("addr");
String tel = request.getParameter("tel");
%>

<h2>학생 정보 입력 결과</h2>
성명 : <%= name %> <br>
주소 : <%= addr %> <br>
연락처 : <%= tel %> <br>

<br> ---------------------------------------- <br>

<%
String id = request.getParameter("strID");
String pass = request.getParameter("strPwd");

out.println("아이디 : " + id + "<br>");
out.println("비밀번호 : " + pass + "<br>");
%>

<br> ---------------------------------------- <br>

<%
String name = request.getParameter("name");
String tym = request.getParameter("studentNum");
String sex = request.getParameter("mw");
String country = request.getParameter("country");

if(sex.equalsIgnoreCase("man")){
	sex = "남자";
}
else{
	sex = "여자";
}
%>

<h2>학생 정보 입력 결과</h2>
성명 : <%= name %> <br>
학번 : <%= tym %> <br>
성별 : <%= sex %> <br>
국가 : <%= country %>

<br> ---------------------------------------- <br>

<%
String name = request.getParameter("name");
String color = request.getParameter("color");

if(color.equalsIgnoreCase("etc")){
	out.println(color);
	color = "gray";
}
%>
<body bgcolor = <%= color %>>

</body>
</html>