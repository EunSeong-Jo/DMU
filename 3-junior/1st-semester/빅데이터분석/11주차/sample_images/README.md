# sample_images — 강사 준비 샘플 이미지

11주차 1·2·3교시 실습에서 공통으로 사용하는 샘플 이미지 폴더입니다.

## 필요 파일

| 파일명 | 용도 | 권장 사양 |
|--------|------|----------|
| `dog.jpg` | ViT/증강 시연용 강아지 사진 | 가로/세로 1024px 내외, JPEG |
| `cat.jpg` | ViT/증강 시연용 고양이 사진 | 가로/세로 1024px 내외, JPEG |
| `landscape.jpg` | ViT 시연용 풍경 사진 | 가로/세로 1024px 내외, JPEG |
| `my_phone.jpg` | (학생용) 본인 휴대폰 사진 자리 | 학생이 직접 업로드 |

## 강사 준비 가이드

1. 저작권 문제가 없는 이미지를 사용하세요. 추천 소스:
   - [Unsplash](https://unsplash.com) (CC0)
   - [Pixabay](https://pixabay.com) (CC0)
   - [Wikimedia Commons](https://commons.wikimedia.org)

2. 검색 키워드 예시:
   - `dog.jpg` → "golden retriever", "labrador" (ImageNet 1,000 클래스에 잘 매칭됨)
   - `cat.jpg` → "tabby cat", "persian cat"
   - `landscape.jpg` → "mountain", "beach", "forest"

3. 이미지를 다운로드한 뒤 위 파일명으로 이 폴더에 저장합니다.

## 학생용 안내

- 1교시 실습 ①(`Image.open`)에서 본인 휴대폰 사진을 가져와 `my_phone.jpg`로 저장하면 됩니다.
- 3교시 본인 사진 분류 체험에서는 자유롭게 파일명을 정해도 됩니다.

## 빠른 다운로드 스크립트(선택)

준비된 강사용 샘플이 없을 때, 다음 코드를 노트북 첫 셀에 실행하면 Wikimedia Commons에서 공개 이미지를 받아옵니다.

```python
# 강사용 자동 다운로드 (옵션) — sample_images/ 가 비어있을 때 1회 실행
from pathlib import Path
import requests

Path("sample_images").mkdir(exist_ok=True)
urls = {
    "dog.jpg":       "https://upload.wikimedia.org/wikipedia/commons/9/90/Labrador_Retriever_portrait.jpg",
    "cat.jpg":       "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg",
    "landscape.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
}
for name, url in urls.items():
    path = Path("sample_images") / name
    if not path.exists():
        path.write_bytes(requests.get(url, timeout=30).content)
        print(f"saved: {path}")
```
