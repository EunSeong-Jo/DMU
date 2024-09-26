<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>

<% out.print("이름 : 홍길동"); %> <br>
<% out.print("학번 : 20103056"); %>

<br> ---------------------------------------- <br>

<%! String s1 = "소속변수"; %>
<% String s1 = "지역변수"; %>
s1 = <%= s1 %> <br>
this.s1 = <%= this.s1 %>

<br> ---------------------------------------- <br>

원주율은 <%= Math.PI %> 이다.

<br> ---------------------------------------- <br>

<!-- red  -->
<%-- green--%>
결과 <%= "black" %> <br>
<%
// white
/*
out.println(“yellow”);
out.println(“pink”);
*/
out.println("blue");
%>

<br> ---------------------------------------- <br>

<%    		
	double a = 3.1;
	double b = 2.3;
	
	out.print(a+ "+" +b+ "=" +(a+b)+ "<br>");
	out.print(a+ "+" +b+ "=" +((int)a / (int)b)+ "<br>");
%>

<br> ---------------------------------------- <br>

<%
    int a1 = 10, b1 = 20;
    char op = '/';
    
    if (true) {
        out.print(a1 + " + " + b1 + " = " + (a1 + b1) + "<br>");
    }
    if (op == '/') {
        out.print(a1 + " / " + b1 + " = " + a1 / (double) b1);
    }
%>

<br> ---------------------------------------- <br>

<%    
    char ch = '@';
    
    if (ch >= 'A' && ch <= 'Z') {
        out.print((char)(ch + 32));
    }

    if (ch >= 'a' && ch <= 'z') {
        out.print((char)(ch - 32));
    }
    
    if (!((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z'))) {
        out.print("입력한 " + ch + " 영문자(대문자,소문자)가 아닌 문자");
    }
%>

 
<br> ---------------------------------------- <br>

<%    
	int a2 = 100;
	int b2 = 300;
  
	if(a2 >= 100 && b2 > 50)
		out.print("입장");
%>

<br> ---------------------------------------- <br>

<%
	int  a3 = 20, b3 = 10;

	out.print(a3 + "<br>"); 
	out.print(++a3 + "<br>");
	out.print(a3 + "<br>"); 
	out.print(a3++ + "<br>"); 
	out.print(a3 + "<br>"); 

	out.print(b3 + "<br>");
	out.print(--b3 + "<br>");
	out.print(b3 + "<br>"); 
%>

</body>
</html>