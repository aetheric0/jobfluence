from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.health import router as health_router
from app.routers.parser import router as parser_router
from app.routers.payment import router as payment_router
from app.routers.demo import router as demo_router

app = FastAPI(
    title='Jobfluence',
    description='Analyze resume vs. job description and provide similarity score + tips',
    version='0.1.0'
)

app.mount('/static', StaticFiles(directory='static'), name='static')

# Include health check
app.include_router(health_router)
app.include_router(parser_router)
app.include_router(payment_router)
app.include_router(demo_router)

#TODO: mount parser and payment routers

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

