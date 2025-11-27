from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import dependencies, schemas, models, database

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"]
)

# Dependencia para obtener DB
get_db = database.get_db


# --- CRUD ---

@router.get("/", response_model=List[schemas.CategoryResponse])
def list_categories(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: dict = Depends(dependencies.get_current_user)  # Protegido con token
):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories


@router.post(
    "/",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
        cat: schemas.CategoryCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(dependencies.get_current_user)
):
    # Validar si existe
    existing = db.query(models.Category).filter(models.Category.name == cat.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría ya existe"
        )

    new_cat = models.Category(name=cat.name)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat


@router.get("/{cat_id}", response_model=schemas.CategoryResponse)
def get_category(
        cat_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(dependencies.get_current_user)
):
    db_cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return db_cat


@router.put(
    "/{cat_id}",
    response_model=schemas.CategoryResponse
)
def update_category(
        cat_id: int,
        cat: schemas.CategoryUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(dependencies.get_current_user)
):
    db_cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    # Actualizar campos
    if cat.name is not None:
        db_cat.name = cat.name

    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.delete(
    "/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(
        cat_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(dependencies.get_current_user)
):
    db_cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    db.delete(db_cat)
    db.commit()
    return