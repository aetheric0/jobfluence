from fastapi import APIRouter

router = APIRouter(prefix='/payment', tags=['payment'])

@router.post('/charge')
async def charge_user():
    # Placeholder for eventual payment processing logic
    return {'message': 'Payment processing not yet implemented'}
