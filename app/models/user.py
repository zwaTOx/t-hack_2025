class UserRepository:
    def __init__(self, db: Session):
        self.db = db