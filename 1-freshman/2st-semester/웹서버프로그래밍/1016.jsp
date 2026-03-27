<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<!-- jsp 인코딩이 html 인코딩과 다르면 인코딩 오류(글자깨짐) 발생 -->
<% // request.setCharacterEncoding("euc-kr"); %>

<%
String studentNum = request.getParameter("studentNum");
String[] majors = request.getParameterValues("major");
%>

<h2>학생 정보 입력 결과</h2>
학번 : <%= studentNum %><p>

<%
if (majors == null){
	out.println("전공 없음");
}
else {
	for (String eachmajor : majors)
		out.println(eachmajor + " ");
	// for (int i = 0; i < majors.length; i++)
		// out.println(majors[i] + " ");
}
%>

<br> ---------------------------------------- <br>

<h2>취미와 가보고 싶은 국가 결과</h2>

<%
String[] hobby = request.getParameterValues("hobby");
String country = request.getParameter("country");

out.println("나라 : " + country + "<br>");

if(country != null){
	for(String eachdata : hobby){
		out.println(eachdata + " ");
	}
}
%>

<br> ---------------------------------------- <br>

<%@ page import="java.util.Enumeration" %>
<h2>취미와 가보고 싶은 국가 결과 - Enumeration</h2>

<%
Enumeration<String> e = request.getParameterNames();

while(e.hasMoreElements()){
	String element = e.nextElement();
	String[] data = request.getParameterValues(element);
	
	if(data != null){
		for(String eachdata : data)
			out.println(eachdata + " ");
	}
	out.println("<p>");
}
%>

<br> ---------------------------------------- <br>

<h2>기술정보 이력서</h2>
이름 : <%= request.getParameter("name") %> <br>
주민번호 : <%= request.getParameter("jnum1") %> - <%= request.getParameter("jnum2") %> <br>
학력 : <%= request.getParameter("graduate") %> <br>
전공 : <%= request.getParameter("major2") %> <br>
경험 플랫폼 : <%
	for(String platform : request.getParameterValues("platform")){
		out.println("[" + platform + "]");
}
%>

</body>
</html>