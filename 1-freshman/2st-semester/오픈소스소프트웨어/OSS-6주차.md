# 대면수업
# Git Cheat Sheet 및 Pull Request

---

## 1. Pull Request 가이드

### 1.1 Pull Request란?
- **PR(Pull Request)** : 다른 사람의 저장소에 변경 내용을 요청하는 작업.
- **Upstream** : 오픈소스 프로젝트 또는 타인의 저장소.
- **Origin** : Fork한 본인의 저장소.

### 1.2 PR 처리 과정
1. **기여자**
   - 저장소 Fork
   - 파일 수정 및 커밋
   - Pull Request 생성
2. **관리자**
   - PR 검토 및 리뷰 요청
   - PR 병합(Merge)

### 1.3 PR 명령어 및 워크플로우
```bash
# PR 생성 (GitHub GUI에서 수행)
# 1. Fork → 저장소 복제
$ git clone <forked-repo-url>
$ git checkout -b feature-branch

# 2. 변경 내용 추가 및 커밋
$ git add .
$ git commit -m "PR 변경 내용"

# 3. 원격 저장소에 Push
$ git push origin feature-branch
```

### 1.4 PR 생성 및 병합
- **GitHub GUI**를 사용하여 PR 생성
  - "Compare & Pull Request" 클릭.
  - 변경 내용 및 관련 이슈(#issue-number) 설명.
- **PR 병합(Merge)**
  - 팀장이 PR 내용을 확인하고 병합 수행.

---

## 2. Git Cheat Sheet

### 2.1 기본 명령어
```bash
# 저장소 초기화
$ git init
$ git init .         # 현재 폴더에서 초기화
$ git init new-repo  # 새로운 폴더에서 초기화

# 상태 확인
$ git status
$ git status -s      # 간략한 상태 표시

# 파일 추가
$ git add .
$ git add file

# 파일 삭제
$ git rm --cached file  # Staging 영역에서만 삭제
$ git rm file           # Staging + Working Directory에서 삭제
```

### 2.2 커밋 및 로그
```bash
# 커밋
$ git commit -m "메시지"
$ git commit --amend      # 마지막 커밋 수정

# 로그
$ git log
$ git log --oneline
$ git log --graph --all
$ git log --patch | -p    # 상세 변경 내용 포함
```

### 2.3 브랜치 관리
```bash
# 브랜치 생성 및 이동
$ git branch new-branch
$ git switch new-branch

# 브랜치 삭제
$ git branch -d branch-name
$ git branch -D branch-name  # 강제 삭제

# 브랜치 확인
$ git branch -v
$ git branch -a
```

### 2.4 Reset 및 Revert
```bash
# Reset
$ git reset --soft HEAD~    # Git 저장소만 변경
$ git reset --mixed HEAD~   # Git 저장소 + Staging 변경
$ git reset --hard HEAD~    # 모든 영역 변경

# Revert
$ git revert HEAD
$ git revert --no-edit HEAD
```

### 2.5 기타 명령어
```bash
# 태그
$ git tag v1.0.0
$ git tag -a v1.1.0 -m "메시지"

# 원격 저장소 관리
$ git remote add origin <url>
$ git push origin main
$ git pull origin main
```
---

## Summary

### 주요 명령어 정리
```bash
# 저장소 초기화
$ git init

# 파일 추가 및 커밋
$ git add .
$ git commit -m "메시지"

# 브랜치 관리
$ git branch <브랜치명>
$ git switch <브랜치명>

# 원격 저장소
$ git push origin main
$ git pull origin main
```

### PR 워크플로우 요약
- Fork → Commit → Push → Pull Request 생성 → Review → Merge

