package kr.ac.dongyang.website.jspwebsite.dto;

import lombok.*;

@Getter  // 📝 Lombok 어노테이션 - getter/setter 자동 생성 → 시험 출제 가능
@Setter  // 📝 Lombok 어노테이션 - getter/setter 자동 생성 → 시험 출제 가능
@ToString  // 📝 toString 메서드 자동 생성 → 시험 출제 가능
@Builder  // 📝 Lombok 어노테이션 - 빌더 패턴 → 시험 출제 가능
@NoArgsConstructor  // 📝 기본 생성자 → 시험 출제 가능
@AllArgsConstructor  // 📝 모든 필드 생성자 → 시험 출제 가능
public class DashboardDto {

    /**
     * 회원수
     */
    int memberCount;  // 📝 회원 수 정보 → 시험 출제 가능

    /**
     * 게시글수
     */
    int bbsContentsCount;  // 📝 게시글 수 정보 → 시험 출제 가능

}
