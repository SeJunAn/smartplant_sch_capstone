import os
from typing import Optional

import requests
from fastapi import APIRouter, HTTPException, UploadFile, File, status

FORWARD_URL = os.getenv(
    "IMAGE_FORWARD_URL",
    "https://lowell-nonsuccessful-covetingly.ngrok-free.dev/upload",
)

router = APIRouter(tags=["images"])


def _post_image_to_remote(
    file: UploadFile,
    forward_url: str,
    timeout: Optional[float] = None,
) -> requests.Response:
    file.file.seek(0)
    files = {
        "file": (
            file.filename or "upload.jpg",
            file.file,
            file.content_type or "application/octet-stream",
        )
    }

    return requests.post(forward_url, files=files, timeout=timeout)


async def _forward_single_image(image: UploadFile = File(...)):
    try:
        response = _post_image_to_remote(image, FORWARD_URL, timeout=10)
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to forward image: {exc}",
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Forward server responded with status {response.status_code}",
        )

    return {"detail": "Image forwarded successfully."}


@router.post("/images/upload", status_code=status.HTTP_202_ACCEPTED)
async def forward_image(image: UploadFile = File(...)):
    return await _forward_single_image(image)


@router.post(
    "/upload",
    status_code=status.HTTP_202_ACCEPTED,
    include_in_schema=False,
)
async def forward_image_legacy(image: UploadFile = File(...)):
    return await _forward_single_image(image)
