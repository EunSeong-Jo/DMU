<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
    <title>회원 가입</title>
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
            max-width: 500px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        .form-group {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .form-group label {
            width: 80px;
            font-weight: bold;
            font-size: 14px;
        }
        .form-group input[type="text"],
        .form-group input[type="password"] {
            flex: 1;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .form-group button {
            margin-left: 10px;
            padding: 10px;
            font-size: 14px;
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .form-group button:hover {
            background-color: #0056b3;
        }
        .form-actions {
            text-align: center;
            margin-top: 20px;
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
            if (Member_Input.id.value.length < 1) {
                alert("아이디를 입력하세요.");
                Member_Input.id.focus();
                return false;
            }

            if (Member_Input.pass.value.length < 1) {
                alert("비밀번호를 입력하세요.");
                Member_Input.pass.focus();
                return false;
            }

            if (Member_Input.name.value.length < 1) {
                alert("이름을 입력하세요.");
                Member_Input.name.focus();
                return false;
            }

            Member_Input.submit();
        }

        function Check_id() {
            browsing_window = window.open(
                "checkid.jsp?id=" + Member_Input.id.value,
                "_idcheck",
                "height=200,width=300, menubar=no, directories=no, resizable=no, status=no, scrollbars=yes"
            );
            browsing_window.focus();
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>회원 가입</h1>
        <form name="Member_Input" method="post" action="member_output.jsp">
            <div class="form-group">
                <label for="id">아이디</label>
                <input type="text" id="id" name="id" maxlength="10">
                <button type="button" onclick="Check_id()">중복검사</button>
            </div>
            <div class="form-group">
                <label for="pass">비밀번호</label>
                <input type="password" id="pass" name="pass" maxlength="10">
            </div>
            <div class="form-group">
                <label for="name">이름</label>
                <input type="text" id="name" name="name" maxlength="10">
            </div>
            <div class="form-group">
                <label for="phone">전화번호</label>
                <input type="text" id="phone" name="phone" maxlength="20">
            </div>
            <div class="form-group">
                <label for="email">이메일</label>
                <input type="text" id="email" name="email" maxlength="50">
            </div>
            <div class="form-actions">
                <button type="button" onclick="Check()">회원가입</button>
            </div>
        </form>
    </div>
</body>
</html>
