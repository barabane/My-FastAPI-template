# My FastAPI template 🗺
<p align="center" width="100%">
  <img src="https://github.com/user-attachments/assets/2d3b7abc-261a-4eed-8cce-4457088970ff">
</p>

<b>Routes/API</b> - Презентационный слой приложения<br>
<b>Services</b> - Сервисный слой. Связующее звено между презентационным слоем и слоем доступа к данным<br>
<b>Repositories</b> - Слой доступа к данным. Взаимодействует с базой данных и моделями<br>
<b>Models</b> - Сущности, правила бизнеса

<b>Для передачи данных между слоями приложения используется DTO</b>

## Стэк
- Fastapi = 0.115.0
- Sqlalchemy = 2.0.35
- Uvicorn = 0.32.0
- Asyncpg = 0.30.0
- Ruff = 0.6.9
- Pre-commit = 4.0.1
- Pydantic-settings = 2.5.2
- Alembic = 1.13.3
- Pytest = 8.3.3

