from fastapi import FastAPI

from database import Base, engine

import models.user
import models.employee
import models.department

from routers import (
    auth,
    employees,
    departments
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():

    return {
        "message":"Employee Management System API"
    }

app.include_router(auth.router)

app.include_router(employees.router)

app.include_router(departments.router)