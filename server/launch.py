import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from server.connect.connection import check_port, get_session, make_table  # Import make_table
from server.routes.forum_router import forum_router
from server.routes.comment_router import comment_router
from server.routes.object_history_router import object_history_router

# from connect.connection import check_port, get_session, make_table  # Import make_table
# from routes.forum_router import forum_router
# from routes.comment_router import comment_router
# from routes.object_history_router import object_history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_session()  # Set up connect session
    make_table()  # Create tables
    yield
    logging.warning("... SERVER SHUTTING DOWN... ")


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

# 라우트 등록
app.include_router(forum_router, prefix="/forum")
app.include_router(comment_router, prefix="/comment")
app.include_router(object_history_router, prefix="/gym_count")


def uvicorn_run(PORT):
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    log_config["formatters"]["default"]["fmt"] = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

    check_port(PORT)
    uvicorn.run("server.launch:app",
                host="0.0.0.0",
                port=PORT,
                reload=True,
                log_config=log_config
                # workers=1
                )


if __name__ == "__main__":  # launch without modules
    import json
    CONFIG = json.loads(open("../config.json").read())
    uvicorn_run(PORT=CONFIG["PORT"])
