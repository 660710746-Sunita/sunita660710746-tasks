# RTM: จองคิวตรวจสุขภาพ (Booking)

อ้างอิง: spec.md SPEC-BKG-001 Draft v2, plan.md v1, tasks.md, test-cases.md

## สรุปผลตรวจ

- รัน test หลังบ้านแล้ว: `cd backend && pytest -v` -> 6 passed
- มี test หน้าเว็บอยู่ 1 ตัวใน `frontend/src/__tests__/setup.test.jsx` และ pass
- อย่างไรก็ตาม มี requirement หลายข้อที่ยังไม่ถึงหรือมีช่องโหว่ตาม spec
- ข้อค้นพบหลัก: `FR-BKG-01` ใช้ช่วงเวลา 14 วัน แทน 30 วัน, `FR-BKG-02/03/05` ยังไม่มี implementation, `Q-02` ถูกเดาเป็นรูปแบบ `A001` โดยไม่รอคำตอบจริง, และ `CON-TECH-01`/`DOM-PDPA-01`/`IF-NOT-01` ยังไม่ถูก enforce ในโค้ดจริง

## ตามรอยไปข้างหน้า

| ID | AC | task | โค้ดที่ทำให้เป็นจริง | test ที่ตรวจจริง | สถานะ | ข้อค้นพบ |
|---|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | `backend/app/slots/router.py`, `backend/app/slots/service.py` | `backend/tests/test_AC_BKG_05.py` -> pass | ช่องโหว่ | โค้ดใช้ `DAYS_AHEAD = 14` ซึ่งไม่ตรงกับ spec ว่า "ภายใน 30 วันข้างหน้า" และไม่มี test ตรวจ 30 วันจริง |
| FR-BKG-02 | AC-BKG-02 | T-04 (พร้อมทำ) | ไม่มีโค้ดจริงที่ตรวจ "มีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน" | ไม่มี | ยังไม่ถึง | ใน `backend/app/booking/service.py` มีเฉพาะการตรวจ `remaining <= 0` ไม่ได้ตรวจคนเดียวกันมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน |
| FR-BKG-03 | AC-BKG-03 | T-05 (พร้อมทำ) | ไม่มีโค้ดจริงสำหรับแจ้ง "ช่วงเวลาเต็ม" และแสดง 3 ตัวเลือกใกล้เคียง | ไม่มี | ยังไม่ถึง | มีเพียง API `/bookings` ที่ตอบ 409 เมื่อเต็ม แต่ไม่มี logic เสนอช่วงที่ว่าง 3 ตัวเลือกตามวันเดียวกัน/วันถัดไป และไม่มีหน้าจอที่แสดง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | `backend/app/booking/router.py`, `backend/app/booking/service.py` | `backend/tests/test_AC_BKG_01.py` -> pass | ช่องโหว่ | โค้ดออกหมายเลขคิวแบบ `A001` โดยเดาเอง แม้ spec ระบุ Q-02 ยังไม่ได้คำตอบ; จึงใช้คำตอบที่ไม่มาจาก spec |
| FR-BKG-05 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มีโค้ดส่งข้อความซ้ำหรือ queue retry | ไม่มี | ยังไม่ถึง | ไม่มี `backend/app/notify/queue.py` หรือ logic ที่บันทึกรายการค้างส่งและแทงซ้ำภายใน 5 นาที |
| FR-BKG-06 | ไม่มี AC | T-10 (พร้อมทำ) | `backend/app/slots/router.py` / `list_available_slots(..., package_code=...)` | ไม่มี | ช่องโหว่ | FR นี้มีโค้ด backend เบื้องต้น แต่ spec ระบุไม่มี AC อย่างชัดเจน จึงเป็นช่องโหว่ด้าน spec/traceability และไม่มี test หน้าจอจริง |
| NFR-PERF-01 | AC-BKG-05 | T-02 | `backend/app/slots/service.py` | `backend/tests/test_AC_BKG_05.py` -> pass | ครบ | test เป็นแบบย่อส่วน 200 request เทียบกับ 200 คนจริง และ p95 < 2s ถูกตรวจจริง |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มีการตั้งค่า TLS/HTTPS หรือ security middleware ในโค้ด | ไม่มี | ยังไม่ถึง | ไม่พบการใช้ TLS 1.2+ หรือการบังคับ HTTPS ใน FastAPI app |
| NFR-REL-02 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มี implementation retry queue | ไม่มี | ยังไม่ถึง | ไม่มีการจัดการข้อความที่ส่งไม่สำเร็จและไม่มีกลไกส่งซ้ำภายใน 5 นาที |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มี UX usability test ต่อ 8/10 คน | ไม่มี | ยังไม่ถึง | spec ระบุเพียงสถิติผู้ใช้ใหม่ แต่ไม่มีการทดสอบจริงหรืออุปกรณ์วัด |
| CON-TECH-01 | ไม่มี AC | T-01 | `backend/app/config.py`, `backend/app/db/session.py` | `backend/tests/test_T01_schema.py` -> pass | ช่องโหว่ | โค้ด default เป็น `sqlite:///./dev.db` หากไม่มี `DATABASE_URL` จะไม่ใช่ PostgreSQL ตาม spec; เป็นค่า dev fallback ที่ขัดกับ constraint |
| DOM-PDPA-01 | AC-BKG-06 | T-08 (พร้อมทำ) | ไม่มี middleware audit log | ไม่มี | ยังไม่ถึง | มีตาราง `audit_logs` ในโมเดล แต่ไม่มีฟังก์ชันบันทึก log ทุก request ที่เข้าถึงข้อมูลการจอง |
| IF-IDP-01 | ไม่มี AC ผู้ต้องการ | T-03 | `backend/app/auth/idp.py` | ไม่มี test ที่ตรวจ token ระดับจริง แต่ `test_AC_BKG_01.py` ใช้ header AUTH | ครบ | API ตรวจ header แบบ `******` และ 401 ถ้ายังไม่ยืนยันตัวตน ทำตาม precondition ที่ spec กำหนด |
| IF-HIS-01 | ไม่มี AC | T-09 (พร้อมทำ) | ไม่มี HIS client และไม่มีฟังก์ชันค้น HN จากเลขบัตรประชาชน | ไม่มี | ยังไม่ถึง | ไม่มี `backend/app/his/client.py` หรือ logic ที่อ้างอิง HN จาก HIS และไม่เก็บ national_id ตาม constraint |
| IF-NOT-01 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มี asynchronous notification queue | ไม่มี | ยังไม่ถึง | `create_booking` ไม่ได้ใส่ข้อความลง queue และไม่แยกส่งข้อความแบบ async ตาม spec |

