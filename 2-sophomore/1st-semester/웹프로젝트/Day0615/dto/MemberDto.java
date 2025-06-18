package kr.ac.dongyang.website.jspwebsite.dto;

import lombok.*;

import java.util.Date;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class MemberDto {

    // 회원 아이디 (기본 키 역할)
    String userId;

    // 회원 이름
    String userName;

    // 비밀번호 (암호화되었을 수도 있음)
    String password;

    // 회원 등록 날짜
    Date createDt;

    // 회원 정보 수정 날짜
    Date updateDt;

}
