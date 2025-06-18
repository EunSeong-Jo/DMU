package kr.ac.dongyang.website.jspwebsite.service;

import kr.ac.dongyang.website.jspwebsite.dto.BoardDto;

import java.util.List;

public interface BoardService {

    /**
     * 게시글 목록
     */
    List<BoardDto> getBoardList();

    /**
     * 게시글 추가
     */
    boolean addBoard(BoardDto board);

    /**
     * 게시글 정보
     */
    BoardDto getBoard(long boardId);

    /**
     * 게시굴 수정
     */
    boolean updateBoard(BoardDto board);
}
