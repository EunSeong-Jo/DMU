<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>0328</title>
    <style>
        label{
            display: inline-block;
            width: 80px;
        }
        input:focus{
            background-color: yellow;
        }
    </style>
</head>
<body>
<!--
<h1>1. 클라이언트와 서버의 환경정보 읽기</h1>
<br>

<a href="exam01Get.jsp">GET 방식 전송</a>

<div>
    <label for="eng">영어 :
        <input type="text" id="eng">
    </label>
</div>

<div>
    <label for="kor">한글 :
        <input type="text" id="kor">
    </label>
</div>

<div>
    <button type="submit">POST 방식 전송</button>
</div>
-->

<form action="exam01Post.jsp" method="post">
    <h2>로그인</h2>

    <div>
        <label for="uId">아이디 :
            <input type="text" id="uId" name="userId" required>
        </label>
    </div>

    <div>
        <label for="uPw">비밀번호 :
            <input type="password" id="uPw" name="userPassword" required>
        </label>
    </div>

    <div>
        <button type="submit">로그인하기</button>
    </div>
</form>

</body>
</html>
