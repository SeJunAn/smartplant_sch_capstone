# smartplant_sch_capstone
2025 순천향대 캡스톤디자인 레포지토리

## Image Forwarding API
- `POST /images/upload`: 아두이노 등 외부 장치에서 이미지를 업로드하면 서버가 `IMAGE_FORWARD_URL` 환경변수(기본값 `http://100.122.114.19:8000/images/upload`)로 이미지를 전달합니다.
- 요청 예시:
  ```bash
  curl -X POST http://<server-ip>:8000/images/upload \
       -H "Content-Type: multipart/form-data" \
       -F "image=@/path/to/image.jpg"
  ```
