# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aptitude technologie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
import easypost

class PriceConfigurator(Document):

	def test_api(self):
		import httplib
		import urllib

		conn = httplib.HTTPConnection(host='www.packit4me.com', port=80)
		frappe.msgprint(_("conn: {0}").format(conn))

		params =  urllib.urlencode({'bins': '0:0:10x10x10', 'items': ['0:0:0:1x1x1', '1:0:0:3x3x3', '2:0:0:2x2x2']})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn.request("POST", "/api/call/raw", params, headers)
		content = conn.getresponse().read()
		conn.close()
		frappe.msgprint(_("Content: {0}").format(content))



		conn = httplib.HTTPConnection(host='www.packit4me.com', port=80)
		params =  urllib.urlencode({'bins': '0:0:10x10x10', 'items': ['0:0:0:1x1x1', '1:0:0:3x3x3', '2:0:0:2x2x2'], 'binId':'0'})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}
		conn.request("POST", "/api/call/preview", params, headers)
		content = conn.getresponse().read()
		conn.close()
		#frappe.msgprint(_("Content: <code> {0} </code>").format(str(content)))

		#frappe.msgprint(_("""
		#<iframe id="serviceFrameSend" src={0} width="1000" height="1000"  frameborder="0">
	#		""").format(content))



		return content
	
	def test(self):
		import requests
		import xml.etree.ElementTree as ET

		content = self.test_api()
		return content


		if self.is_default_shipper_address:
			shipper_city = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'shipper_city')
			shipper_state = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'shipper_state')
			shipper_zipcode = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'shipper_zipcode')
			shipper_country = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'shipper_country')
		else:
			shipper_city = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'shipper_city')
			shipper_state = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'shipper_state')
			shipper_zipcode = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'shipper_zipcode')
			shipper_country = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'shipper_country')
		consignee_city = 'TULSA'
		consignee_state = 'OK'
		consignee_zipcode = 74104
		consignee_country = 'US'
		total_weight = 50
		shipment_class = 50.0
		shipper_aff = 'Y' #true if we are the shipper
		ship_month = 2
		ship_day = 10
		ship_year = 2019
		#US Only: https://www.zipcodeapi.com/rest/rw3tf9DjeiMpy77gvjfg6qO5cU87GjMYp1PynQUijIPHZ6QFMXUdnLbT4iUv5mzf/info.json/85001/degrees  where 85001 = zipcode
		r = requests.get("https://www.abfs.com/xml/aquotexml.asp?DL=2&ID=K4K155D4&ShipCity={shipper_city}&ShipState={shipper_state}&ShipZip={shipper_zipcode}&ShipCountry={shipper_country}&ConsCity={consignee_city}&ConsState={consignee_state}&ConsZip={consignee_zipcode}&ConsCountry={consignee_country}&Wgt1={total_weight}&Class1={shipment_class}&ShipAff={shipper_aff}&ShipMonth={ship_month}&ShipDay={ship_day}&ShipYear={ship_year}".format(shipper_city = shipper_city, shipper_state=shipper_state, shipper_zipcode=shipper_zipcode, shipper_country=shipper_country, consignee_city=consignee_city, consignee_state=consignee_state, consignee_zipcode=consignee_zipcode, consignee_country=consignee_country, total_weight=total_weight, shipment_class=shipment_class, shipper_aff=shipper_aff, ship_month=ship_month, ship_day=ship_day, ship_year=ship_year))
		root = ET.fromstring(r.text)
		try:
			abf_dicount = float(root.find("DISCOUNTPERCENTAGE").text[:-1])
			abf_charge = float(root.find("CHARGE").text)
			amount_before_discount = round(((abf_charge / (100 - abf_dicount)) * 100), 2)
			frappe.throw("abf_charge: {0} <br> abf_dicount: {1} <br> amount_before_discount: {2}".format(abf_charge, abf_dicount, amount_before_discount))
   		except AttributeError:
			frappe.msgprint(_("Rate Quote Error: <br>"))
   	    		for child in root.iter('ERRORMESSAGE'):
				frappe.msgprint(_("<li> {0} </li>").format(child.text))
			frappe.throw('Please fix those issues before proceeding')
		easypost.api_key = "EZTK2501b8a0157045088d3431005830d179E0Y0HFNP0lW0s6B43gxZHw" #DEV
		# create address
		to_address = easypost.Address.create(
			street1="417 Montgomery Street",
			street2="FLOOR 5",
			city="San Francisco",
			state="CA",
			zip="94104",
			country="US",
			company="EasyPost",
			phone="415-456-7890"
		)
		from_address = easypost.Address.create(
			street1="UNDELIEVRABLE ST",
			city="San Francisco",
			state="CA",
			zip="94104",
			country="US",
			company="EasyPost2",
			phone="222-222-7890"
		)
		parcel = easypost.Parcel.create(
			length=20.2,
			width=10.9,
			height=5,
			weight=65.9
		)
		shipment = easypost.Shipment.create(
			to_address=to_address,
			from_address=from_address,
			parcel=parcel
		)
		ship_id = shipment.id
		shipment = easypost.Shipment.retrieve(ship_id)
		for rate in shipment.get_rates().rates:
			carrier = rate.carrier,

			currency = rate.currency,
			rate_price = rate.rate

			frappe.msgprint(_("carrier RATE:  {0}").format(carrier))
			frappe.msgprint(_("currency RATE:  {0}").format(currency))
			frappe.msgprint(_("RATEs:  {0}").format(rate_price))

	def convert_measurement_to_mm(self, measurement, measure):
		if measurement == 'mm':
			measure = measure
		if measurement == 'inches':
			measure = measure * 25.4
		if measurement == 'foot':
			measure = measure * 304.8
		return measure

	def convert_mm_to_foot(self, measure):
		return measure / 304.8

	def get_sqft(self, height, width):
		sqft = (height * width) #/ 144
		#if sqft < 1:
	#		frappe.throw(_("Sorry, the dimensions are too small : {0}  -  {1}").format( height, width  ))
		return sqft

	def get_discount_pourcent(self, total_discount_pourcent, panel_w_back):
		if total_discount_pourcent > 0:
			return (total_discount_pourcent / 100 ) * panel_w_back
		else:
			return 0

	def convert_cad_to_usd(self, amount):
		return amount / float(frappe.db.get_value('Price Configurator Setting', None, 'exchange_rate_usd'))

	def calculate_prices_for_items(self, price_configurator_items, pc_total_discount_pourcent, pc_preferred_currency):
		"""Calculate the price for each panel and update the table accordingly"""
		self.set("price_configurator_items", [])
		for item in price_configurator_items:
			item.item_height_mm = self.convert_measurement_to_mm(self.pc_measurement, item.item_height)
			item.item_width_mm = self.convert_measurement_to_mm(self.pc_measurement, item.item_width)
			height_ft = self.convert_mm_to_foot(item.item_height_mm)
			width_ft = self.convert_mm_to_foot(item.item_width_mm)
			item.item_sqft_per_panel = self.get_sqft(height_ft, width_ft)
			if item.is_zclip:
				item.zclip_qty = self.get_zclip_quantity(item.item_height_mm)
			else:
				item.zclip_qty = 0
			item.zclip_price = self.get_zclip_price(item.zclip_qty, item.item_width_mm, item.item_quantity)
			item.item_panel_price_w_back = self.get_sqft_per_panel_price(item.item_sqft_per_panel, item.item_product, item.item_quantity)
			item.item_discount_pourcent = pc_total_discount_pourcent
			item.item_discount_dollar = self.get_discount_pourcent(pc_total_discount_pourcent, item.item_panel_price_w_back)
			item.item_discount_price = item.item_panel_price_w_back - item.item_discount_dollar
			item.item_line_price_cad = (item.item_discount_price * item.item_quantity) + item.zclip_price
			item.item_line_price_usd = self.convert_cad_to_usd(item.item_line_price_cad)
			item.item_unit_price_cad = item.item_discount_price + (item.zclip_price / item.item_quantity) #get the price for 1 panel
			item.item_unit_price_usd = self.convert_cad_to_usd(item.item_unit_price_cad)
			item.item_total_sqft = item.item_sqft_per_panel * item.item_quantity
			item.price_line = self.get_preferred_currency(pc_preferred_currency, item.item_line_price_cad, item.item_line_price_usd)
			self.append("price_configurator_items", item)

	#Entry Point : Calculate Final Price button
	def calculate_final_price(self):
		"""Will calculate the final price based on price_configurator_item rows"""
		price_configurator_items = frappe.db.get_all('Price Configurator Item', fields=['*'], filters={'parenttype': 'Price Configurator', 'parent': self.name})
		self.pc_total_panel_quantity = sum(t.item_quantity for t in price_configurator_items)
		self.pc_total_discount_pourcent = self.get_panel_qte_discount(self.pc_total_panel_quantity)		
		self.calculate_prices_for_items(price_configurator_items, self.pc_total_discount_pourcent, self.pc_preferred_currency)
		self.calculate_total_prices(price_configurator_items)
		self.save()
		frappe.msgprint("The price have been updated")

	def calculate_total_prices(self, price_configurator_items):
		'''Calculate the total final prices'''
		self.pc_total_line_price_cad = sum(t.item_line_price_cad for t in price_configurator_items)
		self.pc_total_zclip_price = sum(t.zclip_price for t in price_configurator_items)
		self.pc_line_total_unit_price_cad = sum(t.item_unit_price_cad for t in price_configurator_items)
		self.pc_total_unit_price_usd = sum(t.item_unit_price_usd for t in price_configurator_items)
		self.pc_total_sqft = sum(t.item_total_sqft for t in price_configurator_items)
		self.pc_total_sqft_per_panel = self.pc_total_sqft / self.pc_total_panel_quantity
		self.pc_total_base_panel_price = sum(t.item_panel_price_w_back for t in price_configurator_items)
		if self.pc_total_discount_pourcent > 0:
			self.pc_discount_dollar = (self.pc_total_discount_pourcent / 100) * self.pc_total_base_panel_price
		else:
			self.pc_discount_dollar = 0
		self.pc_total_discount_price = self.pc_total_base_panel_price - self.pc_discount_dollar
		self.pc_total_studs_price = self.pc_total_studs * float(frappe.db.get_value('Misc Price', { 'parenttype': 'Price Configurator Setting', 'parent': 'Price Configurator Setting', 'misc_part':'Studs'}, ['misc_price']))

		self.pc_total_av_nuts_price = self.get_av_nuts_price(self.pc_total_av_nuts)
		self.pc_unit_price_cad = self.pc_total_studs_price + self.pc_total_av_nuts_price
		self.pc_unit_price_usd = self.convert_cad_to_usd(self.pc_unit_price_cad)

	def get_zclip_price(self, qty, width, item_quantity):
		width_inches = width / 25.4
		zclip_width = int(width_inches - 4) #Need to remove 4 inches for the border of the panel + round upper
		zclip_price = frappe.db.get_value('Price Configurator Setting', 'Price Configurator Setting', 'zclip_price')
		return zclip_width * int(zclip_price) * qty * item_quantity

	def get_preferred_currency(self, currency, line_price_cad, line_price_usd):
		"""Returns the right amount, based on the selected currency"""
		if currency == 'CAD':
			return line_price_cad
		else:
			return line_price_usd

	def get_panel_qte_discount(self, quantity):
		"""Get the right discount based on the number of panel"""
		discount = 0
		panel_discount_list = frappe.get_all('Discount Range Price', fields=['discount_percent', 'discount_range'], filters={ 'parenttype': 'Price Configurator Setting', 'parent': None })
		panel_discount_list.sort(key=self.sort_list_by_discount_range, reverse=False) #need to order them to be able to get the right discount
		for p in panel_discount_list:
			if quantity == p.discount_range:
				discount = p.discount_percent
				break
			if quantity > p.discount_range:
				discount = p.discount_percent
		return discount

	def get_misc_price(self, misc):
		misc_price = frappe.get_value('Misc Price', {'parenttype': 'Price Configurator Setting', 'parent': 'Price Configurator Setting', 'misc_part':misc}, 'misc_price')
		if not misc_price:
			frappe.throw("Sorry, the select misc have not been set yet. Please contact your administrator.") #Change the message eventually
		return misc_price


	def get_sqft_per_panel_price(self, sqft_per_panel, item, qty):
		"""Get sqft price based on the given sqft"""
		factor = 1
		sqft_per_panel = int(sqft_per_panel) #round the number down
		price_per_sqft = float(frappe.db.get_value('Item', item, 'price_per_sqft'))
		sqft_per_panel_list = frappe.db.get_all('Panel Factor', fields=['panel_range', 'panel_factor'], filters={ 'parenttype': 'Price Configurator Setting', 'parent': 'Price Configurator Setting' })

		sqft_per_panel_list.sort(key=self.sort_list_by_panel_range, reverse=False) #Need to order to be able to get the right prices
		for p in sqft_per_panel_list:
			if qty == p.panel_range:
				factor = p['panel_factor']
				break
			if qty > p.panel_range:
				factor = p['panel_factor']
		frappe.msgprint(_(" <strong>item: {0} </strong> --  sqft_per_panel: {1}  --  factor: {2}  --  qty: {3}").format(item, sqft_per_panel, factor, qty))
		
		return (price_per_sqft * qty * factor * sqft_per_panel)

	def get_av_nuts_price(self, qty):
		"""Get AV Nuts price based on qty"""
		price = 0
		av_nuts_price_list = frappe.get_all('AV Nuts Price Range', fields=['av_nuts_range', 'av_nuts_price'], filters={ 'parenttype': 'Price Configurator Setting', 'parent': 'Price Configurator Setting' })

		av_nuts_price_list.sort(key=self.sort_list_by_av_nuts_range, reverse=False) #Need to order to be able to get the right prices
		for av in av_nuts_price_list:
			if qty == av.av_nuts_range:
				price = av['av_nuts_price']
				break
			if qty > av.av_nuts_range:
				price = av['av_nuts_price']
		return (qty * price) 

	def get_zclip_quantity(self, height):
		"""get zclkip quantity based on panel height"""
		qty = 0
		zclip_price_list = frappe.get_all('ZClip Range', fields=['zclip_range', 'zclip_qty'], filters={ 'parenttype': 'Price Configurator Setting', 'parent': 'Price Configurator Setting' })
		zclip_price_list.sort(key=self.sort_list_by_zclip_range, reverse=False) #Need to order to be able to get the right prices
		for zc in zclip_price_list:
			if height == zc.zclip_range:
				qty = zc['zclip_qty']
				break
			if height > zc.zclip_range:
				qty = zc['zclip_qty']
		return qty

	def sort_list_by_zclip_range(self, json_obj):
		"""Sort given json by zclip range"""
		try:
			return int(json_obj['zclip_range'])
		except KeyError:
			return 0

	def sort_list_by_av_nuts_range(self, json_obj):
		"""Sort given json by av nuts range"""
		try:
			return int(json_obj['av_nuts_range'])
		except KeyError:
			return 0

	def sort_list_by_discount_range(self, json_obj):
		"""Sort given json by discount_range"""
		try:
			return int(json_obj['discount_range'])
		except KeyError:
			return 0

	def sort_list_by_panel_range(self, json_obj):
		"""Sort given json by panel_range"""
		try:
			return int(json_obj['panel_range'])
		except KeyError:
			return 0


