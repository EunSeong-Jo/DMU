<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>

    <!-- 공통 스타일시트 적용 -->
    <link rel="stylesheet" href="/main.css"/>
</head>
<body>

<!-- 공통 상단 메뉴 삽입 -->
<jsp:include page="include_menu.jsp"/>

<!-- 페이지 제목 -->
<h1>회원 추가</h1>

<div class="member-add">
    <!-- 회원 등록 폼 -->
    <form action="/member-add-submit.jsp" method="post">

        <!-- 사용자 이름 입력 -->
        <div>
            <label for="userName">이름</label>
            <input type="text" id="userName" name="user_name" required/>
        </div>

        <!-- 사용자 ID 입력 -->
        <div>
            <label for="userId">아이디</label>
            <input type="text" id="userId" name="user_id" required/>
        </div>

        <!-- 비밀번호 입력 -->
        <div>
            <label for="password">비밀번호</label>
            <input type="password" id="password" name="password" required/>
        </div>

        <!-- 제출 버튼 -->
        <div>
            <button type="submit">회원 추가</button>
        </div>
    </form>
</div>

</body>
</html>
