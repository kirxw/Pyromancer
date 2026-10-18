import uvicorn

from config import CONFIG

if __name__ == "__main__":
    uvicorn.run("server:app",host=CONFIG.HOST,port=CONFIG.PORT)