@frappe.whitelist()
#Called from Quotation -> 'Create Price Configurator'
def create_price_configurator(quote_name = None):
	"""Create a Price Configurator based on the data in Quotation"""
	quote = frappe.get_doc('Quotation', quote_name)
	quote_shipping_address = frappe.db.get_value('Address', quote.shipping_address_name, ['city', 'country', 'state', 'pincode'], as_dict=True)
	pc_name = frappe.db.get_value('Quotation', quote_name, 'price_configurator')
	if pc_name:
		version = len(pc_name.split('v'))
		if version == 1:
			pc_name = pc_name + 'v1'
		else:
			nb = int(pc_name.split('v')[1])
			nb = nb + 1
			pc_name = "PC-" + quote_name.split("-")[1] + 'v' + str(nb)
	else:
		pc_name = "PC-" + quote_name.split("-")[1]
    
	pc = frappe.new_doc('Price Configurator')
	#Set default measurement and country
	country = 'CA'
	measurement = 'mm'
	if quote_shipping_address:
		if quote_shipping_address.country == 'United States':
			country = 'US'
			measurement = 'inches'
		pc.update({
			'doctype_name': pc_name,
			'pc_measurement': measurement,
			'pc_preferred_currency': quote.currency,
			'consignee_city': quote_shipping_address.city,
			'consignee_state': quote_shipping_address.state,
			'consignee_zipcode': quote_shipping_address.pincode,
			'consignee_country': country,
		})
	else:
		pc.update({
			'doctype_name': pc_name,
			'pc_measurement': measurement,
			'pc_preferred_currency': quote.currency,
		})
	pc.flags.ignore_permissions = True
	pc.save()
	quote.update({ 'price_configurator' : pc_name})
	quote.flags.ignore_permissions = True
	quote.save()





