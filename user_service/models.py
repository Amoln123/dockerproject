from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class UserToken(Base):
    __tablename__ = 'users_tokens'
    __table_args__ = {'schema': 'Rolemaster'}  # Specify schema
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Rolemaster.users.id'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    expires_on = Column(DateTime(timezone=True))

    # Optionally, define a relationship to the User model
    # user = relationship("User", back_populates="tokens")

    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token='{self.token}', created_on='{self.created_on}', expires_on='{self.expires_on}')>"


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'Rolemaster'}  # Specify schema
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    mobile = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    modified_on = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to UserToken
    # tokens = relationship("UserToken", back_populates="user")




    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
