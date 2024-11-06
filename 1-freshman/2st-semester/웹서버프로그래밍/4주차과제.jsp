<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<% int i, j, sum = 0, a = 1; %>
<% 
	for (i=2; i<10; i++) {
		for (j=1; j<10; j++) {
			out.print("[" + i + "*" + j + " = " + i*j + "] ");
		}			
		out.print("<br>");
	}
%>

<br> ---------------------------------------- <br>

<% 
for (i = 0; 100 >= i; i++){
	sum += i;
	}
%>

1부터 100까지의 합은 <%= sum %>이다.

<br> ---------------------------------------- <br>

<%
for(i=10; 100 >= i; i += 10){
	sum = 0;
	for(j=1; i >= j; j++){
		sum = sum + j;
	}
	out.println("1..." + i + "=" + sum + "<br>");
}
%>

<br> ---------------------------------------- <br>

<%
for(i = 10; 100 >= i; i += 10){
	sum = 0;
	for(j = (i-9); i >= j; j++){
		sum = sum + j;	
	}
	out.println((i-9) + "..." + i + "=" + sum + "<br>");
}
%>

<br> ---------------------------------------- <br>

<%! int num[] = {10,20,30,40,50}; %>
<% 
sum = 0;

for (i = 0; num.length > i; i++){
	sum += num[i];
}

out.println("<br><br>배열의 합 : " + sum);
%>

<br> ---------------------------------------- <br>

<%
char ch3='n';

if (ch3 == 'Y' | ch3 == 'y')
	out.println("yes");
else if(ch3 == 'N' | ch3 == 'n')
	out.println("no");
else
	out.println("error");
%>

<br> ---------------------------------------- <br>

<%
char ch4='N';

switch (ch4){
	case 'Y':   
	case 'y':
		out.println("yes");
		break;
	case 'N':  
	case 'n':
		out.println("no");
		break;
	default:
		out.println("error");	
}
%>

<br> ---------------------------------------- <br>

<%        
sum = 0;

for(i = 2 ; i <= 5; i += 2){
	sum = sum+ i;
	}
%>
<%= sum %>

<br> ---------------------------------------- <br>

<%
int esum = 0, osum = 0;

for(i = 1; i <= 5; i++){
	if(i % 2 == 0)
		esum += i;
	else
		osum = osum + i;
	}
%> <br>

짝수의 합 : <%=esum %><br>
홀수의 합 : <%=osum %><br>

</body>
</html>