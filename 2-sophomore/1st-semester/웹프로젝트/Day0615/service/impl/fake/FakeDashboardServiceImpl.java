package kr.ac.dongyang.website.jspwebsite.service.impl.fake;

import kr.ac.dongyang.website.jspwebsite.dto.DashboardDto;
import kr.ac.dongyang.website.jspwebsite.service.DashboardService;

// DashboardService 인터페이스의 구현 클래스 중 하나
// 테스트용으로 DB 연결 없이 고정된 값을 반환함
public class FakeDashboardServiceImpl implements DashboardService {

    // DashboardService의 mainInfo() 메서드 오버라이드
    @Override
    public DashboardDto mainInfo() {

        // 대시보드에 보여줄 더미 데이터 생성 후 반환
        return DashboardDto.builder()
                .memberCount(10)        // 회원 수: 임의의 숫자 10
                .bbsContentsCount(21)   // 게시글 수: 임의의 숫자 21
                .build();
    }
}
