package kr.ac.dongyang.website.jspwebsite.service;

import kr.ac.dongyang.website.jspwebsite.dto.MemberDto;

public interface LoginService {

    /**
     * login 처리(성공일 경우 MemberDto 리턴, 실패일 경우는 NULL
     */
    MemberDto login(String userId, String password);

}
