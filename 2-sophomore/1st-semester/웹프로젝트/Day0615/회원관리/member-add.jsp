<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <link rel="stylesheet" href="/main.css"/>
</head>
<body>
<jsp:include page="include_menu.jsp"/>

<h1>회원 추가</h1>
<div class="member-add">
    <form action="/member-add-submit.jsp" method="post">
        <div>
            <label for="userName">이름</label>

            // 📝 input 태그 name 속성 → request.getParameter(...)에서 사용됨 → 시험 출제 가능
            <input type="text" id="userName" name="user_name" required/>

        </div>
        <div>
            <label for="userId">아이디</label>

            // 📝 input 태그 name 속성 → request.getParameter(...)에서 사용됨 → 시험 출제 가능
            <input type="text" id="userId" name="user_id" required/>

        </div>
        <div>
            <label for="password">비밀번호</label>

            // 📝 input 태그 name 속성 → request.getParameter(...)에서 사용됨 → 시험 출제 가능
            <input type="password" id="password" name="password" required/>

        </div>
        <div>
            <button type="submit">회원 추가</button>
        </div>
    </form>
</div>

</body>
</html>
