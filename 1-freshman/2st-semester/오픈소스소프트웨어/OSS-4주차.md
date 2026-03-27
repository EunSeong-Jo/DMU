# Git 커밋, 로그, 및 과거 여행

---

## 1. Git 커밋과 로그

### 1.1 Git의 3 영역
- **작업 디렉토리** : 현재 작업 중인 파일.
- **스테이징 영역** : `git add`로 추가된 파일.
- **Git 저장소** : `git commit`으로 저장된 파일.

### 1.2 버전 관리 기본 명령어
- 파일 추가 및 커밋
  ```bash
  $ git add <파일명>      # 파일 스테이징
  $ git commit -m "메시지" # 변경 사항 저장
  ```
- 상태 확인
  ```bash
  $ git status        # 현재 상태 확인
  $ git status -s     # 간략한 상태 표시
  ```

### 1.3 로그 확인
- **로그 보기 명령어**
  ```bash
  $ git log                # 전체 로그 확인
  $ git log --oneline      # 간략히 표시
  $ git log --graph        # 그래프로 표시
  $ git log --patch        # 파일 변경 내용 확인
  $ git show               # 특정 커밋 정보 보기
  ```

---

## 2. 로그 이력과 과거 여행

### 2.1 과거로 이동
- 이전 커밋으로 이동
  ```bash
  $ git checkout HEAD~1    # 바로 이전 커밋
  $ git checkout HEAD~2    # 두 번째 이전 커밋
  ```
- 최신 상태로 복귀
  ```bash
  $ git checkout main      # 브랜치의 마지막 커밋
  ```

### 2.2 Detached HEAD 상태
- 과거 커밋으로 이동 시 Detached HEAD 상태 발생.
- 새로운 브랜치 생성 및 이동
  ```bash
  $ git switch -c <새 브랜치 이름>
  ```

---

## 3. 실습: 커밋과 로그

### 3.1 커밋 과정
- **파일 생성, 추가, 첫 번째 커밋**
  ```bash
  $ echo "aaa" > hello.txt
  $ git add hello.txt
  $ git commit -m "첫 번째 커밋"
  ```
- **파일 수정 및 두 번째 커밋**
  ```bash
  $ echo "bbb" >> hello.txt
  $ git commit -am "두 번째 커밋"
  ```
- **파일 재수정 및 세 번째 커밋**
  ```bash
  $ echo "ccc" >> hello.txt
  $ git commit -am "세 번째 커밋"
  ```

### 3.2 과거로 이동 및 복귀
- 과거로 이동
  ```bash
  $ git checkout HEAD~2
  ```
- 복귀
  ```bash
  $ git checkout -
  ```

---

## Summary

### 주요 Git 명령어
```bash
# 설정
$ git config --global user.name "이름"
$ git config --global user.email "이메일"

# 저장소 초기화
$ git init

# 파일 추가 및 커밋
$ git add <파일>
$ git commit -m "메시지"

# 로그 확인
$ git log --oneline
$ git log --graph

# 과거로 이동 및 복귀
$ git checkout HEAD~1
$ git checkout main
```

### 상태 확인 및 파일 조작
```bash
$ git status           # 상태 확인
$ git show HEAD        # 마지막 커밋 보기
$ git diff HEAD~ HEAD  # 두 커밋 비교
```
