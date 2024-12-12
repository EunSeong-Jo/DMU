# Git 버전, 태그, 브랜치 활용

---

## 1. Git 버전과 태그 활용

### 1.1 버전 관리 개요
- **버전 정의** : 소프트웨어 변경 시점을 식별하기 위한 표기.
  - 형식 : `major.minor.patch` (예 : `1.0.0`)
    - **메이저** : 주요 변경 사항.
    - **마이너** : 새로운 기능 추가.
    - **패치** : 버그 수정.

### 1.2 태그 종류
- **Annotated 태그**
  - 작성자 정보, 메시지 포함.
  ```bash
  $ git tag -a v1.0.0 -m "태그 메시지"
  ```
- **Lightweight 태그**
  - 이름만 부여.
  ```bash
  $ git tag v1.0.1
  ```

### 1.3 태그 명령어
- 태그 보기
  ```bash
  $ git tag
  ```
- 태그 정보 확인
  ```bash
  $ git show v1.0.0
  ```
- 태그 삭제
  ```bash
  $ git tag -d v1.0.0
  ```

---

## 2. 브랜치 개요와 관리

### 2.1 브랜치 개념
- 브랜치는 독립적으로 작업할 수 있는 **분기점**.
- **장점**
  - 독립 작업 및 실험 가능.
  - 병합(merge)을 통해 변경 사항 통합.

### 2.2 주요 브랜치 명령어
- 브랜치 생성
  ```bash
  $ git branch <branch>
  $ git switch -c <branch>
  ```
- 브랜치 확인
  ```bash
  $ git branch -v
  ```
- 브랜치 이동
  ```bash
  $ git switch <branch>
  $ git checkout <branch>
  ```
- 브랜치 삭제
  ```bash
  $ git branch -d <branch>  # 병합된 브랜치 삭제
  $ git branch -D <branch>  # 강제 삭제
  ```

### 2.3 브랜치 실습
- **브랜치 생성 및 이동**
  ```bash
  $ git switch -c <branch>
  ```
- **기본 브랜치로 복귀**
  ```bash
  $ git switch main
  ```
- **분리된 HEAD 상태**
  ```bash
  $ git checkout HEAD~1
  ```

---

## Summary

### 태그 명령어 요약
```bash
# 주석 태그 생성
$ git tag -a v1.0.0 -m "메시지"

# 태그 확인
$ git tag

# 태그 정보 확인
$ git show v1.0.0

# 태그 삭제
$ git tag -d v1.0.0
```

### 브랜치 명령어 요약
```bash
# 브랜치 생성
$ git branch <브랜치 이름>

# 브랜치 생성 후 이동
$ git switch -c <브랜치 이름>

# 브랜치 확인
$ git branch -v

# 브랜치 삭제
$ git branch -d <브랜치 이름>
$ git branch -D <브랜치 이름>
```
