# StemX: AI-based Audio Separation Tool

**StemX** is an open-source solution that provides high-fidelity audio separation powered by Artificial Intelligence. It supports vocal extraction, instrumental (MR) creation, and 4-track stem separation.

---

## System Requirements

| Specification | Minimum | Recommended |
| :--- | :--- | :--- |
| **RAM** | 4GB+ | 8GB+ |
| **GPU** | NVIDIA GTX 1650 or higher | CUDA-enabled GPU |
| **OS** | Windows 10/11 (64-bit) | Latest updates recommended |

---

## Getting Started (English)

1. **Prepare Files**: Place the audio files you want to separate into the `input` folder.
2. **Run Program**: Execute `StemX_extractor.exe`.
3. **Select Mode**: Choose your desired separation mode following the on-screen instructions.
4. **Check Results**: Once finished, find your processed files in the `output` folder.

> **Note**: An **internet connection** is required during the first run to download AI models and essential modules. After the initial setup, it can be used offline.

---

## Important Notes

* **FFmpeg Required**: `ffmpeg.exe` must be present in the program folder. The program will not function without it.
* **Python Environment**: If Python 3.10 is not detected, the system will attempt an automatic installation. A **PC reboot** is required after installation for proper operation.
* **Compatibility**: This program is optimized for **Python 3.10.11** to prevent bugs found in newer versions (3.14+).

---

## Update Log

* **v1.2 (Current)**: Added multilingual support (Auto-detects EN/KO), improved system stability.
* **v1.1**: Project renamed to StemX, expanded separation modes (Vocals / Inst / 4-Track).

---
---

## 시작하기 (Korean)

1. **파일 준비**: `input` 폴더에 분리하고자 하는 오디오 파일을 넣습니다.
2. **프로그램 실행**: `StemX_extractor.exe`를 실행합니다.
3. **모드 선택**: 화면 안내에 따라 원하는 분리 모드를 선택합니다.
4. **결과 확인**: 작업이 완료되면 `output` 폴더에서 결과물을 확인하세요.

> **참고**: 첫 실행 시 AI 모델 및 필수 모듈 구동을 위해 **인터넷 연결**이 필요합니다. 환경 설정 완료 후에는 오프라인에서도 작동합니다.

---

## 주요 안내 사항

* **FFmpeg 필수**: 프로그램 폴더 내에 `ffmpeg.exe`가 반드시 존재해야 합니다.
* **파이썬 환경**: Python 3.10이 없는 경우 자동 설치를 시도하며, 설치 후에는 반드시 **PC를 재부팅**해야 합니다.
* **지원 규격**: .mp3, .m4a, .wav, .flac 등 주요 오디오 확장자를 지원하며, 1kB 이하의 파일은 제외됩니다.

---

## 📄 License
This project is licensed under the **MIT License**.
