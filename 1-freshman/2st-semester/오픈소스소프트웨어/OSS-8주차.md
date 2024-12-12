# Git 원격 저장소 관리

---

## 1. 원격 저장소 복제 (Clone)

### 1.1 원격 저장소 복제
- 원격 저장소를 지역 저장소로 복제.
- 명령어
  ```bash
  $ git clone <저장소 URL>
  $ git clone <저장소 URL> <폴더명>  # 특정 폴더에 복제
  $ git clone <저장소 URL> .        # 현재 폴더에 복제
  ```

### 1.2 원격 저장소 관리
- 원격 저장소 별칭 확인 및 관리
  ```bash
  $ git remote -v           # 저장소 목록 확인
  $ git remote add <별칭> <URL> # 새로운 저장소 추가
  $ git remote rename <기존별칭> <새별칭> # 이름 변경
  $ git remote rm <별칭>    # 삭제
  ```

---

## 2. 지역과 원격 저장소 연동 (Push, Pull)

### 2.1 Personal Access Token (PAT)
- **이유** : 2021년 8월 이후 비밀번호 인증 대신 토큰 사용.
- 생성 방법
  1. GitHub → **Settings** → **Developer Settings** → **Personal Access Token** → **Generate Token**
  2. 생성된 토큰은 안전하게 보관 필요.

### 2.2 원격 저장소로 Push
- 명령어
  ```bash
  $ git push <원격저장소별칭> <브랜치명>
  $ git push                 # 기본 브랜치로 Push
  ```
- 인증 오류 해결
  ```bash
  $ git push -u https://<토큰>@github.com/<사용자>/<저장소>.git
  ```

### 2.3 원격 저장소로부터 Pull
- Pull 명령어
  ```bash
  $ git pull <원격저장소별칭> <브랜치명>
  $ git pull                 # 기본 브랜치 Pull
  ```

### 2.4 Fetch와 Merge
- Fetch 명령어
  ```bash
  $ git fetch <원격저장소별칭>
  ```
- Fetch 후 병합
  ```bash
  $ git merge <원격저장소별칭>/<브랜치명>
  ```

---

## 3. 실습: 원격 저장소와 연동

### 3.1 Clone과 Fetch 실습
1. GitHub에서 새로운 원격 저장소 생성.
2. 원격 저장소를 지역에 복제
   ```bash
   $ git clone <URL>
   ```
3. 원격 저장소 업데이트 후 Fetch 및 병합
   ```bash
   $ git fetch origin
   $ git merge origin/main
   ```

### 3.2 Push 실습
1. 지역 저장소에서 파일 생성 및 커밋
   ```bash
   $ echo "New Content" > file.txt
   $ git add file.txt
   $ git commit -m "Add new content"
   ```
2. 원격 저장소로 Push
   ```bash
   $ git push origin main
   ```

---

## Summary

### 주요 명령어 정리
```bash
# 원격 저장소 복제
$ git clone <URL>
$ git clone <URL> <폴더명>

# Push
$ git push
$ git push -u origin <브랜치명>

# Pull
$ git pull
$ git pull origin <브랜치명>

# Fetch & Merge
$ git fetch origin
$ git merge origin/main
```
