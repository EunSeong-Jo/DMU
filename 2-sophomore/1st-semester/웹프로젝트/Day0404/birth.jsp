<%@ page import="kr.ac.dongyang.webproject.day0404.HtmlUtils" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>brith</title>
</head>
<body>

    <h1><%= "생년월일" %></h1><br>

    <%= HtmlUtils.selectBox(1900, 2025, "year")%>
    <%= HtmlUtils.selectBox(1, 12, "month")%>
    <%= HtmlUtils.selectBox(1, 31, "day")%>

    <%
        String[] items = {"a", "b", "c"};
    %>
    <%= HtmlUtils.itemList(items)%>

<%--    <select name="year">--%>
<%--        <option>년</option>--%>
<%--        <% for (int i = 1900; i <= 2025; i++){ %>--%>
<%--        <option value="<%= i %>">--%>
<%--            <%= i %>--%>
<%--        </option>--%>
<%--        <% } %>--%>
<%--    </select>--%>

<%--        <select name="month">--%>
<%--            <option>월</option>--%>
<%--            <% for (int i = 1; i <= 12; i++){ %>--%>
<%--            <option value="<%= i %>">--%>
<%--                <%= i %>--%>
<%--            </option>--%>
<%--            <% } %>--%>
<%--        </select>--%>

<%--        <select name="day">--%>
<%--            <option>일</option>--%>
<%--            <% for (int i = 1; i <= 31; i++){ %>--%>
<%--            <option value="<%= i %>">--%>
<%--                <%= i %>--%>
<%--            </option>--%>
<%--            <% } %>--%>
<%--        </select>--%>

    <button type="submit">이동</button>
    <hr>

</body>
</html>