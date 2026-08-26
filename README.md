# Thailand MSW Dataset — Cleaned & Transformed

ที่มา: `thaimsw_msw_data_2556-2570.xlsx` (กรมควบคุมมลพิษ, thaimsw.pcd.go.th)

## สิ่งที่ทำในขั้น Clean

1. **Rename columns** เป็น snake_case ภาษาอังกฤษ ทั้งหมด — พร้อมต่อ DB/ORM/Python โดยตรง
2. **Trim ช่องว่างเกิน** ในชื่อ สสภ. (พบ `"สสภ.1 (เชียงใหม่ )"` มีช่องว่างก่อนวงเล็บปิด)
3. **แก้ปัญหา NULL ที่กำกวม**: กรุงเทพฯ ไม่มีค่า สสภ. (บริหารเอง ไม่ขึ้นกับสำนักงานภูมิภาค) → เติมเป็นข้อความสื่อความหมายแทนปล่อย NULL เฉยๆ
4. **แก้ปัญหาสำคัญ: ปี 2569–2570 เป็นแถว placeholder ที่ยังไม่มีข้อมูลจริง แต่ค่าดิบเป็น 0 ทั้งหมด**
   ระบบต้นทางใส่ 0 แทนที่จะเว้นว่าง ถ้าไม่แก้ตรงนี้ โมเดล ML/กราฟจะเข้าใจผิดว่า "ปี 2570 ขยะกลายเป็นศูนย์" (การล่มสลายของขยะทั้งประเทศในปีเดียว!) → แปลงเป็น `NaN` และเพิ่ม flag `has_actual_data` ไว้กรองทิ้งง่ายๆ
5. **Data quality checks แบบไม่ลบข้อมูลเงียบๆ**: ตรวจสมการ (นำกลับใช้ + กำจัดถูกต้อง + กำจัดไม่ถูกต้อง ควร ≈ เกิดขึ้น) และตรวจ % รวมควร ≈ 100% แล้วบันทึกรายการที่เบี่ยงเบน >5% ไว้ใน `09_data_quality_flags.csv` เพื่อความโปร่งใส (พบ 2 จุดผิดปกติที่กาญจนบุรี)
6. เก็บ log ความไม่ตรงกันของเว็บต้นทางเอง (`09b_source_mismatch_log.csv`) ไว้แยก ไม่ merge เข้าตารางหลัก

## โครงสร้างฐานข้อมูลเชิงสัมพันธ์ (ดู schema.sql)

```
dim_region ──┐
             ├─< dim_province >─┐
dim_ssp_office ┘                 │
                                  ├─< fact_waste_yearly (grain: province x year)
dim_facility_type ──< fact_facility_count (long/tall — เพิ่มประเภทใหม่ไม่ต้อง ALTER TABLE)
                                  │
                                  ├─< fact_hazardous_waste_province
fact_hazardous_waste_country (grain: year, ระดับประเทศ ไม่ join กับจังหวัด)
data_quality_flags (audit table, อ้างอิงแบบ soft link)
```

**เหตุผลการออกแบบ:**
- แยก `fact_facility_count` เป็น long format แทนที่จะเก็บ 16 คอลัมน์ในตารางเดียว เพราะ (ก) เพิ่มเทคโนโลยีกำจัดขยะแบบใหม่ในอนาคตได้โดยไม่แก้ schema (ข) query "สัดส่วนสถานที่แต่ละประเภท" ง่ายกว่ามาก (ค) เหมาะกับการทำ pivot ตอนสร้าง ML features
- `has_actual_data` flag กันไม่ให้ query ธรรมดาที่ลืมกรองปี 2569-2570 ได้ผลลัพธ์ผิด
- ของเสียอันตรายแยกตารางเพราะ grain/ช่วงปีต่างจากขยะมูลฝอยทั่วไป (2561-2569 vs 2556-2570) — ถ้ารวมตารางเดียวจะเกิด NULL จำนวนมากโดยไม่จำเป็น

## ไฟล์ผลลัพธ์

| ไฟล์ | เนื้อหา |
|---|---|
| 01-03 dim_* | ตารางมิติ: ภาค, สสภ., จังหวัด |
| 04 fact_waste_yearly | ขยะมูลฝอยรายจังหวัด-ปี (ตาราง fact หลัก) |
| 05-06 facility | ประเภท + จำนวนสถานที่กำจัด (long format) |
| 07-08 hazardous | ของเสียอันตราย ระดับประเทศ/จังหวัด |
| 09 data_quality_flags | รายการที่ตรวจพบความผิดปกติของสมการ |
| **10_ml_dataset_province_year.csv** | **ตาราง ML-ready** ที่ join ทุกอย่างแล้ว + engineered features |
| schema.sql | DDL สำหรับสร้างฐานข้อมูลจริง (Postgres syntax, ปรับ MySQL/SQLite ได้ง่าย) |

## Features ที่เพิ่มในชุด ML (ไฟล์ 10)

- `generated_yoy_pct` — % การเปลี่ยนแปลงขยะเทียบปีก่อนหน้า (รายจังหวัด)
- `facility_type_diversity` — จำนวนประเภทเทคโนโลยีกำจัดที่จังหวัดนั้นมีใช้จริง (>0 แห่ง)
- `pct_sites_improper` — สัดส่วนสถานที่กำจัด "ไม่ถูกต้อง" (เทกอง/เผากลางแจ้ง) ต่อสถานที่ทั้งหมด
- `trend_pct_per_year` + `trend_label` — ผลจาก Linear Regression ต่ออนุกรมเวลาของแต่ละจังหวัด (increasing / decreasing / stable)
- `behavior_cluster` + `behavior_cluster_label` — ผลจาก KMeans (k=4) จัดกลุ่มพฤติกรรมการจัดการขยะ โดยใช้สัดส่วน recycle/dispose-correct/dispose-incorrect + ความหลากหลายของโครงสร้างพื้นฐาน (ไม่ใช้ปริมาณขยะดิบ เพื่อไม่ให้ขนาดจังหวัด/กทม. ครอบงำผลลัพธ์)
