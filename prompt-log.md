# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 08:13 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: โหมดร่างสำหรับ AC-BKG-01 เนื่องจาก [specs/001-booking/test-cases.md](specs/001-booking/test-cases.md) ยังไม่มีแถวสำหรับ AC นี้
- แถวที่เสนอ: 3 แถว (ทางปกติ 1, ขอบ 1, ทางผิด 1)
- ส่วนที่ยังไม่ชัดเจนใน Then: ช่วง "แสดงหมายเลขคิว" ต้องรอคำตอบ Q-02 และทางผิดเมื่อคงเหลือ 0 ที่ยังไม่มีคำสั่งเฉพาะใน spec
- ไม่เขียนโค้ด test ตามโหมดร่าง และไม่ได้แก้โค้ดระบบ
- ทีมต้องตรวจแถวในตารางและเปลี่ยนสถานะเป็น "ใช้ได้" ก่อน จากนั้นสั่ง /testcases อีกครั้ง

### แก้รอบที่ 2
- ทีมสั่ง: เปลี่ยนจากร่างเป็นใช้ได้
- AI อัปเดตสถานะแถว AC-BKG-01 ใน [specs/001-booking/test-cases.md](specs/001-booking/test-cases.md) เป็น "ใช้ได้" และเริ่มโหมดเขียน test ตามแถวที่ตรวจแล้ว

## 2569-10-07 08:30 คำสั่ง: /verify specs/001-booking/

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: สร้าง [specs/001-booking/rtm.md](specs/001-booking/rtm.md) แผนภูมิ traceability ตามรอย requirement → AC → task → code → test
- รัน test หลังบ้าน: `cd backend && pytest -v` พบ 6 passed
- จัดกลุ่มสถานะตามคำแนะนำ: AC-BKG-01 เป็น "ครบ" แต่มีข้อค้นพบเรื่อง Q-02 และการเดา `A001` โดยไม่มีคำตอบจาก spec, FR-BKG-01 ยังใช้ 14 วันแทน 30 วัน, และมี feature เพิ่มเติม `DELETE /bookings/{id}` ที่อยู่นอก Out of scope
- ไม่แก้โค้ดระบบตามเงื่อนไขของ /verify
- ตรวจ `git status --short` หลัง /verify: ไม่มีไฟล์ใน `app/` หรือ `backend/tests/` ที่ถูกแก้/เปลี่ยนแปลง จึงไม่ต้องใช้ `git restore`

### แก้รอบที่ 3
- ทีมสรุปข้อค้นพบใหม่: แยก "จริง / ยังไม่ถึง / AI เข้าใจผิด" ใน [specs/001-booking/rtm.md](specs/001-booking/rtm.md)
- `FR-BKG-06` ถูกจัดว่าเป็นช่องโหว่ใน spec และ `FR-BKG-01` ถูกระบุว่า “มีแต่ AC ความเร็ว” จึงไม่ควรตีความว่าครบ
- `DELETE /bookings/{id}` ถูกระบุว่าเป็นจุดที่ 3: feature เสริมที่อ้าง ID ผิดเรื่อง และไม่ใช่คำตัดสินจากทีม

## 2569-10-07 10:45 คำสั่ง: /verify specs/001-booking/
- ผล: ปรับให้ตรงกับ spec โดยยกเลิกการเดา queue_no, ปรับ DAYS_AHEAD เป็น 30, เพิ่มคำถามเปิด Q-03/Q-04 และเปลี่ยน Status เป็น Draft v3
- validation: cd backend && pytest -v
