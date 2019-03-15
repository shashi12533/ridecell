# pylint: disable=invalid-name

from config import get_config
from helper import generate_unique_business_id
from helper import get_date_time
from sqlalchemy import (
    orm, create_engine, Column, String, ForeignKey, DateTime, TIMESTAMP, text, Integer
)
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'shashi'

CONFIG = get_config()

Model = declarative_base()
engine = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI,
                       convert_unicode=CONFIG.SQLALCHEMY_CONVERT_UNICODE,
                       pool_recycle=CONFIG.SQLALCHEMY_POOL_CYCLE,
                       echo=CONFIG.SQLALCHEMY_ECHO,
                       connect_args={'timeout': 15})
# Why pool_recycle : http://docs.sqlalchemy.org/en/rel_0_9/dialects/mysql.html#connection-timeouts
_Session = orm.sessionmaker(autocommit=False, autoflush=True, bind=engine)
session = orm.scoped_session(_Session)
Model.metadata.bind = engine
Model.query = session.query_property()

UNIQUE_ID = Column(String(36), primary_key=True, default=generate_unique_business_id)
EXTERNAL_ID_PRIMARY_KEY = Column(String(30), primary_key=True)
NAME = Column(String(255), unique=True)
NAME_NULLABLE_FALSE = Column(String(255), unique=True, nullable=False)
AUTO_INCREMENTAL_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

PRODUCT_ID_FOREIGN_KEY = Column(String(36), ForeignKey('product.id'))
USER_ID_FOREIGN_KEY = Column(String(36), ForeignKey('user.id'))
CART_ID_FOREIGN_KEY = Column(String(36), ForeignKey('cart.id'))
CURRENCY_CODE_FOREIGN_KEY = Column(String(3), ForeignKey('currency.code'))
COUNTRY_CODE_FOREIGN_KEY = Column(String(3), ForeignKey('country.code'))
MERCHANT_ID_FOREIGN_KEY = Column(String(36), ForeignKey('merchant.id'))
CART_ITEM_ID_FOREIGN_KEY = Column(String(36), ForeignKey('cart_items.id'))
EXTERNAL_ID = Column(String(30), nullable=True)

PRODUCT_ID_FOREIGN_KEY_NULLABLE_FALSE = Column(String(36), ForeignKey('product.id'), nullable=False)
USER_ID_FOREIGN_KEY_NULLABLE_FALSE = Column(String(36), ForeignKey('user.id'), nullable=False)
CART_ID_FOREIGN_KEY_NULLABLE_FALSE = Column(String(36), ForeignKey('cart.id'), nullable=False)



CREATED_ON = Column(DateTime, default=get_date_time)
CREATED_ON_WITH_SERVER_DEFAULT = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
MODIFIED_ON = Column(TIMESTAMP, nullable=False, default=get_date_time,
                     server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
DELETED_ON = Column(DateTime)

BOOLEAN_TRUE = Column(TINYINT(1), default=1, nullable=False)
BOOLEAN_FALSE = Column(TINYINT(1), default=0, nullable=False)

