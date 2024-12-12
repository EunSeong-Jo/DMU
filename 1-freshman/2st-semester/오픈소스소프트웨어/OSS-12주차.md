# Git 리베이스, 커밋 수정, VSCode 활용

---

## 1. 브랜치 리베이스 (Rebase)

### 1.1 리베이스란?
- 브랜치의 Base를 수정하여 병합 이력을 선형으로 재구성.
- **장점** : 복잡한 이력을 단순화.
- **단점** : 기존 커밋 ID가 변경됨.

### 1.2 리베이스 수행
- 기본 리베이스
  ```bash
  $ git rebase main
  ```
- 특정 브랜치를 다른 브랜치 기준으로 재배치
  ```bash
  $ git rebase <newparent> <branch>
  ```

### 1.3 리베이스 충돌 해결
1. 충돌 발생 시 수정
   ```bash
   $ git add <수정된 파일>
   ```
2. 리베이스 계속 진행
   ```bash
   $ git rebase --continue
   ```
3. 리베이스 중단
   ```bash
   $ git rebase --abort
   ```

---

## 2. 커밋 이력 수정

### 2.1 최신 커밋 수정
- 커밋 메시지 수정
  ```bash
  $ git commit --amend -m "새로운 메시지"
  ```
- 파일 추가 후 커밋 수정
  ```bash
  $ git add <파일>
  $ git commit --amend --no-edit
  ```

### 2.2 여러 커밋 수정 (대화형 Rebase)
- 대화형 Rebase 시작
  ```bash
  $ git rebase --interactive HEAD~<n>
  ```
- 주요 옵션
  - `pick` : 커밋 유지.
  - `reword` : 메시지 수정.
  - `squash` : 이전 커밋과 병합.
  - `drop` : 커밋 삭제.

---

## 3. VSCode에서 Git 활용

### 3.1 Git 저장소 초기화
1. VSCode에서 폴더 열기.
2. 소스 제어 패널에서 "저장소 초기화" 클릭.

### 3.2 파일 추가 및 커밋
- 파일 생성 → 변경 사항 패널에서 **Stage Changes** 클릭 → **Commit** 버튼 클릭.

### 3.3 Git Graph 설치 및 활용
1. **확장 프로그램 설치**
   - `Git Graph` 검색 후 설치.
2. **로그 확인**
   - 활동 바에서 Git Graph 선택 → 로그와 브랜치 시각화 확인.

### 3.4 Git 명령어와 VSCode 메뉴 활용
- 파일 변경 취소
  ```bash
  $ git restore <파일>
  ```
- 스테이징 취소
  ```bash
  $ git restore --staged <파일>
  ```

---

## Summary

### 리베이스 명령어
```bash
# 리베이스 수행
$ git rebase <브랜치>
$ git rebase --interactive HEAD~<n>

# 리베이스 충돌 해결
$ git rebase --continue
$ git rebase --abort
```

### 커밋 수정 명령어
```bash
# 최신 커밋 수정
$ git commit --amend -m "새 메시지"

# 여러 커밋 수정
$ git rebase --interactive HEAD~<n>
```

### VSCode와 Git
- **Git Graph**를 활용해 로그 확인.
- VSCode UI를 통해 변경 사항 관리 및 커밋.
