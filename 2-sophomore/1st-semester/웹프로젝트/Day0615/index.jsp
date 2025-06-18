<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>회원/게시판 시스템</title>
    <!-- 스타일시트 연결 -->
    <link rel="stylesheet" href="/main.css"/>
</head>
<body>

<!-- 공통 메뉴 영역 삽입 -->
<jsp:include page="include_menu.jsp"/>

<!-- 대시보드 제목 -->
<h1>대시 보드</h1>

<!-- 대시보드 정보 삽입 (회원 수, 게시글 수 출력) -->
<jsp:include page="include_dashboard.jsp"/>

</body>
</html>
