from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.parser import parse_document
from config import settings

router = APIRouter(prefix='/parser', tags=['parser'])

@router.post('/extract')
async def extract_text(file: UploadFile = File(...)):
    file_bytes = await file.read()
    if len(file_bytes) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail='File too large. Maximum allowed size is 5MB.'
        )
    try:
        text = parse_document(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'extracted_text': text}
