# 11주차 — 이미지 분류 프로젝트 (1) · 데이터 수집·전처리·사전학습 모델

## 실습 코드 목록

| 교시 | 파일명 | 내용 | 강의안 |
|------|--------|------|--------|
| 1교시 | `01_image_basics.ipynb` | 이미지 열기·텐서 변환·전처리 파이프라인·CIFAR-10 로드 | [1교시](../../11_week/plane/1교시_이미지_데이터_이해_및_전처리.md) |
| 2교시 | `02_data_augmentation.ipynb` | torchvision transforms 8가지 + 학습/검증 파이프라인 분리 | [2교시](../../11_week/plane/2교시_이미지_데이터_증강.md) |
| 3교시 | `03_pretrained_vit.ipynb` | HuggingFace pipeline + ViT + 본인 사진 분류 + Top-5 해석 | [3교시](../../11_week/plane/3교시_HuggingFace_Vision_사전학습_모델.md) |

## 사전 준비

### 1) 패키지 설치

```bash
pip install torch torchvision transformers datasets pillow matplotlib requests
```

> CPU 환경이면 위 명령 그대로. GPU(CUDA)가 있으면 PyTorch 공식 설치 가이드 참조.

### 2) 샘플 이미지 준비

`sample_images/` 폴더에 다음 파일이 있어야 합니다.
- `dog.jpg`, `cat.jpg`, `landscape.jpg` (강사 준비)
- (선택) `my_phone.jpg` — 학생 본인 사진

자세한 내용은 [`sample_images/README.md`](sample_images/README.md) 참고.

### 3) JupyterLab 실행

```bash
jupyter lab
```
브라우저에서 `BigDataAnalysis/11_week/` 폴더의 노트북을 더블클릭.

## 실습 흐름 (3교시 총 135분 + 쉬는시간 제외)

### 1교시 — 이미지 데이터의 이해 + 전처리 (45분)

| 단계 | 셀 | 내용 | 시간 |
|------|-----|------|------|
| Step 1 | [0]·[1] | matplotlib 한글 + PIL로 이미지 열기 | 5분 |
| Step 2 | [1-1]·[2] | OOM 방지 thumbnail + NumPy 변환 | 5분 |
| Step 3 | [3] | RGB 채널 분리 시각화 | 5분 |
| Step 4 | [4]·[5]·[5-1] | ToTensor / Resize / CenterCrop | 10분 |
| Step 5 | [6] | 표준 전처리 파이프라인 (Resize→ToTensor→Normalize) | 5분 |
| Step 6 | [7]~[10] | CIFAR-10 로드 + 전처리 적용 | 10분 |
| Step 7 | [11]·[12] | 정규화 전/후 비교 + DataLoader 배치 | 5분 |

### 2교시 — 이미지 데이터 증강 (45분)

| 단계 | 셀 | 내용 | 시간 |
|------|-----|------|------|
| Step 1 | [1] | 이미지 + 시각화 함수 준비 | 5분 |
| Step 2 | [2]~[7] | 핵심 증강 6가지 시연 | 15분 |
| Step 3 | [8] | 학습용/검증용 Compose 분리 ★ | 5분 |
| Step 4 | [9] | 같은 사진 12회 적용 — 시각적 충격 | 5분 |
| Step 5 | [10]·[11] | CIFAR-10에 증강 적용 | 5분 |
| Step 6 | [12] | 학생 자율 실습: 내 증강 조합 ★ | 10분 |
| Step 7 | [13] | 증강 퀴즈 | 시간 여유시 |

### 3교시 — HuggingFace Vision 사전학습 모델 (45분)

| 단계 | 셀 | 내용 | 시간 |
|------|-----|------|------|
| Step 1 | [1] | ViT 로드 (첫 실행 시 다운로드 1~3분) | 5분 |
| Step 2 | [2]·[3] | 강사 샘플 분류 + Top-5 시각화 | 10분 |
| Step 3 | [4]·[4-1] | 본인 사진 업로드 / URL 대안 | 5분 |
| Step 4 | [5]·[5-1] | 본인 사진 분류 + Confidence 진단 ★ | 15분 |
| Step 5 | [6] | CIFAR-10 정확도 측정 → 한계 발견 | 5분 |
| Step 6 | [7]·[8] | (선택) Attention 시각화 / 모델 비교 | 5분 |

## 생성/사용 파일

| 파일 | 생성/사용 시점 | 용도 |
|------|-------------|------|
| `~/.cache/huggingface/datasets/uoft-cs___cifar10` | 1교시 셀 [7] | CIFAR-10 자동 캐싱 (재실행 시 즉시 로드) |
| `~/.cache/huggingface/hub/models--google--vit-base-patch16-224` | 3교시 셀 [1] | ViT 모델 가중치 캐싱 (~330MB) |

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `OSError: We couldn't connect to ...` | 인터넷 또는 HF 서버 문제 | 잠시 후 재시도, VPN 끄기 |
| `RuntimeError: CUDA out of memory` | GPU 메모리 부족 | `device=-1` 강제 또는 batch size 축소 |
| `AssertionError: Torch not compiled with CUDA` | GPU 없는데 `device=0` 사용 | `device = 0 if torch.cuda.is_available() else -1` |
| `ValueError: too many dimensions 'str'` | 이미지 경로(str)를 직접 입력 | `Image.open()`으로 먼저 변환 |
| 결과가 모두 같은 라벨 | RGBA 이미지 | `img.convert("RGB")` 호출 |
| `RuntimeError: stack expects each tensor to be equal size` | 배치 안 이미지 크기가 제각각 | `Resize`를 파이프라인에 포함 |
| matplotlib 한글이 깨짐 | 시스템 폰트 미설정 | 노트북 셀 [0] 실행 |
| 첫 셀에서 메모리 폭증 | 휴대폰 원본 사진 그대로 사용 | 1교시 셀 [1-1]의 `thumbnail` 사용 |

## 다음 주차(12주차) 미리보기

11주차에서 발견한 한계 — "ImageNet엔 내가 분류하고 싶은 게 없다" — 를
**파인튜닝(Fine-tuning)** 으로 해결합니다. HuggingFace `Trainer` API로 ViT를
CIFAR-10에 맞게 추가 학습하고, Streamlit으로 이미지 분류 웹 앱까지 완성합니다.
