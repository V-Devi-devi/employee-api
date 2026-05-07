from fastapi import APIRouter, HTTPException, Depends

from schemas.department import DepartmentCreate

from dependencies import get_current_user

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
    dependencies=[Depends(get_current_user)]
)

departments = []

@router.get("/")
def get_departments():

    return departments

@router.post("/")
def create_department(
    department: DepartmentCreate
):

    new_department = {
        "id": len(departments) + 1,
        "name": department.name,
        "location": department.location
    }

    departments.append(new_department)

    return {
        "message":"Department Created",
        "department": new_department
    }

@router.get("/{id}")
def get_department(id:int):

    for department in departments:

        if department["id"] == id:

            return department

    raise HTTPException(
        status_code=404,
        detail="Department Not Found"
    )

@router.put("/{id}")
def update_department(
    id:int,
    department: DepartmentCreate
):

    for dept in departments:

        if dept["id"] == id:

            dept["name"] = department.name

            dept["location"] = department.location

            return {
                "message":"Department Updated",
                "department": dept
            }

    raise HTTPException(
        status_code=404,
        detail="Department Not Found"
    )

@router.delete("/{id}")
def delete_department(id:int):

    for dept in departments:

        if dept["id"] == id:

            departments.remove(dept)

            return {
                "message":"Department Deleted"
            }

    raise HTTPException(
        status_code=404,
        detail="Department Not Found"
    )