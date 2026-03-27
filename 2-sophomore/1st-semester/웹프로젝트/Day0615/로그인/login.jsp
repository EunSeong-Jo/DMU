<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
    <style>
        label {
            display: inline-block;
            width: 50px;
        }
    </style>
</head>
<body>
<jsp:include page="../include_menu.jsp"/>

<h1>로그인</h1>

<!-- 📝 form 태그의 action → 로그인 처리 JSP 연결 -->
<form method="post" action="login-submit.jsp">
    <p><label for="user_id" >ID: </label>

        <!-- 📝 name="user_id" → request.getParameter("user_id")로 받음 -->
        <input type="text" id="user_id" name="user_id" required /></p>
    <p><label for="password">PWD: </label>

        <!-- 📝 name="password" → request.getParameter("password")로 받음 -->
        <input type="password" id="password" name="password" required/></p>

    <div>
        <button type="submit">로그인</button>
        <button type="reset">초기화</button>
    </div>
</form>

</body>
</html>