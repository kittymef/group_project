from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, ForeignKey


#запуск БД
engine = create_async_engine(url='sqlite+aiosqlite:///data.db',
                             connect_args={"timeout": 30})

 
async_session = async_sessionmaker(engine)
 #создание таблицы
class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)

    
#эта таблица пока не используется, будет введена позже,
#для распределения карточек по модулям    
class Module(Base):
    __tablename__ = 'modules'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column()


class Word(Base):
    __tablename__ = 'words'
    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(40))
    translation: Mapped[str] = mapped_column(String(40))
    tg_id: Mapped[int] = mapped_column(BigInteger)
    lang: Mapped[str] = mapped_column(String(40))


#чек корректной работы БД в терминале
async def async_main():
    print("Создание таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы!")