package kr.ac.dongyang.website.jspwebsite.service.impl.fake;

import kr.ac.dongyang.website.jspwebsite.dto.MemberDto;
import kr.ac.dongyang.website.jspwebsite.service.LoginService;

// LoginService 인터페이스의 가짜 구현체
// 실제 DB와 연결하지 않고, 고정된 사용자 정보로 로그인 처리
public class FakeLoginServiceImpl implements LoginService {

    // 로그인 처리 메서드
    @Override
    public MemberDto login(String userId, String password) {

        boolean result = false;

        // 하드코딩된 ID/PW 값이 일치하는지 검사
        if ("hong".equals(userId) && "1234".equals(password)) {
            result = true;
        }

        // 로그인 실패 시 null 반환
        if (!result) {
            return null;
        }

        // 로그인 성공 시 MemberDto 객체를 생성하여 반환
        return MemberDto.builder()
                .userId(userId)             // 로그인한 ID
                .userName("홍길동2")         // 사용자 이름은 고정된 더미값
                .build();
    }
}
