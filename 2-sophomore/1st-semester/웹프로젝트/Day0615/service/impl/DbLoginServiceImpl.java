package kr.ac.dongyang.website.jspwebsite.service.impl;

import kr.ac.dongyang.website.jspwebsite.dao.MemberDao;
import kr.ac.dongyang.website.jspwebsite.dto.MemberDto;
import kr.ac.dongyang.website.jspwebsite.service.LoginService;

// LoginService 인터페이스를 구현한 클래스
// DB에 접근하여 실제 회원 정보로 로그인 처리 수행
public class DbLoginServiceImpl implements LoginService {

    // 로그인 요청을 처리하는 메서드
    @Override
    public MemberDto login(String userId, String password) {

        // MemberDao를 통해 userId에 해당하는 회원 정보 조회
        MemberDao memberDao = new MemberDao();  // 📝 DAO 객체 생성 → 시험 출제 가능
        MemberDto member = memberDao.getMember(userId);  // 📝 회원 정보 조회 → 시험 출제 가능

        // 해당 ID의 회원이 존재하지 않으면 로그인 실패 (null 반환)
        if (member == null) {
            return null;  // 📝 로그인 실패 처리 → 시험 출제 가능
        }

        // 입력한 비밀번호가 DB에 저장된 비밀번호와 다르면 로그인 실패
        if (!member.getPassword().equals(password)) {  // 📝 비밀번호 일치 여부 확인 → 시험 출제 가능
            return null;  // 📝 로그인 실패 처리 → 시험 출제 가능
        }

        // 로그인 성공 시 해당 회원 정보(MemberDto) 반환
        return member;  // 📝 로그인 성공 시 정보 반환 → 시험 출제 가능
    }
}
