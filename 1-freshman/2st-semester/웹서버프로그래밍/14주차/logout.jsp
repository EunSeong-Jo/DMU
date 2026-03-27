<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%
    // 세션 무효화
    session.invalidate();

    // 로그인 페이지로 리다이렉트
    response.sendRedirect("member.jsp");
%>
