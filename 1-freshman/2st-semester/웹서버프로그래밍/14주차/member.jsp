<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
    <title>회원 인증</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 400px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }
        .signup-link {
            text-align: right;
            margin-bottom: 20px;
        }
        .signup-link a {
            text-decoration: none;
            color: #007bff;
            font-weight: bold;
            font-size: 14px;
        }
        .signup-link a:hover {
            text-decoration: underline;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 14px;
        }
        .form-group input[type="text"],
        .form-group input[type="password"] {
            width: 100%;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .form-actions {
            text-align: right; /* 로그인 버튼 오른쪽 정렬 */
        }
        .form-actions button {
            padding: 10px 20px;
            font-size: 14px;
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .form-actions button:hover {
            background-color: #0056b3;
        }
    </style>
    <script language="JavaScript">
        function Check() {
            if (Member.id.value.length < 1) {
                alert("아이디를 입력하세요.");
                Member.id.focus();
                return false;
            }

            if (Member.pass.value.length < 1) {
                alert("비밀번호를 입력하세요.");
                Member.pass.focus();
                return false;
            }

            Member.submit();
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>회원 인증</h1>
        <div class="signup-link">
            <a href="member_input.jsp">회원가입</a>
        </div>
        <form name="Member" method="post" action="member_ok.jsp">
            <div class="form-group">
                <label for="id">ID</label>
                <input type="text" id="id" name="id" maxlength="10">
            </div>
            <div class="form-group">
                <label for="pass">비밀번호</label>
                <input type="password" id="pass" name="pass" maxlength="10">
            </div>
            <div class="form-actions">
                <button type="button" onclick="Check()">로그인</button>
            </div>
        </form>
    </div>
</body>
</html>
