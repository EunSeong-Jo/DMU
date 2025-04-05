<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>nine X nine</title>
</head>
<body>

    <%
        boolean isLogin = false;

        if (!isLogin){
            response.sendRedirect("login.jsp");
        }
    %>

    <h1><%= "구구단" %></h1><br>

    <%
        String dan = request.getParameter("dan");
        // int danval = dan != null ? Integer.parseInt(dan) : 0;
        int danVal = 0;

        try {
            danVal = Integer.parseInt(dan);
        } catch (NumberFormatException e){
            System.out.print("null값이 입력됨");
        }
    %>

    <form action="ninenine.jsp" method="GET">
        <select name="dan">
            <option>선택</option>

            <% for (int i = 2; i <= 9; i++){ %>

            <option value="<%= i %>" <%= i == danVal ? "selected" : "" %>>
                <%= i %>
            </option>

            <% } %>
        </select>

        <button type="submit">이동</button>
    </form>

    <hr>

    <%
        if (danVal != 0) {
            for (int i = 1; i <= 9; i++){%>
            <p><%="%d * %d = %d".formatted(danVal, i, danVal * i)%></p>
        <%}%>
    <%}%>

</body>
</html>