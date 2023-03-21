# This is a sample Python script.
import atexit
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
import pydantic
from typing import Optional
from typing import Type


app = Flask('app')

engine = create_engine('postgresql://appadmin:1234@127.0.0.1:5431/appdb')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all()
def stardata():
    Base.metadata.create_all()
#
class HttpError(Exception):
    #   база для хендлера. действует по шаблону базы
    def __init__(self, status_code: int, description):
        self.status_code = status_code
        self.description = description
 # 3 то для чего создавали базу
@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'description': error.description})
    response.status_code = error.status_code
    return response
#
class CreateAdvUser(pydantic.BaseModel):
    head_adv: str
    autor: str
    @pydantic.validator('autor')
    def validate_nikname(cls, value):
        if len(value) <= 3:
            raise ValueError("Username_is_too_SHORT")
        return value
#
def validate(input_data: dict, validation_model: Type[CreateAdvUser]):
    # засунуто в пост чтобы разрешало постить только тем у кого указан ник и
    # гоолва обьявления
    try:
        model_item = validation_model(**input_data)
        return model_item.dict(exclude_none=True)  #если пришло нан то просто ничего не делай . ненадо писать нан так же.
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())  #делает описание ошибки атвтоматичси
#
class Useradven(Base):

    __tablename__ = 'app_adv'

    id = Column(Integer, primary_key=True, autoincrement=True)
    head_adv = Column(String, index=True, unique=False)
    text_of_adv = Column(String, index=True, unique=False)
    time_create = Column(DateTime, server_default=func.now())
    autor = Column(String, index=True, unique=False)


#
class PatchAdv(pydantic.BaseModel):
    head_adv: Optional[str]
    # опционально может быть а может и не быть автора
    @pydantic.validator('head_adv')
    def validate_nikname(cls, value):
        if len(value) <= 3:
            raise ValueError("head_adv_is_too_SHORT")
        return value


#
def hi():
    json_data = request.json
    print(f"{json_data=}")
    return jsonify({"hi WORLD": "WE HAVE NO PROBLEM"})

#
def get_user(useradven_id: int, session: Session):
    user = session.get(Useradven, useradven_id)
    if user is None:
        return jsonify({'HET': 'TAKOrO userA'})
    return user
#
class UserViev(MethodView):
    def get(self, useradven_id: int):
        with Session() as session:
            user = get_user(useradven_id, session)
            return jsonify({"ID": user.id, "aBTOP" :user.id, "BPEMya": user.time_create.isoformat()})
    #
    def post(self):
        jsn_data = request.json
        # можно делать таким образом.
        if 'text_of_adv' not in jsn_data:
            raise HttpError(409, "HET_avde-texta")
        with Session() as session:
            adver = Useradven(head_adv=jsn_data.get('head_adv'),
                              autor=jsn_data.get('autor'))
            session.add(adver)
            try:
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, "user_K_nPuMEPY_exist")
                #кусок кода такой же но другим способом.
                # response = jsonify({'id': 'user_K_nPuMEPY_exist'})
                # response.status_code = 409
                # return {"id": jsn_data.get("id")}
                 #
            return jsonify({' Объявление внезапно CO3DAHO ABTOPOM': adver.autor})
    #
    def patch(self):
        jsn_data = validate(request.json, PatchAdv)
        return jsonify({"HEDOnuCAHHO": "noka..."})


    #
    def delete(self, useradven_id):
        with Session() as session:
            user = get_user(useradven_id, session)
            session.delete(user)
            session.commit()
            return jsonify({"ID": "DELETED OK "})
        #
# Press the green button in the gutter to run the script.

app.add_url_rule('/', view_func=hi, methods=["GET"])
app.add_url_rule('/adv/<int:useradven_id>/', view_func=UserViev.as_view('userz'), methods=["GET", "DELETE"])
app.add_url_rule('/adv/', view_func=UserViev.as_view('create'), methods=["POST"])

if __name__ == '__main__':
    stardata()
    app.run()
    # app.run(host='0.0.0.0', port=5000)