## ข้อค้นพบตามรอยย้อนกลับ

### 1) จริง (Actual findings)
- `backend/app/slots/service.py` ใช้ `14` วันแทน 30 วัน จาก `FR-BKG-01` ซึ่งไม่ตรงกับ spec ที่ระบุ “ภายใน 30 วันข้างหน้า”
- `backend/app/booking/service.py` เคยมี bug จริงที่ยอมให้จองได้เมื่อ `remaining == 0` ก่อนถูกแก้เป็น `remaining <= 0`
- `CON-TECH-01`: default database ใน `backend/app/config.py` เป็น SQLite เมื่อไม่มี `DATABASE_URL` ซึ่งขัดกับ constraint ที่ต้องใช้ PostgreSQL
- `Q-02` ยังไม่มีคำตอบจาก spec และ `queue_no` ที่ใช้ `A001` เป็นการเดาโดย AI/นักพัฒนา ไม่ใช่ requirement ที่ได้จากทีม
- `backend/app/booking/router.py` มี `DELETE /bookings/{booking_id}` ซึ่งเป็น feature เสริมที่อยู่นอก scope “ยกเลิก / เลื่อนคิว (UC-02)” และไม่มี requirement/AC ที่รองรับ

### 2) ยังไม่ถึง (Not yet implemented)
- `FR-BKG-02`: ยังไม่มี logic ตรวจว่าผู้รับบริการมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน และแสดงหมายเลขคิวเดิม
- `FR-BKG-03`: ยังไม่มี logic แจ้ง “ช่วงเวลาเต็ม” และเสนอช่วงว่าง 3 ตัวเลือกภายในวันเดียวกันและวันถัดไป 1 วัน
- `FR-BKG-05` / `NFR-REL-02`: ยังไม่มี retry queue หรือการส่งซ้ำข้อความเมื่อส่งไม่สำเร็จ
- `DOM-PDPA-01`: ยังไม่มี audit log ทุก request ที่เข้าถึงข้อมูลการจอง
- `IF-HIS-01`: ยังไม่มี HIS lookup และไม่มีการควบคุมไม่ให้เก็บเลขบัตรประชาชน
- `IF-NOT-01`: ยังไม่มี asynchronous notification queue
- `NFR-SEC-01`: ยังไม่มี TLS/HTTPS enforcement ใน FastAPI app

