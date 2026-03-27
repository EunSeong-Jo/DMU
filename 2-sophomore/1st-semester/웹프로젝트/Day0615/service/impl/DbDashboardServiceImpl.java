package kr.ac.dongyang.website.jspwebsite.service.impl;

import kr.ac.dongyang.website.jspwebsite.dao.BoardDao;
import kr.ac.dongyang.website.jspwebsite.dao.MemberDao;
import kr.ac.dongyang.website.jspwebsite.dto.DashboardDto;
import kr.ac.dongyang.website.jspwebsite.service.DashboardService;

// DashboardService 인터페이스의 실제 구현 클래스
// 회원 수, 게시글 수 등을 DB에서 조회하여 대시보드 정보 제공
public class DbDashboardServiceImpl implements DashboardService {

    // 대시보드에 필요한 주요 정보를 반환하는 메서드
    @Override
    public DashboardDto mainInfo() {

        // 회원 수 구하기: MemberDao를 이용해 회원 목록을 조회하고 크기를 계산
        MemberDao memberDao = new MemberDao();  // 📝 회원 DAO 객체 생성 → 시험 출제 가능
        int memberCount = memberDao.getMemberList().size();  // 📝 전체 회원 수 계산 → 시험 출제 가능

        // 게시글 수 구하기: BoardDao를 이용해 게시글 목록을 조회하고 크기를 계산
        BoardDao boardDao = new BoardDao();  // 📝 게시판 DAO 객체 생성 → 시험 출제 가능
        int boardCount = boardDao.getBoardList().size();  // 📝 전체 게시글 수 계산 → 시험 출제 가능

        // DashboardDto 객체를 생성하여 반환
        return DashboardDto.builder()  // 📝 DashboardDto 빌더 시작 → 시험 출제 가능
                .memberCount(memberCount)           // 회원 수 세팅
                .bbsContentsCount(boardCount)       // 게시글 수 세팅
                .build();  // 📝 DashboardDto 객체 생성 완료 → 시험 출제 가능
    }
}
