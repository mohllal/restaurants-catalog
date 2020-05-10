from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy import event, DDL

Base = declarative_base()


# User table class
class User(Base):
    # Set table name
    __tablename__ = 'user'

    # Map table columns
    name = Column(String(20), nullable=False)
    picture = Column(String(250), nullable=True)
    email = Column(String(250), nullable=False)
    id = Column(Integer, nullable=False, primary_key=True)


# Restaurant table class
class Restaurant(Base):
    # Set table name
    __tablename__ = 'restaurant'

    # Map table columns
    name = Column(String(20), nullable=False)
    description = Column(String(), nullable=False)
    telephone = Column(String(20), nullable=False)
    image = Column(String(), nullable=True)
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description,
            'telephone': self.tel,
            'id': self.id,
            'user id': self.user_id,
        }


# MenuItem table class
class MenuItem(Base):
    # Set table name
    __tablename__ = 'menuItem'

    # Map table columns
    name = Column(String(20), nullable=False)
    description = Column(String(), nullable=False)
    category = Column(String(20), nullable=False)
    price = Column(String(8), nullable=False)
    reviews = Column(Integer, nullable=True, default=0)
    rate = Column(Integer, nullable=True, default=0)
    image = Column(String(), nullable=True)
    id = Column(Integer, nullable=False, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant, backref=backref("menuItem", cascade="all, delete"))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'reviews': self.reviews,
            'rate': self.rate,
            'id': self.id,
            'restaurant id': self.restaurant_id,
            'user id': self.user_id,
        }


# MenuItem table class
class Review(Base):
    # Set table name
    __tablename__ = 'review'

    # Map table columns
    content = Column(String(250), nullable=False)
    rate = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=True, default=func.now())
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref("review", cascade="all, delete"))
    menuItem_id = Column(Integer, ForeignKey('menuItem.id'))
    menuItem = relationship(MenuItem, backref=backref("review", cascade="all, delete"))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'content': self.content,
            'rate': self.rate,
            'date': self.created_date,
            'id': self.id,
            'user id': self.user_id,
            'menu item id': self.menuItem_id,
        }

trigger = DDL(
    """
CREATE TRIGGER aft_insert2 AFTER INSERT ON review
BEGIN
UPDATE menuItem SET rate = ((rate * reviews) + NEW.rate)/(reviews + 1),
reviews = reviews + 1 WHERE NEW.menuItem_id = menuItem.id;
END;
"""
              )

event.listen(
    Review.__table__,
    'after_create',
    trigger.execute_if(dialect='sqlite')
)

engine = create_engine('sqlite:///restaurantmenu.db')
# Add classes as tables to the 'restaurantmenu.db' database
Base.metadata.create_all(engine)
