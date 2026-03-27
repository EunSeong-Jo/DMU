package kr.ac.dongyang.website.jspwebsite.service;

import kr.ac.dongyang.website.jspwebsite.dto.MemberDto;

import java.util.List;

public interface MemberService {

    /**
     * 회원 목록
     */
    List<MemberDto> getMemberList();

    /**
     * 회원 정보
     */
    MemberDto getMember(String userId);

    /**
     * 회원 추가
     */
    boolean addMember(MemberDto member);

    /***
     * 회원 수정
     */
    boolean updateMember(MemberDto member);

    /**
     * 회원 삭제
     */
    boolean deleteMember(String userId);


}
