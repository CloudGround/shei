// Copyright (c) 2016, Aptitude technologie and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Schedule Aid"] = {
	"filters": [
		{
			"fieldname": "prj_type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": "\nArchitectural\nGraphic",
			"default": "Graphic",
		},
	]
}
