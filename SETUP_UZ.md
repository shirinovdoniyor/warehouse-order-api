# Ishga tushirish

## 1. Fayllarni GitHub'ga yuborish
ZIPni oching. Ichidagi warehouse-order-api papkasida terminal oching.
Git o'rnatilgan bo'lishi kerak. Birinchi push brauzer orqali GitHub loginini so'rashi mumkin.

```sh
git init -b main
git add .
git commit -m "chore: bootstrap AI-assisted warehouse API"
git remote add origin https://github.com/shirinovdoniyor/warehouse-order-api.git
git push -u origin main
```
Agar git identity so'ralsa, o'zingizning ismingiz va GitHub email'ingizni
`git config user.name` hamda `git config user.email` orqali belgilang, keyin commitni qaytaring.
Bu buyruqlar FAQAT hozirgi bo'sh repository uchun. Repo to'lgan bo'lsa force-push qilmang.
ZIPning o'zini GitHub'ga yuklamang: ichidagi fayllar, jumladan .github kerak.

## 2. Kalit va yozish ruxsati
OPENAI_API_KEY allaqachon Settings > Secrets and variables > Actions'da bo'lishi kerak.
Settings > Actions > General > Workflow permissions: Read and write permissions.
Tashkilot cheklovi yoki main himoyasi bo'lsa, workflow to'g'ridan-to'g'ri push qila olmasligi mumkin.

## 3. Birinchi tekshiruv
Actions > Daily AI development > Run workflow > main > Run workflow.
Muvaffaqiyatli run main'ga bitta yangi commit/push qiladi. Keyingi runlar avtomatik.
Rejalashtirilgan workflow faqat default branch'dan ishlaydi: default branch main bo'lsin.

## 4. Nima avtomatik bo'ladi?
Kuniga 5–10 xil vaqt, Toshkent vaqti 08:00–22:00. Har safar bir kichik roadmap vazifasi.
Har push testlardan keyin, docs/learning/ ichiga o'zbekcha tushuntirish bilan.
Kunlik limit muvaffaqiyatli pushlardan hisoblanadi. Qo'lda Run workflow ham limitga kiradi.
Har 20 daqiqadagi reja tekshiruvi AI chaqirmaydi; faqat navbat yetganda AI ishlaydi.
GitHub kechikishi, xatolar yoki tugagan roadmap sabab kamroq push bo'lishi mumkin.
35 ta vazifa bor: taxminan 4–7 faol kun, keyin yangi reja kerak bo'ladi.

## 5. Xarajat va to'xtatish
API uchun foydalanishga qarab xarajat bo'ladi; kalit yaratilishi kredit borligini bildirmaydi.
OpenAI API billing/usage holatini tekshiring. GitHub runner kvotalari ham hisobingizga bog'liq.
Actions > Daily AI development > ... > Disable workflow bilan to'xtating.
Yoki Settings > Secrets and variables > Actions > Variables: AI_ENABLED=false.
Xatolik takrorlansa, xarajat bo'lmasligi uchun workflow'ni vaqtincha o'chiring.

## 6. Xatolar
401: API kalitini tekshiring. 429/insufficient_quota: API limit/billingni tekshiring.
403 push: Actions yozish ruxsati va main branch qoidalarini tekshiring.
No changes / forbidden path / test failed: run logini ko'ring; bunday holatda push qilinmaydi.
main changed: qo'lda o'zgarish bo'lgan; yangi run yangi main'dan boshlaydi.
Roadmap tugasa: reja bosqichi run=false bo'ladi. TASKS.md'ga yangi aniq vazifalar qo'shing.
Bot pushlari alohida CI'ni qayta chaqirmasligi mumkin; publish'dan OLDIN testlar bajariladi.

## Intervyuga tayyorlanish
Har kuni docs/learning/ dagi izohni o'qing, kodni lokal ishlating va mashqni bajaring.
AI yordamida ishlab chiqilganini ochiq ayting; o'zingiz tushunadigan qarorlarni izohlang.
Bot commitlari sizning shaxsiy contribution grafigingizga tushishi kafolatlanmaydi.
