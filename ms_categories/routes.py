from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_service.dependencies import admin_required
from .database import get_db
from .models import Category
from .schemas import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"]
)


@router.get("", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_required)]
)
def create_category(
    cat: CategoryCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(Category).filter(Category.name == cat.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría ya existe"
        )

    new_cat = Category(name=cat.name)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat


@router.put(
    "/{cat_id}",
    response_model=CategoryResponse,
    dependencies=[Depends(admin_required)]
)
def update_category(
    cat_id: int,
    cat: CategoryUpdate,
    db: Session = Depends(get_db),
):
    db_cat = db.query(Category).filter(Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    db_cat.name = cat.name
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.delete(
    "/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(admin_required)]
)
def delete_category(
    cat_id: int,
    db: Session = Depends(get_db),
):
    db_cat = db.query(Category).filter(Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    db.delete(db_cat)
    db.commit()
    # 204: sin cuerpo de respuesta
    return
