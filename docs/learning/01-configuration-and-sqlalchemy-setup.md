# 01. Konfiguratsiya va SQLAlchemy sessiyasini sozlash

Ushbu ta'limiy qo'llanma sun'iy intellekt (AI assistant) tomonidan avtomatlashtirilgan tarzda tayyorlangan bo'lib, repozitoriy egasi va o'rganuvchilar uchun mo'ljallangan.

## Nimalar o'zgardi?
1. `app/config.py` moduli yaratildi. `pydantic-settings` orqali tizim sozlamalari (`Settings`) yaratildi va `DATABASE_URL` kabi parametrlar muhit o'zgaruvchilaridan (`.env` yoki environment) o'qiladigan qilindi.
2. `app/database.py` moduli yaratildi:
   - SQLAlchemy 2 `DeclarativeBase` asosida `Base` klassi e'lon qilindi.
   - Dvigatel (`Engine`) va sessiya ishlab chiqaruvchi (`sessionmaker`) funksiyalari yaratildi.
   - FastAPI yo'llari uchun `get_db()` dependency generatori qo'shildi (har bir so'rov uchun alohida sessiya ochib, ish yakunlangach uni avtomatik yopadi).
   - SQLite test muhitlari uchun `StaticPool` va `foreign_keys=ON` sozlamasi kiritildi.
3. `tests/test_database.py` faylida konfiguratsiya, ma'lumotlar bazasi bilan ishlash, holat o'zgarishi (commit/rollback) va FastAPI dependency override orqali testlar yozildi.
4. `TASKS.md` va `README.md` yangilandi.

## Nima uchun bu o'zgarishlar qilindi?
Loyihaning kelgusi barcha vazifalari (foydalanuvchilar, mahsulotlar, buyurtmalar) ma'lumotlar bazasi bilan mustahkam aloqada ishlaydi. Ishlab chiqarish muhitida PostgreSQL ishlatiladi, biroq avtomatlashtirilgan testlarni tez va mustaqil (tashqi Postgres xizmatiga bog'liq bo'lmagan holda) bajarish uchun xotiradagi (in-memory) SQLite muhiti bilan qulay integratsiya talab etiladi.

## Qanday ishga tushiriladi va tekshiriladi?
Testlarni ishga tushirish uchun quyidagi buyruqni bajaring:
```sh
python -m pytest -q tests/test_database.py
```
Barcha mavjud testlarni tekshirish uchun:
```sh
python -m pytest -q
```

## Loyihalashdagi tanlovlar va kelishuvlar (Tradeoffs)
- **Sinxron sessiya (Session) tanlovi**: Hozirgi bosqichda synchronous SQLAlchemy API tanlandi. Bu boshlang'ich arxitekturani sodda, tushunarli va test qilishni oson qiladi. Kelgusida yuqori yuklamalar uchun `AsyncSession`ga o'tish imkoniyati saqlanib qoladi.
- **Sessiya hayot sikli (Session lifecycle)**: `get_db()` dependency generator orqali ishlaydi (`yield db`). So'rov muvaffaqiyatli tugasa yoki istisno yuz bersa ham, `finally` bloki sessiyani xavfsiz yopilishini ta'minlaydi (connection leak oldi olinadi).
- **SQLite va StaticPool**: Xotiradagi SQLite (`sqlite:///:memory:`) har bir yangi ulanishda bo'sh ma'lumotlar bazasini yaratadi. Bitta test davomida jadval va yozuvlar saqlanib turishi uchun `StaticPool`dan foydalanildi.

## 3 ta texnik intervyu savoli va javoblari

### 1-savol: FastAPI'da ma'lumotlar bazasi sessiyasini Dependency Injection orqali uzatishning afzalligi nimada?
**Javob:** Dependency Injection (masalan, `Depends(get_db)`) orqali har bir HTTP so'roviga o'zining shaxsiy DB sessiyasi beriladi va javob qaytgach, `finally` orqali u yopiladi. Shuningdek, test yozishda `app.dependency_overrides[get_db]` yordamida haqiqiy ma'lumotlar bazasi o'rniga test bazasini (SQLite yoki mock) osonlikcha almashtirish mumkin.

### 2-savol: SQLAlchemy 2.0 da `DeclarativeBase` ishlatish nima uchun `declarative_base()` funksiyasidan afzalroq?
**Javob:** SQLAlchemy 2.0 dan boshlab `class Base(DeclarativeBase)` sintaksisi joriy qilingan. Bu yondashuv zamonaviy Python statik tip tekshirgichlari (mypy, pyright, IDE autocompletion) bilan to'liq va aniq integratsiyani ta'minlaydi hamda kod o'qilishini yaxshilaydi.

### 3-savol: SQLite'da chet el kalitlari (foreign keys) sukut bo'yicha nega ishlamaydi va buni qanday faollashtirish kerak?
**Javob:** SQLite tarixiy sabablarga ko'ra orqaga qaytuvchi moslikni saqlash maqsadida foreign key cheklovlarini sukut bo'yicha tekshirmaydi. SQLAlchemy'da dvigatel ulanishi sodir bo'lganda `event.listens_for(Engine, "connect")` orqali har bir SQLite ulanishiga `PRAGMA foreign_keys=ON` buyrug'ini yuborish orqali buni yoqish zarur.

## Repozitoriy egasi uchun kichik amaliy mashq
`.env` faylini yaratib, unga `DATABASE_URL=sqlite:///./local_dev.db` parametrini yozing. Keyin Python terminalida quyidagi kodni ishga tushirib ko'ring va sozlama to'g'ri o'qilayotganini tekshiring:
```python
from app.config import get_settings
print(get_settings().database_url)
```
