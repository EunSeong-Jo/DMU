package kr.ac.dongyang.website.jspwebsite.dto;

import lombok.*;

import java.util.Date;

@Getter  // 📝 Lombok 어노테이션 - getter/setter 자동 생성 → 시험 출제 가능
@Setter  // 📝 Lombok 어노테이션 - getter/setter 자동 생성 → 시험 출제 가능
@ToString  // 📝 toString 메서드 자동 생성 → 시험 출제 가능
@Builder  // 📝 Lombok 어노테이션 - 빌더 패턴 → 시험 출제 가능
@AllArgsConstructor  // 📝 모든 필드 생성자 → 시험 출제 가능
@NoArgsConstructor  // 📝 기본 생성자 → 시험 출제 가능
public class BoardDto {

    // 게시글 고유 ID (기본 키)
    long id;  // 📝 게시글 ID 필드 → 시험 출제 가능

    // 게시글 제목
    String subject;  // 📝 게시글 제목 필드 → 시험 출제 가능

    // 게시글 본문 내용
    String contents;

    // 작성자 이름 또는 ID
    String writer;

    // 게시글 작성 일시
    Date createDt;

    // 게시글 마지막 수정 일시
    Date updateDt;

    // 조회수
    int viewCount;  // 📝 조회수 필드 → 시험 출제 가능

    // 작성자의 IP 주소
    String ipAddr;

}
