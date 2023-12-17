from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app import app, db
from flask_login import UserMixin
import enum
import hashlib


class RoleEnum(enum.Enum):
    ADMIN = "admin"
    PASSENGER = "passenger"


class Flight(db.Model):
    __tablename__ = 'flight'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Booking(db.Model):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref='bookings')

    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    flight = relationship("Flight")

    time = Column(DateTime, default=datetime.now())

    @property
    def passenger_name(self):
        return self.user.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        khachhang_user = User(name="Khach hang",
                    username="khachhang",
                    password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                    role=RoleEnum.PASSENGER)

        thanhdat_user = User(name="Thanh Dat",
                              username="thanhdat",
                              password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                              role=RoleEnum.PASSENGER)

        admin_user = User(name="admin",
                    username="admin",
                    password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                    role=RoleEnum.ADMIN)
        db.session.add_all([khachhang_user, thanhdat_user, admin_user])

        f1 = Flight(name="Hà Nội tới TP.HCM", price=2400000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f2 = Flight(name="Nha Trang tới Phú Quốc", price=2500000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f3 = Flight(name="Đà Lạt tới Đà Nẵng", price=2000000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f4 = Flight(name="Cà Mau tới Cần Thơ", price=1500000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f5 = Flight(name="Hải Phòng tới Huế", price=3000000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f6 = Flight(name="Cần Thơ tới Nha Trang", price=1700000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f7 = Flight(name="Cà Mau tới Buôn Ma Thuột", price=2600000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f8 = Flight(name="Hải Phòng tới Huế", price=2900000, image="https://wallpapercave.com/wp/9aungfd.jpg")

        db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8])

        b1 = Booking(user=thanhdat_user, flight=f4)
        b2 = Booking(user=thanhdat_user, flight=f6)
        b3 = Booking(user=thanhdat_user, flight=f5)

        b4 = Booking(user=khachhang_user, flight=f2)
        b5 = Booking(user=khachhang_user, flight=f8)
        b6 = Booking(user=khachhang_user, flight=f5)

        db.session.add_all([b1, b2, b3, b4, b5, b6])

        db.session.commit()
