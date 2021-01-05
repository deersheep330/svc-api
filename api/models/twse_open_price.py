from sqlalchemy import Column, String, Date, func, Float

from ..db import Base

class TwseOpenPrice(Base):

    __tablename__ = 'twse_open_price'

    symbol = Column(String(16), nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True, server_default=func.sysdate())
    price = Column(Float, nullable=False)

    def __repr__(self):
        return str([getattr(self, c.name, None) for c in self.__table__.c])
