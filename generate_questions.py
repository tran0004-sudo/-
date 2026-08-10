# -*- coding: utf-8 -*-
"""
공부별 학습앱 · 매일 문제 자동 생성기
- 수학: 규칙 기반으로 매일 새 연산 문제 생성(완전 무료, AI 불필요)
- 국어/영어/사회/과학: 교육과정 기반 개념 문제 풀에서 매일 다른 문제 샘플
- 출력: questions.json  (앱의 '클라우드 자동 업데이트' 형식)
정답(a)은 0부터: 0=첫째 보기, 1=둘째 …
"""
import json, random, datetime

# 날짜로 시드 → 매일 다른 문제, 같은 날은 동일
today = datetime.date.today().isoformat()
random.seed(today)

Q = []
def add(subject, g, u, q, c, a, e):
    Q.append({"subject": subject, "g": g, "u": u, "q": q,
              "c": [str(x) for x in c], "a": int(a), "e": e,
              "src": f"매일 자동생성 {today}"})

# ---------- 수학: 4지선다 만들기 ----------
def distract(ans, n=3):
    seen = {ans}; out = []
    cand = [ans+1, ans-1, ans+2, ans-2, ans+3, ans+10, ans-10, ans+5]
    random.shuffle(cand)
    for d in cand:
        if d >= 0 and d not in seen:
            seen.add(d); out.append(d)
        if len(out) >= n: break
    k = 4
    while len(out) < n:
        if ans + k not in seen: seen.add(ans+k); out.append(ans+k)
        k += 1
    return out

def mc(ans):
    opts = [ans] + distract(ans)
    random.shuffle(opts)
    return opts, opts.index(ans)

def make_math(g, unit, n, kinds):
    for _ in range(n):
        k = random.choice(kinds)
        if k == '+':
            cap = 9 if g <= 1 else 50 if g <= 2 else 100 if g <= 3 else 999
            a, b = random.randint(1, cap), random.randint(1, cap); ans, sym = a+b, '+'
        elif k == '-':
            cap = 9 if g <= 1 else 50 if g <= 2 else 100 if g <= 3 else 999
            a = random.randint(2, cap); b = random.randint(1, a); ans, sym = a-b, '-'
        elif k == 'x':
            lim = 9 if g <= 3 else 12
            a, b = random.randint(2, lim), random.randint(2, lim); ans, sym = a*b, '×'
        else:  # ÷
            b = random.randint(2, 9); ans = random.randint(2, 9 if g <= 3 else 12); a = b*ans; sym = '÷'
        opts, ai = mc(ans)
        add('mat', g, unit, f"{a} {sym} {b} = ?", opts, ai, f"{a} {sym} {b} = {ans}!")

make_math(1, '덧셈과 뺄셈', 10, ['+', '-'])
make_math(2, '덧셈과 뺄셈', 6,  ['+', '-'])
make_math(2, '곱셈구구',   8,  ['x'])
make_math(3, '곱셈',       6,  ['x'])
make_math(3, '나눗셈',     8,  ['/'])
make_math(4, '곱셈과 나눗셈', 8, ['x', '/'])
make_math(5, '자연수의 혼합 계산', 6, ['+', '-', 'x'])
make_math(6, '분수의 나눗셈', 6, ['/'])

# ---------- 개념 문제 풀(국어/영어/사회/과학/수학개념) ----------
POOL = [
 # 수학 개념
 ('mat',3,'분수와 소수',"1/4은 전체를 몇 등분한 것 중 하나일까요?",['2','3','4','5'],2,"분모가 4니 4등분!"),
 ('mat',4,'각도',"직각은 몇 도일까요?",['45도','90도','180도','360도'],1,"직각=90도!"),
 ('mat',4,'삼각형',"세 변의 길이가 모두 같은 삼각형은?",['이등변삼각형','정삼각형','직각삼각형','둔각삼각형'],1,"정삼각형!"),
 ('mat',5,'약수와 배수',"12와 18의 최대공약수는?",['3','6','9','36'],1,"6!"),
 ('mat',6,'비와 비율',"전체 200명 중 50명은 몇 %일까요?",['20%','25%','50%','40%'],1,"50/200=25%!"),
 # 국어
 ('kor',3,'반대말',"'크다'의 반대말은?",['작다','높다','길다','넓다'],0,"크다↔작다!"),
 ('kor',3,'국어사전',"낱말의 뜻을 찾을 때 쓰는 책은?",['동화책','국어사전','그림책','일기장'],1,"국어사전!"),
 ('kor',4,'높임 표현',"할머니께서 진지를 ___.",['먹는다','드신다','먹었다','씹는다'],1,"'드신다'로 높여요!"),
 ('kor',5,'속담',"'티끌 모아 ○○' 빈칸에 알맞은 말은?",['태산','바다','구름','모래'],0,"티끌 모아 태산!"),
 ('kor',6,'비유하는 표현',"'사과 같은 내 얼굴'처럼 빗대어 나타내는 것은?",['비유','반복','높임','줄임'],0,"빗대는 것=비유!"),
 # 영어
 ('eng',3,'색깔',"'red'는 무슨 색일까요?",['빨강','파랑','노랑','초록'],0,"red=빨강!"),
 ('eng',3,'과일',"'apple'의 뜻은?",['바나나','사과','포도','딸기'],1,"apple=사과!"),
 ('eng',4,'감정 표현',"'I'm happy.'의 뜻은?",['기쁘다','슬프다','배고프다','피곤하다'],0,"happy=기쁜!"),
 ('eng',5,'be동사',"'She ___ a teacher.' 빈칸에 알맞은 말은?",['am','is','are','be'],1,"She 뒤엔 is!"),
 ('eng',6,'과거 표현',"'yesterday'의 뜻은?",['오늘','어제','내일','지금'],1,"어제!"),
 # 사회
 ('soc',3,'우리나라',"우리나라의 수도는 어디일까요?",['부산','서울','대전','광주'],1,"서울!"),
 ('soc',4,'촌락과 도시',"건물과 사람이 많은 곳은?",['촌락','도시','바다','산'],1,"도시!"),
 ('soc',5,'우리 역사',"훈민정음(한글)을 만든 왕은?",['세종대왕','정조','태종','광개토대왕'],0,"세종대왕!"),
 ('soc',6,'삼권분립',"법을 만드는 국가 기관은?",['국회','법원','정부','학교'],0,"국회!"),
 # 과학
 ('sci',3,'자석의 이용',"자석에 붙는 것은?",['철 클립','유리컵','나무젓가락','고무공'],0,"철에 붙어요!"),
 ('sci',4,'물의 상태 변화',"물이 얼면 무엇이 될까요?",['수증기','얼음','구름','비'],1,"얼음!"),
 ('sci',5,'태양계와 별',"낮에 빛과 열을 주는 별은?",['달','태양','북극성','별똥별'],1,"태양!"),
 ('sci',6,'우리 몸의 구조',"우리 몸에서 숨을 쉬는 기관은?",['위','폐','간','심장'],1,"폐!"),
]
# 매일 개념 문제 절반 정도를 무작위 샘플(항상 다르게)
sample = random.sample(POOL, k=max(12, len(POOL)//2))
for (sub,g,u,q,c,a,e) in sample:
    add(sub,g,u,q,c,a,e)

# ---------- 검증 & 저장 ----------
for it in Q:
    assert 0 <= it['a'] < len(it['c']), it

random.shuffle(Q)
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)

print(f"[{today}] 생성 완료: {len(Q)}문제 → questions.json")
