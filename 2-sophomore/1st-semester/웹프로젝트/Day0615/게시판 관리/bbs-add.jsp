<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <!-- 외부 CSS 파일 연결 -->
    <link rel="stylesheet" href="/main.css"/>
</head>
<body>

<!-- 메뉴 영역 공통 포함 (include_menu.jsp 파일을 삽입) -->
// 📝 JSP include 지시어 사용 (`jsp:include page=...`) → 공통 메뉴 삽입 → 시험 출제 가능
<jsp:include page="../include_menu.jsp"/>
    <h1>게시글 추가</h1>

    <div class="member-add">

    <!-- 게시글 등록을 위한 폼 생성 -->
    <!-- 사용자가 입력한 내용은 bbs-add-submit.jsp로 POST 방식 전송됨 -->

        // 📝 form 전송 방식 지정 (`method="post"`) → 시험 출제 가능
    <form action="/게시판%20관리/bbs-add-submit.jspubmit.jsp" method="post">

    <!-- 작성자 입력란 -->
    <div>
        <label for="writer">작성자</label>

        // 📝 input/textarea 태그의 name 속성 → request.getParameter(...)로 사용됨 → 시험 출제 가능
        <input type="text" id="writer" name="writer" required/>

    </div>

    <!-- 제목 입력란 -->
    <div>
        <label for="subject">제목</label>

        // 📝 input/textarea 태그의 name 속성 → request.getParameter(...)로 사용됨 → 시험 출제 가능
        <input type="text" id="subject" name="subject" required/>

    </div>

    <!-- 내용 입력란 (여러 줄 텍스트 가능) -->
    <div>
        <label for="contents">내용</label>

        // 📝 input/textarea 태그의 name 속성 → request.getParameter(...)로 사용됨 → 시험 출제 가능
        <textarea id="contents" name="contents" cols="60" rows="10"></textarea>

    </div>

    <!-- 제출 버튼 -->
    <div>
        <button type="submit">게시글 추가</button>
    </div>

    </form>
    </div>

    </body>
</html>