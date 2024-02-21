#!/usr/bin/env python3

# from user import User
#
# print(User.__tablename__)
#
# for column in User.__table__.columns:
#     print("{}: {}".format(column, column.type))


# from db import DB
# from user import User
#
# my_db = DB()
#
# user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
# print(user_1.id)
#
# user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
# print(user_2.id)
#
# from db import DB
# from user import User
#
# from sqlalchemy.exc import InvalidRequestError
# from sqlalchemy.orm.exc import NoResultFound
#
#
# my_db = DB()
#
# user = my_db.add_user("test@test.com", "PwdHashed")
# print(user.id)
#
# find_user = my_db.find_user_by(email="test@test.com")
# print(find_user.id)
#
# try:
#     find_user = my_db.find_user_by(email="test2@test.com")
#     print(find_user.id)
# except NoResultFound:
#     print("Not found")
#
# try:
#     find_user = my_db.find_user_by(no_email="test@test.com")
#     print(find_user.id)
# except InvalidRequestError:
#     print("Invalid")
#
# from auth import _hash_password
#
# print(_hash_password("Hello Holberton"))
# from auth import Auth
#
# email = 'me@me.com'
# password = 'mySecuredPwd'
#
# auth = Auth()
#
# try:
#     user = auth.register_user(email, password)
#     print("successfully created a new user!")
# except ValueError as err:
#     print("could not create a new user: {}".format(err))
#
# try:
#     user = auth.register_user(email, password)
#     print("successfully created a new user!")
# except ValueError as err:
#     print("could not create a new user: {}".format(err))

from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))