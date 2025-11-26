from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_service.dependencies import admin_required
from .database import get_db
from .models import PointOfSale
from .schemas import (
    PointOfSaleCreate,
    PointOfSaleUpdate,
    PointOfSaleResponse,
)

router = APIRouter(
    prefix="/api/points-of-sale",
    tags=["points_of_sale"],
)


@router.get("", response_model=list[PointOfSaleResponse])
def list_points(db: Session = Depends(get_db)):
    points = db.query(PointOfSale).all()
    return points


@router.post(
    "",
    response_model=PointOfSaleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_required)],
)
def create_point(pos: PointOfSaleCreate, db: Session = Depends(get_db)):
    new_pos = PointOfSale(
        name=pos.name,
        address=pos.address,
        city=pos.city,
    )
    db.add(new_pos)
    db.commit()
    db.refresh(new_pos)
    return new_pos


@router.put(
    "/{pos_id}",
    response_model=PointOfSaleResponse,
    dependencies=[Depends(admin_required)],
)
def update_point(
    pos_id: int,
    pos: PointOfSaleUpdate,
    db: Session = Depends(get_db),
):
    db_pos = db.query(PointOfSale).filter(PointOfSale.id == pos_id).first()
    if not db_pos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de atención no encontrado",
        )

    db_pos.name = pos.name
    db_pos.address = pos.address
    db_pos.city = pos.city
    db.commit()
    db.refresh(db_pos)
    return db_pos


@router.delete(
    "/{pos_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(admin_required)],
)
def delete_point(pos_id: int, db: Session = Depends(get_db)):
    db_pos = db.query(PointOfSale).filter(PointOfSale.id == pos_id).first()
    if not db_pos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de atención no encontrado",
        )

    db.delete(db_pos)
    db.commit()
    return
