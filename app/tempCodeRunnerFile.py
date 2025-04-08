def get_items_by_query(db: Session, query: str):
    return db.query(models.Item).filter(models.Item.name.ilike(f"%{query}%")).all()