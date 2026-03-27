<%@ page import="kr.ac.dongyang.website.jspwebsite.service.DashboardService" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.service.impl.DbDashboardServiceImpl" %>
<%@ page import="kr.ac.dongyang.website.jspwebsite.dto.DashboardDto" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%
    // 대시보드 정보를 제공할 서비스 객체 생성
    DashboardService dashboardService = new DbDashboardServiceImpl();  // 📝 서비스 객체 생성 (`new DbDashboardServiceImpl()`) → 시험 출제 가능

    // DB에서 회원 수와 게시글 수 조회
    DashboardDto dashboard = dashboardService.mainInfo();  // 📝 대시보드 정보 조회 메서드 호출 (`mainInfo()`) → 시험 출제 가능
%>

<!-- 조회한 회원 수 출력 -->
<p>현재 회원수: <%=dashboard.getMemberCount()%>명</p>  // 📝 표현식 `<%= %>`을 통한 값 출력 (`getMemberCount()`) → 시험 출제 가능

<!-- 조회한 게시글 수 출력 -->
<p>현재 게시글 수: <%=dashboard.getBbsContentsCount()%>건</p>  // 📝 표현식 `<%= %>`을 통한 값 출력 (`getBbsContentsCount()`) → 시험 출제 가능
