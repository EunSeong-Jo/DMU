# 대면수업

## 임시 작업물

### 시험문제
 - git stash

 git init .

 git config --global user.name <name>
 git config --global user.email <email>

 echo 666 > f

 cat f

 git add f

 git commit -m first

 git log --oneline

 git diff

 echo 777 >> f

 git add f

 git commit -m second

 git log --oneline

 echo 888 >> f

 git add f

 # git diff --staged HEAD
 git diff

 echo 999 >> f

 git diff

 git status -s

 git stash
 
 git status -s

 cat f

 # git stash apply
 git stash apply --index

 git status -s

 cat f

 git diff






git diff --staged

git diff HEAD

git diff HEAD^ HEAD






- git reset

--hard
work, stage, git 영역 전부 바꿈

--soft
work, stage 영역은 놔두고 git만 바꿈

--mixed
work 영역은 놔두고 stage, git 영역만 바꿈

git reset --hard HEAD~

git diff

git diff HEAD

git diff --staged

cat f

git reset --hard ORIG_HEAD

cat f

git diff

git diff HEAD

git diff --staged


ox 2개 , 괄호 3개 , 객관식 5개 , 실습 2개