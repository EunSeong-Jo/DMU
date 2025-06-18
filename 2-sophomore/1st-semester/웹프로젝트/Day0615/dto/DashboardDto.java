package kr.ac.dongyang.website.jspwebsite.dto;

import lombok.*;

@Getter
@Setter
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DashboardDto {

    /**
     * 회원수
     */
    int memberCount;

    /**
     * 게시글수
     */
    int bbsContentsCount;


}
