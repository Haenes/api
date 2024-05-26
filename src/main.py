from fastapi import FastAPI

from projects.router import router as projects_router
from issues.router import router as issues_router

app = FastAPI()

app.include_router(projects_router)
app.include_router(issues_router)


# TODO: revert last changes for bugtracker (finally find more elegant solution)
# TODO: add try/except blocks
# TODO: implement authentication
# TODO: add tests