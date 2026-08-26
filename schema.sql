-- =========================================================
-- Thailand MSW (Municipal Solid Waste) — Relational Schema
-- Design: star-ish schema, dims เล็ก + fact ยาว (long) สำหรับ facility
-- เหมาะทั้งกับเว็บ (query ง่าย, join ตรงไปตรงมา) และ ML (aggregate ทำ view ต่อได้)
-- =========================================================

CREATE TABLE dim_region (
    region_id   SERIAL PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE dim_ssp_office (
    ssp_office_id   SERIAL PRIMARY KEY,
    ssp_office_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE dim_province (
    province_code   INTEGER PRIMARY KEY,      -- รหัสจังหวัดทางการ
    province_name   VARCHAR(100) NOT NULL,
    region_id       INTEGER NOT NULL REFERENCES dim_region(region_id),
    ssp_office_id   INTEGER REFERENCES dim_ssp_office(ssp_office_id)
);

CREATE TABLE dim_facility_type (
    facility_type_id     SERIAL PRIMARY KEY,
    facility_type_code   VARCHAR(50) NOT NULL UNIQUE,
    facility_type_name_th VARCHAR(150) NOT NULL
);

-- ตารางหลัก: 1 แถว = 1 จังหวัด x 1 ปี
CREATE TABLE fact_waste_yearly (
    province_code                       INTEGER NOT NULL REFERENCES dim_province(province_code),
    year_be                             SMALLINT NOT NULL,
    has_actual_data                     BOOLEAN NOT NULL DEFAULT TRUE,
    generated_ton_day                   NUMERIC(12,2),
    recycled_ton_day                    NUMERIC(12,2),
    disposed_correct_ton_day            NUMERIC(12,2),
    disposed_incorrect_ton_day          NUMERIC(12,2),
    residual_ton                        NUMERIC(14,2),
    pct_recycled                        NUMERIC(5,2),
    pct_disposed_correct                NUMERIC(5,2),
    pct_disposed_incorrect              NUMERIC(5,2),
    generated_million_ton_yr            NUMERIC(10,4),
    recycled_million_ton_yr             NUMERIC(10,4),
    disposed_correct_million_ton_yr     NUMERIC(10,4),
    disposed_incorrect_million_ton_yr   NUMERIC(10,4),
    residual_million_ton_yr             NUMERIC(10,4),
    PRIMARY KEY (province_code, year_be)
);

-- long format: เพิ่มประเภทสถานที่กำจัดใหม่ในอนาคตได้โดยไม่ต้อง ALTER TABLE
CREATE TABLE fact_facility_count (
    province_code     INTEGER NOT NULL,
    year_be           SMALLINT NOT NULL,
    facility_type_id  INTEGER NOT NULL REFERENCES dim_facility_type(facility_type_id),
    site_count        INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (province_code, year_be, facility_type_id),
    FOREIGN KEY (province_code, year_be) REFERENCES fact_waste_yearly(province_code, year_be)
);

CREATE TABLE fact_hazardous_waste_country (
    year_be                       SMALLINT PRIMARY KEY,
    hw_generated_ton              NUMERIC(14,2),
    hw_weee_ton                   NUMERIC(14,2),
    hw_other_ton                  NUMERIC(14,2),
    hw_collected_total_ton        NUMERIC(14,2),
    hw_managed_correct_total_ton  NUMERIC(14,2)
    -- คอลัมน์ breakdown ช่องทางอื่นๆ ดูไฟล์ 07_fact_hazardous_country.csv
);

CREATE TABLE fact_hazardous_waste_province (
    province_code   INTEGER NOT NULL REFERENCES dim_province(province_code),
    year_be         SMALLINT NOT NULL,
    hw_generated_ton   NUMERIC(12,2),
    hw_collected_ton   NUMERIC(12,2),
    hw_disposed_ton    NUMERIC(12,2),
    PRIMARY KEY (province_code, year_be)
);

-- transparency: ไม่ลบข้อมูลที่ต้นทาง (คพ.) ให้ค่าไม่ตรงกันเอง แต่บันทึกไว้ตรวจสอบย้อนหลังได้
CREATE TABLE data_quality_flags (
    id              SERIAL PRIMARY KEY,
    province_name   VARCHAR(100),
    year_be         SMALLINT,
    issue           VARCHAR(100),
    detail          TEXT
);

-- =========================================================
-- ML FEATURE VIEW (ตัวอย่าง) — ต่อยอดจาก fact tables ด้านบน
-- ใน production แนะนำ materialize เป็นตาราง/feature store จริง
-- =========================================================
-- CREATE VIEW v_ml_features AS
-- SELECT f.province_code, p.province_name, r.region_name, f.year_be,
--        f.generated_ton_day, f.pct_recycled, f.pct_disposed_correct, f.pct_disposed_incorrect,
--        LAG(f.generated_ton_day) OVER (PARTITION BY f.province_code ORDER BY f.year_be) AS prev_year_generated
-- FROM fact_waste_yearly f
-- JOIN dim_province p USING (province_code)
-- JOIN dim_region r USING (region_id)
-- WHERE f.has_actual_data;
