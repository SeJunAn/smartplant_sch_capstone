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
- `POST /pump-command`: 웹 UI에서 명령을 등록하면 DB 큐에 저장되고 `command_id`, `issued_at`, `duration_seconds` 정보를 응답합니다.
- `GET /pump-command`: 외부 장비가 호출해 가장 오래된 미사용 명령을 가져가며, 조회 즉시 큐에서 제거됩니다. 대기 명령이 없으면 `{"command_id": null, "water": false, "duration_seconds": 0}` 을 반환합니다.
- `PUMP_COMMAND_ENDPOINT` 환경변수를 설정하면 웹 UI에서 사용할 펌프 명령 등록 URL을 지정할 수 있습니다. 기본값은 `https://rabidly-thioacetic-cortez.ngrok-free.dev/pump-command` 입니다.
