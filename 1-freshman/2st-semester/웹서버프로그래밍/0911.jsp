<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>

<font size=7 color=red> 수업 </font> 중입니다.<br><br>

<%	int year = 365; %>
<%	out.println("1년은 약 몇 주일까요? <p>"); %>

<%-- 표현식 (세미콜론 없음) --%>
<%=	year / 7 %>
<%=	" 주 입니다." %><br><br>

<%	int i = 0; %>
[지역변수] i = <%= ++i %><br>

[소속변수] memi = <%= ++memi %>
<%!	int memi = 0; %>

<%! public int abs(int a){
		if(a < 0)
			return -a;
		else
			return a;
		}
	%><br><br>
	
	-3의 절대값은 <%= abs(-3) %> 이다.

<br>
<%
int a = 10;
int b = 3;

out.println(a + "+" + b + "=" + (a + b) + "<br>");
out.println(a + "-" + b + "=" + (a - b) + "<br>");
out.println(a + "*" + b + "=" + (a * b) + "<br>");
out.println(a + "/" + b + "=" + (a / b) + "<br>");
out.println(a + "/" + b + "=" + (a / (double)b) + "<br>");
%>

<br>
<%
int c = 11;
int d = 5;

out.println((c == d) + "<br>");
out.println((c < d) + "<br>");
out.println((c != d) + "<br><br>");

out.println((c > 1 && c < 5) + "<br>");
out.println((c > 1 || c < 5) + "<br>");
out.println(!(c > 1) + "<br>");
%>

<br>
<%	
int e = 123;

if (e >= 10 && e <= 150)
	out.print("10대");
%>

<br>
<%
char ch = 'A';

if (ch >= 'A' && ch <= 'Z')
	out.println((char)(ch + 32));
%>

<br>
<%	
char ch2 = 's';

if (ch2 == 'Y' || ch2 == 'y')
	out.println("yes");
else
	out.println("error");
%>

<br>
<%
char ch3 = 'n';

if(ch3 == 'Y' || ch3 == 'y')
	out.println("yes");
else if(ch3 == 'N' || ch3 =='n')
	out.println("no");
else
	out.println("error");
%>

<br>
<%	
int n = 2;

switch(n){
	case 1: out.println('1');
	case 2: out.println('2');
	case 3: out.println('3');
		break;
	case 4: out.println('4');
	
	default: out.println("error");
}
%>

<br>
<%
char ch4 = 'N';

switch(ch4){
	case 'Y':
	case 'y': out.println("yes");
		break;
		
	case 'N':
	case 'n': out.println("no");
		break;
	
	default:
		out.println("error");
	}
%>

</body>
</html>