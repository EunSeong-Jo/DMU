<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>

    <!-- 공통 스타일 시트 연결 -->
    <link rel="stylesheet" href="/main.css"/>

    <!-- 로그인 폼 스타일 정의 -->
    <style>
        label {
            display: inline-block;
            width: 50px; /* 라벨 폭 고정하여 입력창 정렬 */
        }
    </style>
</head>
<body>

<!-- 상단 공통 메뉴 포함 -->
<jsp:include page="include_menu.jsp"/>

<!-- 로그인 폼 제목 -->
<h1>로그인</h1>

<!-- 로그인 입력 폼 -->
<form method="post" action="login-submit.jsp">
    <!-- 사용자 ID 입력 -->
    <p>
        <label for="user_id">ID: </label>
        <input type="text" id="user_id" name="user_id" required />
    </p>

    <!-- 비밀번호 입력 -->
    <p>
        <label for="password">PWD: </label>
        <input type="password" id="password" name="password" required />
    </p>

    <!-- 제출 및 초기화 버튼 -->
    <div>
        <button type="submit">로그인</button>
        <button type="reset">초기화</button>
    </div>
</form>

</body>
</html>
