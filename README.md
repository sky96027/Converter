# LaTeX ↔ 한글 수식 변환기 (AST 기반 파서)

이 프로젝트는 LaTeX 수식과 한글 수식 간의 상호 변환을 수행하기 위한 AST(Abstract Syntax Tree) 기반 파서를 구현하는 것을 목표로 합니다.

---

## 요구 사항 정의
    - 한글 xml parse, 한글 수식을 추출.
    - 한글 수식을 LaTeX 으로 변환.
    - LaTeX 을 한글 수식 으로 변환.


## 구성 요소

- **AST 노드 기반 구조**  
  수식 요소를 각 노드(예: `FunctionNode`, `FractionNode`, `RootNode` 등)로 분할하여 변환 로직을 구성

- **토큰화 + 파싱 분리**  
  수식은 먼저 `tokenize()` 함수를 통해 토큰화되고, 이후 `build_ast()`에서 재귀적으로 AST를 구성

- **우선순위 기반 분기 처리**  
  이항 연산자는 연산자 우선순위에 따라 트리 형태로 분기됨 (`+`, `×`, `^` 등)

- **재귀적 구조 처리**  
  각 노드 내부에서 하위 수식을 다시 `build_ast()`를 호출해 처리하는 방식으로 중첩 수식을 다룸

---

## 테스트

현재 다음 수식 유형에 대해 테스트를 구성하고 실행 중입니다:

- 기본 연산: `+`, `-`, `×`, `/`, `^`
- 함수: `sin`, `cos`, `log`, `sqrt`
- 분수, 제곱근, 로그 등 구조적 노드
- 간단한 `cases` 수식에 대한 구조 테스트

> 일부 테스트는 통과하였으며, 복합 구조나 중첩 수식에서는 추가 보완이 필요한 상황입니다.

---
## 현재 구현 범위 및 한계

- 수식 노드별 클래스를 통해 파싱 구조를 나누는 작업은 진행되었음
- 중첩 수식(예: 적분 안에 분수, 함수 안에 괄호 등)에 대한 처리에서 일부 누락된 토큰 처리나 구조 오염 문제가 발생 중
- `CasesNode`, `MatrixNode` 등 일부 노드는 후처리 훅 + 로직 강화 가 필요한 상태

---

## 향후 계획

- 복잡한 구조 ( 적분 내 분수 등 ) 파싱
- 샘플 xml에서 수식만 추출해내는 추출기 구현 ( pyhwpx 이용 )
- 테스트 커버리지 확장 ( 수식마다 한글 -> LaTeX 방향, LaTeX -> 한글 방향 각각 테스트 ) 및 실제 XML 수식 기반 수식 전환 적용
- 실제 추출해낸 수능 수식을 변환 ( 2회전 이상 변환 시에도 수학적 의미를 파괴하지 않게 )

---

## 📁 디렉토리 구조

```bash
.
├── converter/                        # 변환기 핵심 로직이 모여 있는 메인 모듈
│   ├── hooks/                        # 웹 브라우저 개발 환경 설정
│         ├── __init__.py             
│         └── postprocess_hook.py     # 복합 구조 정제
│   └── mapping/                      # 수식 요소 간 매핑 정보
│         ├── __init__.py
│         ├── map.py                  # 각 수식 유형별 쌍방향 매핑 테이블
│         └── precedence.py           # 연산자 우선순위 정의
│   └── nodes/                        # 수식을 구성하는 AST 노드 정의
│         ├── __init__.py
│         ├── angle.py                # 각도 기호 노드 (\angle)
│         ├── arrow.py                # 화살표 기호 노드 (\to, \mapsto 등)
│         ├── bar.py                  # 막대 기호 (\bar)
│         ├── bigop.py                # 시그마, 파이 등 누산 연산자 노드
│         ├── binary_op.py            # +, -, ×, ÷ 등 이항 연산자 노드
│         ├── bracket.py              # 자동 괄호 구조 처리 노드
│         ├── cases.py                # 케이스 분기 수식 노드 (\begin{cases} ...)
│         ├── derivative.py           # 도함수, 미분 표현 노드 (f', ∂ 등)
│         ├── fraction.py             # 분수 표현 노드 (\frac)
│         ├── function.py             # sin, cos 등 기본 함수 표현 노드
│         ├── integral.py             # 적분 표현 노드 (\int)
│         ├── limit.py                # 극한 표현 노드 (\lim)
│         ├── literal.py              # 리터럴 값 (숫자, 변수 등) 노드
│         ├── log.py                  # 로그 표현 노드 (\log)
│         ├── matrix.py               # 행렬 표현 노드 (\begin{matrix})
│         ├── power.py                # 지수 표현 노드 (^)
│         ├── root.py                 # 제곱근, n제곱근 노드 (\sqrt)
│         ├── symbol.py               # 그리스 문자, 수학 기호 등 심볼 표현
│         └── vector.py               # 벡터 및 단위벡터 표현 노드 (\vec, \hat)
│   └── util                          # 공통 유틸리티 함수 및 예외 처리
│         ├── __init__.py
│         ├── exceptions.py           # 사용자 정의 예외 클래스
│         └── string_util.py          # 문자열 파싱 및 변환용 유틸
│   ├── __init__.py
│   ├── base.py                       # ExprNode: 모든 수식 노드의 추상 베이스 클래스
│   └── parser.py                     # 핵심 파서 로직: 수식 → AST로 변환
├── sample                            # 테스트용 입력 파일 및 샘플 수식 모음
│   └── section0.xml                  # 수식 추출후 변환 실행해햐할 실제 샘플
├── tests                             # 유닛 테스트 코드 모음
│   ├── __init__.py                   
│   └── test_parser.py                # AST 및 변환 로직 검증을 위한 테스트
├── README.md
├── __init__.py
├── main.py                           # CLI 진입점
└── setup.py   
```    
---


## 📌 주의 사항

- 이 프로젝트는 구현 진행 중입니다. 일부 수식은 정확히 변환되지 않을 수 있으며, 구조적 보완이 필요한 부분이 존재합니다.
---

## 노션 Report Link
- 과제 개요, 해결 방안, 시행착오 설명 포함
- https://hot-track-f23.notion.site/1cf13a3e1bfc80be9e7ae45db8bc294e
---