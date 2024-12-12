# 오픈소스 소프트웨어와 Git Stash 관리

---

## 1. 오픈소스 소프트웨어 개요

### 1.1 오픈소스 소프트웨어 정의
- **OSS(Open Source Software)**
  - 소스코드가 공개되어 누구나 수정 및 재배포 가능.
  - 소프트웨어 발전 및 버그 개선을 빠르게 수행 가능.
- **자유 소프트웨어와 오픈소스 소프트웨어**
  - GNU 프로젝트로 시작.
  - "Free"는 비용이 아닌 자유의 의미.
  - 예: Linux, Git, Firefox.

### 1.2 주요 라이선스
- **GPL (GNU General Public License)**
  - 소스코드 공개 의무.
  - 2차 저작물도 GPL로 배포.
- **MIT License**
  - 최소한의 제한, 수정 및 배포가 자유로움.
  - 예 : jQuery, Bootstrap.
- **Apache License**
  - 소스코드 공개 의무 없음.
  - 예 : Android, Hadoop.

### 1.3 주요 오픈소스 소프트웨어
- **AI 및 빅데이터** : Python, TensorFlow, PyTorch.
- **웹 및 데이터베이스** : Apache, MySQL.
- **운영체제 및 도구** : Linux, Git.

---

## 2. Git Stash 관리

### 2.1 Stash 개요
- **Stash란**
  - 작업 디렉토리 및 스테이징 영역의 변경사항을 임시 저장.
  - 스택 구조로 가장 최근에 저장된 내용이 맨 위에 위치.
- **필요성**
  - 브랜치 전환 또는 과거 커밋으로 이동 시 작업 상태 저장.

### 2.2 Stash 명령어
- **임시 저장**
  ```bash
  $ git stash                   # 기본 저장
  $ git stash -m "메시지"       # 메시지 포함 저장
  $ git stash -u               # 추적되지 않은 파일도 포함
  ```
- **임시 저장 복원**
  ```bash
  $ git stash apply             # 복원 (목록 유지)
  $ git stash pop               # 복원 (목록 삭제)
  $ git stash apply --index     # 스테이징 영역 포함 복원
  ```
- **목록 관리**
  ```bash
  $ git stash list              # Stash 목록 보기
  $ git stash show stash@{n}    # 특정 Stash 상세 보기
  $ git stash drop stash@{n}    # 특정 Stash 삭제
  $ git stash clear             # 모든 Stash 삭제
  ```

### 2.3 Stash 실습
1. 저장소 생성
   ```bash
   $ git init gstash
   ```
2. 파일 생성 및 변경
   ```bash
   $ echo "내용" > file.txt
   $ git add file.txt
   $ echo "추가 내용" >> file.txt
   ```
3. Stash로 저장
   ```bash
   $ git stash
   ```
4. 저장 복원
   ```bash
   $ git stash apply
   ```

---

## Summary

### 주요 명령어 요약
```bash
# Stash 저장
$ git stash
$ git stash -m "메시지"
$ git stash -u

# Stash 복원
$ git stash apply
$ git stash pop
$ git stash apply --index

# Stash 관리
$ git stash list
$ git stash show stash@{n}
$ git stash drop stash@{n}
$ git stash clear
```

### 오픈소스의 장단점
- **장점**
  - 협업 및 커스터마이징 용이.
  - 빠른 버그 수정과 업데이트.
- **단점**
  - 품질 보증, 보안 문제 발생 가능.
  - 유지보수 부담.
