from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.api.configs.config import Config

engine = create_engine(Config.fetch('dataBaseUrl'), echo=False) # Движок
SessionLocal = sessionmaker(bind=engine) # Фабрика сессий

"""engine.py — это «подключение» к базе данных. 
Он создает движок (engine) и фабрику сессий (sessionmaker), через которые тесты общаются с БД."""