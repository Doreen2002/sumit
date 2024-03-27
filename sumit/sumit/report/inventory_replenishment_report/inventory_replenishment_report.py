# Copyright (c) 2024, khan and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
					



def execute(filters=None):
	if not filters: filters = {}
	
	data = []
	coloumns = [
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
			"fieldname": "item_group",
			"label": "Item Group",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "uom",
			"label": "UOM",
			"fieldtype": "Data",
			"width": 60
		},
		{
			"fieldname": "reserved",
			"label": "Reserved",
			"fieldtype": "Data",
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
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "lead_time",
			"label": "Lead Time",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "qty_to_order",
			"label": "Qty To Order",
			"fieldtype": "Data",
			"width": 100
		}
	]
	
	
	data = get_data(filters)
	
	return coloumns, data
def get_data(filters):
	data = []
	wh = filters.get("warehouse")

	if wh:
		stock = frappe.db.get_all("Bin", filters={"warehouse": wh}, fields=["item_code", "actual_qty",  "stock_uom", "reserved_qty"])
		for st in stock:
			item_code = st.item_code
			item_name = frappe.db.get_value("Item", item_code, "item_name")
			item_group = frappe.db.get_value("Item", item_code, "item_group")
			uom = st.stock_uom
			stock_balance = st.actual_qty
			lead_time = 1
			if not lead_time:
				lead_time = 1
			safety_stock = frappe.db.get_value("Item", item_code, "safety_stock")

			#average consumption or out quantity for a time period
			avg_consumption = get_average_consumption(filters, item_code)
			reserve_stock = lead_time 
			if int(safety_stock) > int(lead_time):
				reserve_stock =  safety_stock
			qty_to_order = int((reserve_stock - stock_balance) * avg_consumption )
			if qty_to_order < 0:
				qty_to_order = 0

			data.append({
				"item_group": item_group,
				"item_name": item_name,
				"item_code": item_code,
				"uom": uom,
				"reserved": reserve_stock,
				"stock": stock,
				"balance_stock": stock_balance,
				"avg_consumption": round(avg_consumption, 2),
				"lead_time": 1,
				"qty_to_order": qty_to_order
			})
	return data

def get_average_consumption(filters, item_code):
        #get stock ledger entries where quanity change is negative
       
        entries = frappe.get_list("Stock Ledger Entry",
        filters={
            "item_code": item_code,
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