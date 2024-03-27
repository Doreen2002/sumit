import frappe
from frappe.utils import today, add_days

@frappe.whitelist()
def avg():
	item_code = "Water Small"
	start_date = "2023-01-01"
	end_date = "2024-12-31"
	stock_ledger = frappe.db.get_all("Stock Ledger Entry", filters={"item_code": item_code, "posting_date": [">=", start_date, "<=", end_date]}, fields=["actual_qty", "posting_date"])
	consumption = 0
	for sl in stock_ledger:
		consumption += sl.actual_qty
	return consumption

@frappe.whitelist()
def duration():
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    time_frames = ["1 day", "1 week", "1 month", "1 year"]
    duration = 0
    tf = "1 day"
    time_frame = 0
    if tf == "1 day":
        time_frame = 1
        dura
    elif tf == "1 week":
        duration = frappe.utils.getdate(end_date) - frappe.utils.getdate(start_date)
    elif tf == "1 month":
        duration = frappe.utils.getdate(end_date) - frappe.utils.getdate(start_date)
    elif tf == "1 year":
        duration = frappe.utils.getdate(end_date) - frappe.utils.getdate(start_date)
    else:
        duration


    # duration = frappe.utils.getdate(end_date) - frappe.utils.getdate(start_date)
    return duration

@frappe.whitelist()
def add_days():
    start_date = "2026-01-01"
    end_date = "2023-12-31"
    duration = 365
    new_date = frappe.utils.add_days(frappe.utils.getdate(start_date), -50)
    return new_date.days

@frappe.whitelist()
def get_stock_ledger_entries():
        #get stock ledger entries where quanity change is negative
        ic = "Coffee"
        from_date = "01-12-2023"
        to_date = "31-12-2023"
        entries = frappe.get_list("Stock Ledger Entry",
        filters={
            "item_code": ic,
            "actual_qty": ["<", 0],
            "posting_date": [">=", from_date, "<=", to_date]
            },
        fields=["item_code", "actual_qty"])
        sum_qty = 0
        for entry in entries:
            sum_qty += entry.actual_qty
        duration = frappe.utils.getdate(to_date) - frappe.utils.getdate(from_date)
        average_consumption = abs(sum_qty) / duration.days
        return average_consumption