// Copyright (c) 2024, khan and contributors
// For license information, please see license.txt

frappe.query_reports["Inventory Replenishment Report"] = {
	"filters": [
	
		{
			fieldname: 'warehouse',
			label: __('Warehouse'),
			fieldtype: 'Link',
			options: 'Warehouse',
			get_query: function() {
				return {
					filters: {
						'is_group': 0
					}
				};
			}
		},

		// from date
		{
			fieldname: 'from_date',
			label: __('From Date'),
			fieldtype: 'Date',
			default: frappe.datetime.add_days(frappe.datetime.get_today(), -30)
		},
		// to date
		{
			fieldname: 'to_date',
			label: __('To Date'),
			fieldtype: 'Date',
			default: frappe.datetime.get_today()
		},
		
		{
			"label": "Send Email",
			"fieldname": "custom_take_action",
			"fieldtype": "Button",
			"width": 200,
			"click": function() {
				var me = this;
				var filters = me.get_values();
				if (!filters) return;
				frm.call({
					method: "send_email",
					args: {
					},
					callback: function(r) {
						if(r.message) {
							frappe.msgprint(__("Email Sent"));
						}
					}
				});
			}
		}
		
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.id == "qty_to_order" && data["qty_to_order"] > 0) {
			value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
			
		}
		return value
	}
};
