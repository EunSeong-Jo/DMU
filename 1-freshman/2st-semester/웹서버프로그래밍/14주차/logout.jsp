<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR"%>
<%
    // ���� ��ȿȭ
    session.invalidate();

    // �α��� �������� �����̷�Ʈ
    response.sendRedirect("member.jsp");
%>
