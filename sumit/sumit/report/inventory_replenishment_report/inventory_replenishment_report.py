# Copyright (c) 2024, khan and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from erpnext.stock.report.stock_balance.stock_balance import execute as stock_balance
from datetime import datetime
from frappe.utils import date_diff



def execute(filters=None):
	if not filters: filters = {}
	
	data = []
	coloumns = [
		{
			"fieldname":"warehouse",
			"label": "Warehouse",
			"fieldtype": "Link",
			"options":"Warehouse",
			"width": 200
		},
		{
			"fieldname": "item_name",
			"label": "Item Name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200
		},
		
		{
			"fieldname": "uom",
			"label": "UOM",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "reserved",
			"label": "Reserved",
			"fieldtype": "Float",
			"width": 100
		},

		{
			"fieldname": "balance_stock",
			"label": "Balance Stock",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "avg_consumption",
			"label": "Avg Consumption",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "lead_time",
			"label": "Lead Time",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "custom_safety_time_in_days",
			"label": "Safety Time in Days",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "qty_to_order",
			"label": "Qty To Order",
			"fieldtype": "Float",
			"width": 100
		}
	]
	
	
	

	
	data = get_data(filters)
	return coloumns, data
def date_converter_month(date_str):
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date
	
def get_data(filters):

	data =[]
	wh = filters.get("warehouse")
	item_filters={}
	stock_ledger_filters = {}
	if filters.get("item_group"):
		item_filters["item_group"] = filters.get("item_group")
	if filters.get("item_code"):
		item_filters["item_code"] = filters.get("item_code")	
	if filters.get("from_date") and filters.get("to_date"):
		stock_ledger_filters["posting_date"] = ['between', [filters.get("from_date"), filters.get("to_date")]]
		#stock_ledger_filters["posting_date"] = ['between', [date_converter_month(filters.get("from_date")), date_converter_month(filters.get("to_date"))]]
	# frappe.throw(f"{filters.get("from_date")}")
	# pass
	if wh:
		items = frappe.db.get_list("Item", filters=item_filters, fields=["*"])
		for item in items: 
			stock = 0
			average_consup = 0
			reserved_stock = 0
			qty_to_order = 0
			difference = date_diff(filters.get("to_date") , filters.get("from_date"))
			for s in frappe.db.get_all("Bin", filters={"warehouse": wh, "item_code": item.item_code}, fields=["item_code", "actual_qty",  "stock_uom", "reserved_qty"]):
				stock+=s.actual_qty
			stock_ledger_filters["item_code"] = item.item_code
			stock_ledger_filters["warehouse"] = filters.get("warehouse")
			for r in frappe.db.get_list("Stock Ledger Entry", filters=stock_ledger_filters, fields=["*"]):
				if r.actual_qty < 0:
					average_consup -= r.actual_qty
			avg = average_consup/difference	
			if item.custom_safety_time_in_days > item.lead_time_days:
				reserved_stock = avg * item.custom_safety_time_in_days
			if item.lead_time_days > item.custom_safety_time_in_days:
				reserved_stock = avg * item.lead_time_days
			if stock < reserved_stock: 
				qty_to_order = reserved_stock - stock
			data.append({
					"warehouse": filters.get("warehouse"),
					"item_name": item.item_name,
					"item_code": item.item_code,
					"uom": item.stock_uom,
					"reserved": reserved_stock,
					"balance_stock": stock,
					"avg_consumption": avg,
					"lead_time": item.lead_time_days,
					"custom_safety_time_in_days": item.custom_safety_time_in_days,
					"qty_to_order": qty_to_order
				})
	return data

def get_average_consumption(filters, item_code):
        #get stock ledger entries where quanity change is negative
       
        entries = frappe.get_list("Stock Ledger Entry",
        filters={
            "item_code": "FS/INV/00810",
            "actual_qty": ["<", 0],
            "posting_date": [">=", filters.get("from_date"), "<=", filters.get("to_date")]
            },
        fields=["item_code", "actual_qty"])
        sum_qty = 0
        for entry in entries:
            sum_qty += entry.actual_qty
        duration = frappe.utils.getdate(filters.get("to_date")) - frappe.utils.getdate(filters.get("from_date"))
        average_consumption = abs(sum_qty) / duration.days
        return average_consumption

@frappe.whitelist()
def get_stock_ledger_entries():
	return stock_balance
