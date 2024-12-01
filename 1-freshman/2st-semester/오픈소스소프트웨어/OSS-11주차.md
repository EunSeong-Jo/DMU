# Git 브랜치 병합과 충돌 해결

---

## 1. 브랜치 병합 개요

### 1.1 브랜치 병합의 종류
- **Fast-Forward 병합**
  - 두 브랜치가 일렬 상태일 때, 단순히 포인터만 이동.
  ```bash
  $ git merge <브랜치명>
  ```
- **3-Way 병합**
  - 두 브랜치가 갈라져 있을 때, 새로운 커밋을 생성하여 병합.
  ```bash
  $ git merge <브랜치명> --no-ff
  ```
- **Squash 병합**
  - 브랜치 내용을 하나의 커밋으로 병합.
  ```bash
  $ git merge <브랜치명> --squash
  $ git commit -m "Squash merge 메시지"
  ```

### 1.2 병합의 주요 옵션
- **--ff-only** : Fast-Forward 병합만 허용.
- **--no-ff** : Fast-Forward 병합 방지, 무조건 3-Way 병합 수행.
- **--squash** : 병합 브랜치 이력 없이 현재 브랜치에 병합.

---

## 2. 병합 충돌 발생과 해결

### 2.1 병합 충돌 이해
- **충돌 조건**
  - 동일 파일의 동일 부분이 두 브랜치에서 다르게 수정된 경우.
- **충돌 발생 시 메시지**
  - `CONFLICT (content) : Merge conflict in <파일명>`

### 2.2 충돌 해결 과정
1. 충돌 발생한 파일 수정
   - 충돌 표시
     ```text
     <<<<<<< HEAD

     현재 브랜치 내용

     =======

     병합 브랜치 내용

     >>>>>>> <브랜치명>
     ```
2. 충돌 해결 후 파일 저장

3. 수정된 파일을 Staging 영역에 추가
   ```bash
   $ git add <파일명>
   ```
4. 커밋하여 병합 완료
   ```bash
   $ git commit -m "Resolve conflict 메시지"
   ```

### 2.3 충돌 취소
- 병합 취소
  ```bash
  $ git merge --abort
  ```

---

## 3. 실습 예제

### 3.1 Fast-Forward 병합
```bash
$ git merge <브랜치명>
```

### 3.2 3-Way 병합
1. 병합 수행
   ```bash
   $ git merge <브랜치명> --no-ff
   ```
2. 충돌 발생 시
   ```bash
   $ git merge topic
   CONFLICT (content) : Merge conflict in <파일명>
   ```
3. 충돌 해결 및 병합 완료
   ```bash
   $ git add <파일명>
   $ git commit -m "Resolve conflict"
   ```

### 3.3 Squash 병합
1. 병합 수행
   ```bash
   $ git merge <브랜치명> --squash
   ```
2. 커밋
   ```bash
   $ git commit -m "Squash merge 메시지"
   ```

---

## Summary

### 병합 명령어 요약
```bash
# Fast-Forward 병합
$ git merge <브랜치명>

# 3-Way 병합
$ git merge <브랜치명> --no-ff

# Squash 병합
$ git merge <브랜치명> --squash
$ git commit -m "Squash merge 메시지"

# 병합 취소
$ git merge --abort
```

### 충돌 해결 요약
1. 충돌 파일 수정 후 저장

2. 파일 Staging
   ```bash
   $ git add <파일명>
   ```
3. 병합 완료 커밋
   ```bash
   $ git commit -m "Resolve conflict 메시지"
   ```
