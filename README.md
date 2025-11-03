# smartplant_sch_capstone
2025 순천향대 캡스톤디자인 레포지토리

## Image Forwarding API
- `POST /images/upload`: 아두이노 등 외부 장치에서 이미지를 업로드하면 서버가 `IMAGE_FORWARD_URL` 환경변수(기본값 `https://lowell-nonsuccessful-covetingly.ngrok-free.dev/upload`)로 이미지를 전달합니다.
- 요청 예시:
  ```bash
  curl -X POST http://<server-ip>:8000/images/upload \
       -H "Content-Type: multipart/form-data" \
       -F "image=@/path/to/image.jpg"
  ```

## Pump Command API
- `POST /pump-command`: 웹 UI에서 요청하면 펌프 명령이 등록되고, 현재 서버 시간과 함께 큐에 저장됩니다.
- `GET /pump-command`: 외부 장비가 호출해 대기 중인 명령을 가져가며, 한 번 조회되면 큐에서 제거됩니다. 대기 명령이 없으면 `{"water": false, "duration_seconds": 0}` 을 반환합니다.
