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

</body>
</html>