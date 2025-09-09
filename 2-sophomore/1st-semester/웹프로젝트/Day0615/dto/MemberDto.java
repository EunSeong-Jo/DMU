package kr.ac.dongyang.website.jspwebsite.dto;

import lombok.*;

import java.util.Date;

@Getter  // 📝 Lombok 어노테이션 - getter/setter 자동 생성 → 시험 출제 가능
@Setter  // 📝 Lombok 어노테이션 - getter/setter 자동 생성 → 시험 출제 가능
@Builder  // 📝 Lombok 어노테이션 - 빌더 패턴 → 시험 출제 가능
@AllArgsConstructor  // 📝 모든 필드 생성자 → 시험 출제 가능
@NoArgsConstructor  // 📝 기본 생성자 → 시험 출제 가능
@ToString  // 📝 toString 메서드 자동 생성 → 시험 출제 가능
public class MemberDto {

    // 회원 아이디 (기본 키 역할)
    String userId;  // 📝 사용자 ID 필드 → 시험 출제 가능

    // 회원 이름
    String userName;

    // 비밀번호 (암호화되었을 수도 있음)
    String password;

    // 회원 등록 날짜
    Date createDt;  // 📝 가입일 필드 → 시험 출제 가능

    // 회원 정보 수정 날짜
    Date updateDt;

}
