from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import dependencies
from auth_service.dependencies import admin_required
from .database import get_db
from .models import City
from .schemas import CityCreate, CityUpdate, CityResponse

router = APIRouter(
    prefix="/api/cities",
    tags=["cities"],
)


@router.get("", response_model=list[CityResponse])
def list_cities(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    return cities


@router.post(
    "",
    response_model=CityResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_required)],
)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    existing = db.query(City).filter(City.name == city.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La ciudad ya existe",
        )

    new_city = City(name=city.name)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.put(
    "/{city_id}",
    response_model=CityResponse,
    dependencies=[Depends(admin_required)],
)
def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada",
        )

    db_city.name = city.name
    db.commit()
    db.refresh(db_city)
    return db_city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(admin_required)],
)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada",
        )

    db.delete(db_city)
    db.commit()
    return

@router.get("/")
def read_cities(current_user = Depends(dependencies.get_current_user)):
    # ... tu lógica existente ...
    return [{"id": 1, "name": "Example"}]