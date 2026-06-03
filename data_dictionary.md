# BlueStock Mutual Fund Data Warehouse - Data Dictionary

## 1. Dimension Tables

### dim_fund
* **amfi_code** (INTEGER, Primary Key)
* **scheme_name** (TEXT)
* **category** (TEXT)
* **fund_house** (TEXT)

### dim_date
* **date_id** (TEXT, Primary Key)
* **year** (INTEGER)
* **month** (INTEGER)
* **day** (INTEGER)
* **quarter** (INTEGER)

---

## 2. Fact Tables

### fact_nav
* **date_id** (TEXT, Foreign Key)
* **amfi_code** (INTEGER, Foreign Key)
* **nav** (REAL)

### fact_transactions
* **investor_id** (INTEGER)
* **amfi_code** (INTEGER, Foreign Key)
* **transaction_type** (TEXT)
* **amount** (REAL)
* **date_id** (TEXT, Foreign Key)

### fact_performance
* **amfi_code** (INTEGER, Primary Key/Foreign Key)
* **return_1y** (REAL)
* **return_3y** (REAL)
* **return_5y** (REAL)
* **expense_ratio** (REAL)

### fact_aum
* **fund_house** (TEXT)
* **aum_amount** (REAL)
* **date_id** (TEXT, Foreign Key) 