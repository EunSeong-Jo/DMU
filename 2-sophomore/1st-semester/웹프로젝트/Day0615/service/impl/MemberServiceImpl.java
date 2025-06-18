package kr.ac.dongyang.website.jspwebsite.service.impl;

import kr.ac.dongyang.website.jspwebsite.dao.MemberDao;
import kr.ac.dongyang.website.jspwebsite.dto.MemberDto;
import kr.ac.dongyang.website.jspwebsite.service.MemberService;

import java.util.List;

// MemberService 인터페이스의 구현 클래스
// DAO를 이용해 실제 DB 연동 작업을 처리함
public class MemberServiceImpl implements MemberService {

    /**
     * 전체 회원 목록 조회
     */
    @Override
    public List<MemberDto> getMemberList() {
        MemberDao memberDao = new MemberDao();                 // DAO 객체 생성
        List<MemberDto> memberList = memberDao.getMemberList(); // 회원 목록 조회
        return memberList;
    }

    /**
     * 특정 회원 정보 조회 (userId 기준)
     */
    @Override
    public MemberDto getMember(String userId) {
        MemberDao memberDao = new MemberDao();                 // DAO 객체 생성
        MemberDto member = memberDao.getMember(userId);        // 회원 단건 조회
        return member;
    }

    /**
     * 신규 회원 추가
     */
    @Override
    public boolean addMember(MemberDto member) {
        MemberDao memberDao = new MemberDao();                 // DAO 객체 생성
        boolean result = memberDao.addMember(member);          // 회원 등록 요청
        return result;                                         // 성공 여부 반환
    }

    /**
     * 회원 정보 수정
     */
    @Override
    public boolean updateMember(MemberDto member) {
        MemberDao memberDao = new MemberDao();                 // DAO 객체 생성
        boolean result = memberDao.updateMember(member);       // 회원 정보 수정 요청
        return result;
    }

    /**
     * 회원 삭제
     */
    @Override
    public boolean deleteMember(String userId) {
        MemberDao memberDao = new MemberDao();                 // DAO 객체 생성
        boolean result = memberDao.deleteMember(userId);       // 해당 ID 회원 삭제 요청
        return result;
    }
}