### 3) AI เข้าใจผิด / ตีความผิด (Misinterpretation)
- `FR-BKG-06` เป็นช่องโหว่ใน spec: มีโค้ด backend เบื้องต้น แต่ spec ไม่มี AC ที่ระบุชัดเจนว่าต้องคำนวณช่วงว่างใหม่เมื่อเปลี่ยนแพ็กเกจ ดังนั้นการกล่าวว่า “FR-BKG-06 ทำแล้ว” เป็นการตีความเกิน scope และไม่ใช่การตัดสินใจจากทีม
- `FR-BKG-01` มีเพียง `AC-BKG-05` ซึ่งเป็น AC ด้านความเร็ว (`NFR-PERF-01`) ไม่ใช่ AC ของฟังก์ชันหลัก “แสดงช่วงเวลาว่าง และจำนวนที่นั่งคงเหลือภายใน 30 วัน” ดังนั้น การสรุปว่า FR-BKG-01 ครบโดยอ้างจากความเร็วเท่านั้นเป็นการเข้าใจผิด
- จุดที่ 3: `DELETE /bookings/{booking_id}` ไม่ควรเชื่อมกับ `FR-BKG-04` หรือบอกว่า “ทีมตัดสินใจเอง” เพราะ spec ระบุชัดว่า “ยกเลิก / เลื่อนคิว (UC-02)” อยู่ใน Out of scope และไม่มี requirement/AC ที่รองรับฟีเจอร์นี้
- สรุป: ใน `rtm.md` ถ้ามีข้อความว่า “ทีมตัดสินใจเอง” ต้องไม่ถูกใช้กับกรณีนี้ เพราะความจริงคือ AI เพิ่มฟีเจอร์นอก scope โดยไม่มีคำสั่งหรือคำตอบจาก spec

## ข้อสรุปด้านคุณภาพของ test

- `backend/tests/test_AC_BKG_01.py` มี test ที่ตรวจจริงและผ่าน: บันทึก booking, decrement remaining, 409 เมื่อเต็ม
- แต่มี AC ที่ยังไม่มี test ในโค้ด:
  - AC-BKG-02
  - AC-BKG-03
  - AC-BKG-04
  - AC-BKG-06
- ใน `specs/001-booking/test-cases.md` มีการย้ายแถว AC-BKG-01 เป็น "ใช้ได้" และมี test จริงแล้วจึงเป็น “ครบ” สำหรับ AC-BKG-01 อย่างไรก็ตาม AC อื่น ๆ ยังค้างอยู่

## สรุปความพร้อม

- ครบตาม spec: บางส่วนใน `FR-BKG-01` (backend ให้ข้อมูลช่วงเวลา), `FR-BKG-04` (booking callback) และ `IF-IDP-01` (authentication stub)
- ยังไม่ถึง: `FR-BKG-02`, `FR-BKG-03`, `FR-BKG-05`, `NFR-REL-02`, `DOM-PDPA-01`, `IF-HIS-01`, `IF-NOT-01`
- มีช่องโหว่/ข้อผิดพลาดที่ต้องแก้ก่อนรับรอง: `FR-BKG-01` (30 วันผิด), `CON-TECH-01` (default SQLite), `Q-02` (formatted queue number guessed), `DELETE /bookings/{id}` เป็น feature นอก scope
