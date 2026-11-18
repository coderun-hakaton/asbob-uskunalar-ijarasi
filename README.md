# Asbob ijarasi

Django asosidagi, SQLite ma'lumotlar bazasida ishlaydigan asbob-uskunalar ijara katalogi. Katalog va ijara so'rovlari Django admin panelidan boshqariladi.

## Ishga tushirish (Windows)

```powershell
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```

Sayt `http://127.0.0.1:8000/` manzilida ochiladi. Dastlabki 6 ta jihoz migratsiya vaqtida bazaga qo'shiladi.

Admin yaratish va panelga kirish:

```powershell
py manage.py createsuperuser
```

Admin panel: `http://127.0.0.1:8000/admin/`.

## Testlar

```powershell
py manage.py test
```

Mahsulotlar va ijara so'rovlari `db.sqlite3` faylida saqlanadi. Ishlab chiqarish muhitida `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0` va `DJANGO_ALLOWED_HOSTS` qiymatlarini muhit o'zgaruvchilari orqali belgilang.

## Railway'ga joylash

Loyiha Railway uchun `railway.toml` orqali sozlangan. Railway'da loyiha yaratib, PostgreSQL servis qo'shing va Django servisiga GitHub repozitoriyni ulang. PostgreSQL uchun `DATABASE_URL` ni servisdagi `DATABASE_URL` o'zgaruvchisiga reference qiling.

Django servisining variables bo'limida quyidagilarni belgilang:

- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` — maxfiy, tasodifiy kalit; uni repozitoriyga yozmang.
- `DJANGO_ALLOWED_HOSTS` — Railway bergan domen, masalan `your-app.up.railway.app`.

Deploy vaqtida migratsiyalar bajariladi, statik fayllar WhiteNoise orqali tarqatiladi. Birinchi deploy'dan so'ng Railway shell'da `python manage.py createsuperuser` buyrug'i bilan production adminini alohida, kuchli parol bilan yarating. Lokal `admin/admin` hisobidan production'da foydalanmang.

Windows'da maxfiy kalit yaratish:

```powershell
py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
