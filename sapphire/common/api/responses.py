from fastapi.responses import FileResponse


class ImageResponse(FileResponse):
    media_type = "image/*"
