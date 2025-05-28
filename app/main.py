from fastapi import FastAPI
from app.routers.health import router as health_router

app = FASTAPI(
    title='Jobfluence',
    description='Analyze resume vs. job description and provide similarity score + tips',
    version='0.1.0'
)

# Include health check
app.include_router(health_router)

#TODO: mount parser and payment routers

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

