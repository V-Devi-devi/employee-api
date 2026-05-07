from pydantic import BaseModel

class DepartmentBase(BaseModel):
    name: str
    location: str = "string"

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int
    class Config:
        from_attributes = True