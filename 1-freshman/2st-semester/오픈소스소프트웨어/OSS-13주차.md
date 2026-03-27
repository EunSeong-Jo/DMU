# Git 버전 되돌리기와 커밋 취소

---

## 1. 버전 되돌리기 (`reset`)

### 1.1 `reset` 명령어 개요
- 이전 커밋으로 되돌리며, 작업 디렉토리, 스테이징 영역, Git 저장소 상태를 변경.
- **3가지 옵션**
  - `--hard` : 작업 디렉토리, 스테이징 영역, Git 저장소 모두 변경.
  - `--mixed` : Git 저장소와 스테이징 영역만 변경.
  - `--soft` : Git 저장소만 변경.

### 1.2 주요 명령어
- 특정 커밋으로 되돌리기
  ```bash
  $ git reset --hard <commit_id>
  $ git reset --mixed <commit_id>
  $ git reset --soft <commit_id>
  ```
- 바로 이전 상태로 복원
  ```bash
  $ git reset --hard ORIG_HEAD
  ```

### 1.3 `reset` 옵션 비교
| 옵션       | Git 저장소 | 스테이징 영역 | 작업 디렉토리 |
|------------|------------|---------------|----------------|
| `--hard`   | 변경       | 변경          | 변경           |
| `--mixed`  | 변경       | 변경          | 유지           |
| `--soft`   | 변경       | 유지          | 유지           |

---

## 2. 커밋 취소 (`revert`)

### 2.1 `revert` 명령어 개요
- 이전 커밋을 취소하면서 새로운 커밋 생성.
- **`reset`과 차이점**
  - `reset` : 이전 커밋 상태로 되돌리고 이후 커밋 이력 삭제.
  - `revert` : 이전 커밋을 되돌리는 새로운 커밋 생성, 기존 이력 유지.

### 2.2 주요 명령어
- 최신 커밋 취소
  ```bash
  $ git revert HEAD
  ```
- 특정 커밋 취소
  ```bash
  $ git revert <commit_id>
  ```
- 충돌 발생 시 해결
  ```bash
  $ git revert --continue
  ```
- 메시지 없이 자동 커밋
  ```bash
  $ git revert --no-edit HEAD
  ```

### 2.3 `revert` 와 `reset` 비교
| 항목       | `reset`                                | `revert`                                  |
|------------|----------------------------------------|-------------------------------------------|
| 목적       | 특정 커밋 상태로 이동, 이후 이력 삭제  | 특정 커밋 취소, 새로운 커밋 생성          |
| 새로운 커밋 | 없음                                   | 있음                                      |
| 이력 유지  | 삭제                                   | 유지                                     |
| 작업 트리  | 깨끗하지 않아도 가능                   | 깨끗해야만 가능                           |

---

## 3. 실습 요약

### 3.1 `reset` 실습
```bash
# 저장소 초기화
$ git init grst
$ echo "123" > file.txt
$ git add file.txt
$ git commit -m "Commit 1"
$ echo "ABC" >> file.txt
$ git commit -am "Commit 2"
$ echo "AB12" >> file.txt
$ git commit -am "Commit 3"

# 이전 커밋으로 되돌리기
$ git reset --hard HEAD~1
$ git reset --mixed HEAD~2
$ git reset --soft HEAD~3
```

### 3.2 `revert` 실습
```bash
# 커밋 취소
$ git revert HEAD
$ git revert HEAD~2

# 충돌 발생 시 해결
$ git revert --continue
```

---

## Summary

### `reset` 명령어
```bash
$ git reset --hard <commit_id>
$ git reset --mixed <commit_id>
$ git reset --soft <commit_id>
$ git reset --hard ORIG_HEAD
```

### `revert` 명령어
```bash
$ git revert HEAD
$ git revert <commit_id>
$ git revert --no-edit HEAD
```