# 파일 비교, 삭제, 복원

---

## 1. 파일 비교 (diff)

### 1.1 Git 3 영역 파일 비교
- **작업 디렉토리 <---> 스테이징 영역**
  ```bash
  $ git diff
  ```
- **스테이징 영역 <---> Git 저장소**
  ```bash
  $ git diff --staged
  ```
- **작업 디렉토리 <---> Git 저장소**
  ```bash
  $ git diff HEAD
  ```

### 1.2 커밋 간 파일 비교
- **이전 커밋과 현재 커밋 비교**
  ```bash
  $ git diff HEAD~ HEAD
  ```
- **특정 커밋 간 비교**
  ```bash
  $ git diff <commit1> <commit2>
  ```

---

## 2. 파일 삭제 (rm)

### 2.1 작업 디렉토리 삭제
- **리눅스 명령**
  ```bash
  $ rm <file>
  ```

### 2.2 스테이징 영역 삭제
- **Git 명령**
  ```bash
  $ git rm --cached <file>
  ```

### 2.3 작업 디렉토리와 스테이징 영역 동시 삭제
- **Git 명령**
  ```bash
  $ git rm <file>
  ```

---

## 3. 파일 복원 (restore)

### 3.1 작업 디렉토리 복원
- 스테이징 영역 기준 복원
  ```bash
  $ git restore <file>
  ```

### 3.2 스테이징 영역 복원
- Git 저장소 기준 복원
  ```bash
  $ git restore --staged <file>
  ```

### 3.3 전체 복원
- 작업 디렉토리와 스테이징 영역 모두 복원
  ```bash
  $ git restore --source=HEAD --staged --worktree <file>
  ```

---

## 4. 실습 : 파일 관리

### 4.1 저장소 생성 및 파일 추가
- **명령어**
  ```bash
  $ git init
  $ echo "내용" > file.txt
  $ git add file.txt
  $ git commit -m "파일 추가"
  ```

### 4.2 파일 삭제
- 작업 디렉토리와 스테이징 영역에서 삭제
  ```bash
  $ git rm <file>
  ```
- 복구
  ```bash
  $ git restore --source=HEAD <file>
  ```

---

## Summary

### 파일 비교 명령어
```bash
$ git diff                # 작업 디렉토리 vs 스테이징 영역
$ git diff --staged       # 스테이징 영역 vs Git 저장소
$ git diff HEAD           # 작업 디렉토리 vs Git 저장소
```

### 파일 삭제 명령어
```bash
$ git rm <file>           # 작업 디렉토리와 스테이징 영역에서 삭제
$ git rm --cached <file>  # 스테이징 영역에서만 삭제
```

### 파일 복원 명령어
```bash
$ git restore <file>                    # 작업 디렉토리 복원
$ git restore --staged <file>           # 스테이징 영역 복원
$ git restore --source=HEAD <file>      # 작업 디렉토리 복원
$ git restore --source=HEAD --staged --worktree <file>
```
