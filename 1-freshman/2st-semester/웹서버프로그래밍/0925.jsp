<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page info = 'page' %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>

<%-- 평균이 90점 이상 100점 이하면 A, 80점이상 90점 미만이면 B, 
70점이상 80점 미만이면 C, 60점 이상 70점 미만이면 D, 60점 미만이면 F학점 처리 --%>

<%
int kor = 90;
int eng = 95;
int mat = 90;
int sum, avg;

sum = kor + eng + mat;
avg = sum / 3;

if (100 >= avg && avg >= 90)
	out.println("A");
else if (90 > avg && avg >= 80)
	out.println("B");
else if (80 > avg && avg >= 70)
	out.println("C");
else if (70 > avg && avg >= 60)
	out.println("D");
else
	out.println('F');

out.println("<br><br>");

switch ((int)(avg / 10)){
	case 10:
		out.println("평균 : " + avg + ", 학점 : A+");
		break;
	case 9:
		out.println("평균 : " + avg + ", 학점 : A");
		break;
	case 8:
		out.println("평균 : " + avg + ", 학점 : B");
		break;
	case 7:
		out.println("평균 : " + avg + ", 학점 : C");
		break;
	case 6:
		out.println("평균 : " + avg + ", 학점 : D");
		break;
		
	default:
		out.println("평균 : " + avg + ", 학점 : F");
}
%>

<br><br>

<%
int sum2 = 0;

for(int i = 1; i <= 5; i = i + 2){
	sum2 += i;
}
%>
<%=sum2 %>

<br><br>

<%
int esum = 0, osum = 0;
int i;

for(i = 1; i <= 5; i++){
	if(i % 2 == 0)
		esum = esum + i;
	else
		osum = osum + i;
}

out.println("1부터" + (i-1) + "까지 짝수합" + esum + "<br>");
out.println("1부터" + (i-1) + "까지 홀수합" + osum + "<br>");
%>

<br><br>

<%
int gu = 7;
int i2 = 1;

while(i2 <= 9){
	out.println(gu + "*" + i2 + "=" + (gu * i2) + "<br>");
	i2++;
}
%>

<br><br>

<%
int gu2 = 3;
int i3 = 1;

do{
	out.print(gu2 + "*" + i3 + "=" + (gu2 * i3) + "<br>");
	i3 = i3 + 1;
}
while(i3 <= 9);
%>

<br><br>

<%
int i4, j;

for(j = 1; j < 3; j++){
	out.println(j);
}
%>

<br><br>

<%
int i5, j2;
int sum3;

for(i5 = 10; i5 <= 100; i5 = i5 + 10){
	sum3 = 0;
	for(j2 = 1; j2 <= i5; j2++){
		sum3 = sum3 + j2;
	}
	out.println("1..." + i5 + "=" + sum3 + "<br>");
}

out.println("<br><br>");

for(i5 = 10; i5 <= 100; i5 = i5 + 10){
	sum3 = 0;
	for(j2 = i5 - 9; j2 <= i5; j2++){
		sum3 = sum3 + j2;
	}
	out.println((i5 - 9) + "..." + i5 + "=" + sum3 + "<br>");
}
%>

<br><br>

<%@ page import = "java.util.Date" %>
현재 시각 : <%= new Date().toLocaleString() %>

<br><br>

<%@ page errorPage = 'error.jsp' %>
<%
String str[] = {
		"감사합니다.", "Thank you."
	};
%>

한국어로 [<%= str[0] %>]는 영어로 [<%= str[1] %>]이다.

</body>
</html>