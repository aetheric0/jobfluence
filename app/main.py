from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.parser import router as parser_router
from app.routers.payment import router as payment_router

app = FastAPI(
    title='Jobfluence',
    description='Analyze resume vs. job description and provide similarity score + tips',
    version='0.1.0'
)

# Include health check
app.include_router(health_router)
app.include_router(parser_router)
app.include_router(payment_router)

#TODO: mount parser and payment routers

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

