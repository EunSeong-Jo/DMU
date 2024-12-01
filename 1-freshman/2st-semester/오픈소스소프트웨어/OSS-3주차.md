# Git 설치, 설정, VSCode, 및 리눅스 명령어

---

## 1. Git 설치와 실행

### 1.1 Git 다운로드 및 설치
- **Git 홈페이지** : [https://git-scm.com/](https://git-scm.com/)
- **다운로드 경로** : [http://git-scm.com/downloads](http://git-scm.com/downloads)
- 설치 후 Git Bash와 Git GUI 제공.

### 1.2 설치 후 실행
- **Git 실행 방법**
  1. **Git Bash 실행** : 메뉴에서 직접 실행.
  2. **탐색기에서 실행** : `Git Bash Here` 선택.
  3. **CLI 사용** 
     ```bash
     $ pwd           # 현재 경로 확인
     $ ls -al        # 디렉토리 리스트 확인
     ```

---

## 2. Git 설정과 저장소 생성

### 2.1 주요 설정
- 사용자 이름과 이메일 설정
  ```bash
  $ git config --global user.name "사용자이름"
  $ git config --global user.email "이메일주소"
  ```
- 주요 설정 명령어
  ```bash
  $ git config --global core.editor "code --wait"   # 기본 편집기 설정
  $ git config --global core.autocrlf true         # 줄바꿈 자동 변환
  $ git config --global core.safecrlf false        # 줄바꿈 안전 설정
  $ git config --global init.defaultBranch main    # 기본 브랜치 이름
  ```

### 2.2 저장소 생성
- Git 저장소 초기화
  ```bash
  $ git init                # 현재 디렉토리를 Git 저장소로 초기화
  $ git init <폴더명>       # 특정 폴더를 Git 저장소로 초기화
  ```

---

## 3. 비주얼 스튜디오 코드 (VSCode)

### 3.1 VSCode 개요
- 오픈소스 에디터로 다양한 언어 및 확장을 지원.
- 다운로드: [https://code.visualstudio.com/](https://code.visualstudio.com/)

### 3.2 설치 및 설정
- 설치 시 "탐색기에서 VSCode로 열기" 메뉴 선택 권장.
- 주요 구성 요소
  - 탐색기, 검색, 소스 제어, 디버그, 확장 프로그램 등.

---

## 4. 리눅스 명령어

### 4.1 기본 명령어
- **디렉토리 관련**
  ```bash
  $ pwd          # 현재 디렉토리 확인
  $ mkdir <이름> # 새 디렉토리 생성
  $ ls -al       # 파일 및 디렉토리 상세 목록 확인
  ```

- **파일 관련**
  ```bash
  $ touch <파일명>     # 빈 파일 생성
  $ echo "내용" > 파일 # 파일에 내용 작성
  $ cat <파일명>       # 파일 내용 보기
  $ cp <원본> <대상>  # 파일 복사
  $ mv <파일명> <새이름> # 파일 이름 변경
  $ rm <파일명>        # 파일 삭제
  ```

### 4.2 파이프와 리다이렉트
- **명령어 조합**
  ```bash
  $ cat file1 file2 | more # 페이지 단위로 출력
  $ echo "내용" >> file    # 기존 파일에 내용 추가
  ```

---

## Summary

### Git 명령어 정리
```bash
# 저장소 생성 및 초기화
$ git init

# 설정
$ git config --global user.name "이름"
$ git config --global user.email "이메일"

# 파일 추가 및 커밋
$ git add <파일>
$ git commit -m "메시지"

# 상태 및 로그 확인
$ git status
$ git log --oneline
```

### 리눅스 명령어 정리
```bash
# 디렉토리 확인 및 이동
$ pwd
$ cd <디렉토리>

# 파일 작업
$ touch <파일>
$ echo "내용" > <파일>
$ cat <파일>

# 삭제
$ rm <파일>
$ rm -rf <디렉토리>
```
