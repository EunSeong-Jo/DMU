package kr.ac.dongyang.website.jspwebsite.dto;

import lombok.*;

import java.util.Date;

@Getter
@Setter
@ToString
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class BoardDto {

    // 게시글 고유 ID (기본 키)
    long id;

    // 게시글 제목
    String subject;

    // 게시글 본문 내용
    String contents;

    // 작성자 이름 또는 ID
    String writer;

    // 게시글 작성 일시
    Date createDt;

    // 게시글 마지막 수정 일시
    Date updateDt;

    // 조회수
    int viewCount;

    // 작성자의 IP 주소
    String ipAddr;

}
