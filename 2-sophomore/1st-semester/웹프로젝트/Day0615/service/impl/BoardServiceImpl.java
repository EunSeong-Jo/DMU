package kr.ac.dongyang.website.jspwebsite.service.impl;

import kr.ac.dongyang.website.jspwebsite.dao.BoardDao;
import kr.ac.dongyang.website.jspwebsite.dto.BoardDto;
import kr.ac.dongyang.website.jspwebsite.service.BoardService;

import java.util.List;

// BoardService 인터페이스의 구현 클래스
// 실제 게시판 관련 DB 작업을 DAO를 통해 처리
public class BoardServiceImpl implements BoardService {

    // 게시글 목록 조회
    @Override
    public List<BoardDto> getBoardList() {
        BoardDao boardDao = new BoardDao();                    // DAO 인스턴스 생성
        List<BoardDto> boardList = boardDao.getBoardList();    // DB에서 게시글 목록 조회
        return boardList;
    }

    // 게시글 추가
    @Override
    public boolean addBoard(BoardDto board) {
        BoardDao boardDao = new BoardDao();                    // DAO 인스턴스 생성
        boolean result = boardDao.addBoard(board);             // 게시글 추가 요청
        return result;                                         // 성공 여부 반환
    }

    // 게시글 단건 조회 (ID 기준)
    @Override
    public BoardDto getBoard(long boardId) {
        BoardDao boardDao = new BoardDao();                    // DAO 인스턴스 생성
        BoardDto board = boardDao.getBoard(boardId);           // ID에 해당하는 게시글 조회
        return board;
    }

    // 게시글 수정
    @Override
    public boolean updateBoard(BoardDto board) {
        BoardDao boardDao = new BoardDao();                    // DAO 인스턴스 생성
        boolean result = boardDao.updateBoard(board);          // 게시글 수정 요청
        return result;
    }

}
