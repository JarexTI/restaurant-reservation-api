from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.table import Table
from app.schemas.table import TableCreate, TableRead

router = APIRouter()


@router.get('/', response_model=list[TableRead])
async def get_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()


@router.get('/{table_id}', response_model=TableRead)
async def get_table(table_id: int, db: Session = Depends(get_db)):
    table = db.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail='Table not found')
    return table


@router.post('/', response_model=TableRead)
async def create_table(table: TableCreate, db: Session = Depends(get_db)):
    table_name = db.query(Table).filter(
        Table.name == table.name
    ).count()
    if table_name:
        raise HTTPException(
            status_code=404,
            detail='Such a table already exists'
        )

    new_table = Table(
        name=table.name,
        seats=table.seats,
        location=table.location
    )
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table


@router.delete('/{table_id}', response_model=TableRead)
async def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail='Table not found')
    db.delete(table)
    db.commit()
    return table
