import sublime
import sublime_plugin
import re
import webbrowser


class hl7searchCommand(sublime_plugin.WindowCommand):
	def run(self):     
		
		window = self.window
		view = window.active_view()
		sel = view.sel()
		region1 = sel[0]
		selectionText = view.substr(region1)

		segmentList = segment("","")
		eventList = event("","")

		isValid = 0

		URL = "http://hl7-definition.caristix.com:9010/HL7%20v2.5.1/Default.aspx?version=HL7 v2.5.1&"


		for eventItem in eventList.loadEventList():

			regex = "(\^)"
			filler = "_"
			codeWithoutCircunflex = re.sub(regex, filler, selectionText)

			if (eventItem.code == codeWithoutCircunflex):
				URL = URL + "triggerEvent=" + eventItem.code
				isValid = 1

		for segmentItem in segmentList.loadSegmentList():
			if (segmentItem.code == selectionText):
				URL = URL + "segment=" + segmentItem.code
				isValid = 1


		if (isValid == 1):
			webbrowser.open_new(URL)


class hl7inspectorCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		#Popup layout
		header = ""
		body = ""

		#Segment
		selectedSegment = self.view.substr(self.view.line(self.view.sel()[0]))


		fields = selectedSegment.split('|')

		segmentList = segment("","")

		for segmentItem in segmentList.loadSegmentList():
			if (segmentItem.code == fields[0]):
				header = segmentItem.code + " - " + segmentItem.description


		header = '<b style="color:#33ccff;">' + header + '</b>'


		fieldId = 0
		componentId = 1
		subComponentId = 1


		for field in fields:

			if (field != ""):

				if(field != "^~\&"):
					components =  re.compile(r'(?<!\\)(?:\\\\)*\^').split(field)

					totalCircunflex = field.count("^")

					for component in components:
						if(component != ""):

							subComponents =  re.compile(r'(?<!\\)(?:\\\\)*&').split(component)

							if(len(subComponents) > 1):

								for subComponent in subComponents:
									if(subComponent != ""):

										regex = "(<)"
										filler = "&lt;"
										subComponent = re.sub(regex, filler, subComponent)
			
										regex = "(>)"
										filler = "&gt;"
										subComponent = re.sub(regex, filler, subComponent)
			
										body = body + '<br>' + str(fieldId) + "." + str(componentId) + "."+ str(subComponentId) + " - " + subComponent


									subComponentId = subComponentId + 1

								subComponentId = 1


							else: 

								regex = "(<)"
								filler = "&lt;"
								component = re.sub(regex, filler, component)
	
								regex = "(>)"
								filler = "&gt;"
								component = re.sub(regex, filler, component)
	
	
								if(totalCircunflex > 0):
									body = body + '<br>' + str(fieldId) + "." + str(componentId) + " - " + component
								else:
									body = body + '<br>' + str(fieldId) + " - " + component

						componentId = componentId + 1

					componentId = 1

				else:
					body = body + '<br>' + str(1) + " - " + "^~\&" + "\n"


			fieldId = fieldId + 1

		message = header + body
		message = message.replace("&", "&amp;")

		self.view.show_popup(message, on_navigate=print)
		



class segment(object):
	def __init__(self, code, description):
		self.code = code
		self.description = description

	def loadSegmentList(self):
		segmentList = []

		segmentList.append(segment("ABS", "Abstract"))
		segmentList.append(segment("ACC", "Accident"))
		segmentList.append(segment("ADD", "Addendum"))
		segmentList.append(segment("ADJ", "Adjustment"))
		segmentList.append(segment("AFF", "Professional Affiliation"))
		segmentList.append(segment("AIG", "Appointment Information - General Resource"))
		segmentList.append(segment("AIL", "Appointment Information - Location Resource"))
		segmentList.append(segment("AIP", "Appointment Information - Personnel Resource"))
		segmentList.append(segment("AIS", "Appointment Information"))
		segmentList.append(segment("AL1", "Patient Allergy Information"))
		segmentList.append(segment("APR", "Appointment Preferences"))
		segmentList.append(segment("ARQ", "Appointment Request"))
		segmentList.append(segment("ARV", "Access Restriction"))
		segmentList.append(segment("AUT", "Authorization Information"))
		segmentList.append(segment("BHS", "Batch Header"))
		segmentList.append(segment("BLC", "Blood Code"))
		segmentList.append(segment("BLG", "Billing"))
		segmentList.append(segment("BPO", "Blood product order"))
		segmentList.append(segment("BPX", "Blood product dispense status"))
		segmentList.append(segment("BTS", "Batch Trailer"))
		segmentList.append(segment("BTX", "Blood Product Transfusion/Disposition"))
		segmentList.append(segment("BUI", "Blood Unit Information"))
		segmentList.append(segment("CDM", "Charge Description Master"))
		segmentList.append(segment("CDO", "Cumulative Dosage"))
		segmentList.append(segment("CER", "Certificate Detail"))
		segmentList.append(segment("CM0", "Clinical Study Master"))
		segmentList.append(segment("CM1", "Clinical Study Phase Master"))
		segmentList.append(segment("CM2", "Clinical Study Schedule Master"))
		segmentList.append(segment("CNS", "Clear Notification"))
		segmentList.append(segment("CON", "Consent Segment"))
		segmentList.append(segment("CSP", "Clinical Study Phase"))
		segmentList.append(segment("CSR", "Clinical Study Registration"))
		segmentList.append(segment("CSS", "Clinical Study Data Schedule Segment"))
		segmentList.append(segment("CTD", "Contact Data"))
		segmentList.append(segment("CTI", "Clinical Trial Identification"))
		segmentList.append(segment("DB1", "Disability"))
		segmentList.append(segment("DG1", "Diagnosis"))
		segmentList.append(segment("DMI", "DRG Master File Information"))
		segmentList.append(segment("DON", "Donation"))
		segmentList.append(segment("DRG", "Diagnosis Related Group"))
		segmentList.append(segment("DSC", "Continuation Pointer"))
		segmentList.append(segment("DSP", "Display Data"))
		segmentList.append(segment("ECD", "Equipment Command"))
		segmentList.append(segment("ECR", "Equipment Command Response"))
		segmentList.append(segment("EDU", "Educational Detail"))
		segmentList.append(segment("EQP", "Equipment/log Service"))
		segmentList.append(segment("EQU", "Equipment Detail"))
		segmentList.append(segment("ERR", "Error"))
		segmentList.append(segment("EVN", "Event Type"))
		segmentList.append(segment("FAC", "Facility"))
		segmentList.append(segment("FHS", "File Header"))
		segmentList.append(segment("FT1", "Financial Transaction"))
		segmentList.append(segment("FTS", "File Trailer"))
		segmentList.append(segment("GOL", "Goal Detail"))
		segmentList.append(segment("GP1", "Grouping/Reimbursement - Visit"))
		segmentList.append(segment("GP2", "Grouping/Reimbursement - Procedure Line Item"))
		segmentList.append(segment("GT1", "Guarantor"))
		segmentList.append(segment("Hxx", "any HL7 segment"))
		segmentList.append(segment("IAM", "Patient Adverse Reaction Information"))
		segmentList.append(segment("IAR", "allergy reaction"))
		segmentList.append(segment("IIM", "Inventory Item Master"))
		segmentList.append(segment("ILT", "Material Lot"))
		segmentList.append(segment("IN1", "Insurance"))
		segmentList.append(segment("IN2", "Insurance Additional Information"))
		segmentList.append(segment("IN3", "Insurance Additional Information, Certification"))
		segmentList.append(segment("INV", "Inventory Detail"))
		segmentList.append(segment("IPC", "Imaging Procedure Control Segment"))
		segmentList.append(segment("IPR", "Invoice Processing Results"))
		segmentList.append(segment("ISD", "Interaction Status Detail"))
		segmentList.append(segment("ITM", "Material Item"))
		segmentList.append(segment("IVC", "Invoice Segment"))
		segmentList.append(segment("IVT", "Material Location"))
		segmentList.append(segment("LAN", "Language Detail"))
		segmentList.append(segment("LCC", "Location Charge Code"))
		segmentList.append(segment("LCH", "Location Characteristic"))
		segmentList.append(segment("LDP", "Location Department"))
		segmentList.append(segment("LOC", "Location Identification"))
		segmentList.append(segment("LRL", "Location Relationship"))
		segmentList.append(segment("MFA", "Master File Acknowledgment"))
		segmentList.append(segment("MFE", "Master File Entry"))
		segmentList.append(segment("MFI", "Master File Identification"))
		segmentList.append(segment("MRG", "Merge Patient Information"))
		segmentList.append(segment("MSA", "Message Acknowledgment"))
		segmentList.append(segment("MSH", "Message Header"))
		segmentList.append(segment("NCK", "System Clock"))
		segmentList.append(segment("NDS", "Notification Detail"))
		segmentList.append(segment("NK1", "Next of Kin / Associated Parties"))
		segmentList.append(segment("NPU", "Bed Status Update"))
		segmentList.append(segment("NSC", "Application Status Change"))
		segmentList.append(segment("NST", "Application control level statistics"))
		segmentList.append(segment("NTE", "Notes and Comments"))
		segmentList.append(segment("OBR", "Observation Request"))
		segmentList.append(segment("OBX", "Observation/Result"))
		segmentList.append(segment("ODS", "Dietary Orders, Supplements, and Preferences"))
		segmentList.append(segment("ODT", "Diet Tray Instructions"))
		segmentList.append(segment("OM1", "General Segment"))
		segmentList.append(segment("OM2", "Numeric Observation"))
		segmentList.append(segment("OM3", "Categorical Service/Test/Observation"))
		segmentList.append(segment("OM4", "Observations that Require Specimens"))
		segmentList.append(segment("OM5", "Observation Batteries (Sets)"))
		segmentList.append(segment("OM6", "Observations that are Calculated from Other Observations"))
		segmentList.append(segment("OM7", "Additional Basic Attributes"))
		segmentList.append(segment("ORC", "Common Order"))
		segmentList.append(segment("ORG", "Practitioner Organization Unit"))
		segmentList.append(segment("OVR", "Override Segment"))
		segmentList.append(segment("PAC", "Shipment Package"))
		segmentList.append(segment("PCE", "Patient Charge Cost Center Exceptions"))
		segmentList.append(segment("PCR", "Possible Causal Relationship"))
		segmentList.append(segment("PD1", "Patient Additional Demographic"))
		segmentList.append(segment("PDA", "Patient Death and Autopsy"))
		segmentList.append(segment("PDC", "Product Detail Country"))
		segmentList.append(segment("PEO", "Product Experience Observation"))
		segmentList.append(segment("PES", "Product Experience Sender"))
		segmentList.append(segment("PID", "Patient Identification"))
		segmentList.append(segment("PKG", "Item Packaging"))
		segmentList.append(segment("PMT", "Payment Information"))
		segmentList.append(segment("PR1", "Procedures"))
		segmentList.append(segment("PRA", "Practitioner Detail"))
		segmentList.append(segment("PRB", "Problem Details"))
		segmentList.append(segment("PRC", "Pricing"))
		segmentList.append(segment("PRD", "Provider Data"))
		segmentList.append(segment("PRT", "Participation Information"))
		segmentList.append(segment("PSG", "Product/Service Group"))
		segmentList.append(segment("PSH", "Product Summary Header"))
		segmentList.append(segment("PSL", "Product/Service Line Item"))
		segmentList.append(segment("PSS", "Product/Service Section"))
		segmentList.append(segment("PTH", "Pathway"))
		segmentList.append(segment("PV1", "Patient Visit"))
		segmentList.append(segment("PV2", "Patient Visit - Additional Information"))
		segmentList.append(segment("PYE", "Payee Information"))
		segmentList.append(segment("QAK", "Query Acknowledgment"))
		segmentList.append(segment("QID", "Query Identification"))
		segmentList.append(segment("QPD", "Query Parameter Definition"))
		segmentList.append(segment("QRD", "withdrawn"))
		segmentList.append(segment("QRF", "withdrawn"))
		segmentList.append(segment("QRI", "Query Response Instance"))
		segmentList.append(segment("RCP", "Response Control Parameter"))
		segmentList.append(segment("RDF", "Table Row Definition"))
		segmentList.append(segment("RDT", "Table Row Data"))
		segmentList.append(segment("REL", "Clinical Relationship Segment"))
		segmentList.append(segment("RF1", "Referral Information"))
		segmentList.append(segment("RFI", "Request for Information"))
		segmentList.append(segment("RGS", "Resource Group"))
		segmentList.append(segment("RMI", "Risk Management Incident"))
		segmentList.append(segment("ROL", "Role"))
		segmentList.append(segment("RQ1", "Requisition Detail-1"))
		segmentList.append(segment("RQD", "Requisition Detail"))
		segmentList.append(segment("RXA", "Pharmacy/Treatment Administration"))
		segmentList.append(segment("RXC", "Pharmacy/Treatment Component Order"))
		segmentList.append(segment("RXD", "Pharmacy/Treatment Dispense"))
		segmentList.append(segment("RXE", "Pharmacy/Treatment Encoded Order"))
		segmentList.append(segment("RXG", "Pharmacy/Treatment Give"))
		segmentList.append(segment("RXO", "Pharmacy/Treatment Order"))
		segmentList.append(segment("RXR", "Pharmacy/Treatment Route"))
		segmentList.append(segment("RXV", "Pharmacy/Treatment Infusion"))
		segmentList.append(segment("SAC", "Specimen Container detail"))
		segmentList.append(segment("SCD", "Anti-Microbial Cycle Data"))
		segmentList.append(segment("SCH", "Scheduling Activity Information"))
		segmentList.append(segment("SCP", "Sterilizer Configuration (Anti-Microbial Devices)"))
		segmentList.append(segment("SDD", "Sterilization Device Data"))
		segmentList.append(segment("SFT", "Software Segment"))
		segmentList.append(segment("SGH", "Segment Group Header"))
		segmentList.append(segment("SGT", "Segment Group Trailer"))
		segmentList.append(segment("SHP", "Shipment"))
		segmentList.append(segment("SID", "Substance Identifier"))
		segmentList.append(segment("SLT", "Sterilization Lot"))
		segmentList.append(segment("SPM", "Specimen"))
		segmentList.append(segment("STF", "Staff Identification"))
		segmentList.append(segment("STZ", "Sterilization Parameter"))
		segmentList.append(segment("TCC", "Test Code Configuration"))
		segmentList.append(segment("TCD", "Test Code Detail"))
		segmentList.append(segment("TQ1", "Timing/Quantity"))
		segmentList.append(segment("TQ2", "Timing/Quantity Relationship"))
		segmentList.append(segment("TXA", "Transcription Document Header"))
		segmentList.append(segment("UAC", "User Authentication Credential Segment"))
		segmentList.append(segment("UB1", ""))
		segmentList.append(segment("UB2", "Uniform Billing Data"))
		segmentList.append(segment("URD", "withdrawn"))
		segmentList.append(segment("URS", "withdrawn"))
		segmentList.append(segment("VAR", "Variance"))
		segmentList.append(segment("VND", "Purchasing Vendor"))
		segmentList.append(segment("ZL7", "(proposed example only)"))
		segmentList.append(segment("Zxx", "any Z-Segment"))

		return segmentList


class event(object):
	def __init__(self, code, description):
		self.code = code
		self.description = description

	def loadEventList(self):
		eventList = []

		eventList.append(event("ACK", "General acknowledgment message"))
		eventList.append(event("ADR_A19", "Patient query"))
		eventList.append(event("ADT_A01", "Admit/visit notification"))
		eventList.append(event("ADT_A02", "Transfer a patient"))
		eventList.append(event("ADT_A03", "Discharge/end visit"))
		eventList.append(event("ADT_A04", "Register a patient"))
		eventList.append(event("ADT_A05", "Pre-admit a patient"))
		eventList.append(event("ADT_A06", "Change an outpatient to an inpatient"))
		eventList.append(event("ADT_A07", "Change an inpatient to an outpatient"))
		eventList.append(event("ADT_A08", "Update patient information"))
		eventList.append(event("ADT_A09", "Patient departing - tracking"))
		eventList.append(event("ADT_A10", "Patient arriving - tracking"))
		eventList.append(event("ADT_A11", "Cancel admit/visit notification"))
		eventList.append(event("ADT_A12", "Cancel transfer"))
		eventList.append(event("ADT_A13", "Cancel discharge/end visit"))
		eventList.append(event("ADT_A14", "Pending admit"))
		eventList.append(event("ADT_A15", "Pending transfer"))
		eventList.append(event("ADT_A16", "Pending discharge"))
		eventList.append(event("ADT_A17", "Swap patients"))
		eventList.append(event("ADT_A18", "Merge patient information"))
		eventList.append(event("ADT_A20", "Bed status update"))
		eventList.append(event("ADT_A21", "Patient goes on a \"leave of absence\""))
		eventList.append(event("ADT_A22", "Patient returns from a \"leave of absence\""))
		eventList.append(event("ADT_A23", "Delete a patient record"))
		eventList.append(event("ADT_A24", "Link patient information"))
		eventList.append(event("ADT_A25", "Cancel pending discharge"))
		eventList.append(event("ADT_A26", "Cancel pending transfer"))
		eventList.append(event("ADT_A27", "Cancel pending admit"))
		eventList.append(event("ADT_A28", "Add person information"))
		eventList.append(event("ADT_A29", "Delete person information"))
		eventList.append(event("ADT_A30", "Merge person information"))
		eventList.append(event("ADT_A31", "Update person information"))
		eventList.append(event("ADT_A32", "Cancel patient arriving - tracking"))
		eventList.append(event("ADT_A33", "Cancel patient departing - tracking"))
		eventList.append(event("ADT_A34", "Merge patient information - patient id only"))
		eventList.append(event("ADT_A35", "Merge patient information - account number only"))
		eventList.append(event("ADT_A36", "Merge patient information - patient id and account number"))
		eventList.append(event("ADT_A37", "Unlink patient information"))
		eventList.append(event("ADT_A38", "Cancel pre-admit"))
		eventList.append(event("ADT_A39", "Merge person - patient id"))
		eventList.append(event("ADT_A40", "Merge patient - patient identifier list"))
		eventList.append(event("ADT_A41", "Merge account - patient account number"))
		eventList.append(event("ADT_A42", "Merge visit - visit number"))
		eventList.append(event("ADT_A43", "Move patient information - patient identifier list"))
		eventList.append(event("ADT_A44", "Move account information - patient account number"))
		eventList.append(event("ADT_A45", "Move visit information - visit number"))
		eventList.append(event("ADT_A46", "Change patient id (for backward compatibility only)"))
		eventList.append(event("ADT_A47", "Change patient identifier list"))
		eventList.append(event("ADT_A48", "Change alternate patient id"))
		eventList.append(event("ADT_A49", "Change patient account number"))
		eventList.append(event("ADT_A50", "Change visit number"))
		eventList.append(event("ADT_A51", "Change alternate visit id"))
		eventList.append(event("ADT_A52", "Cancel leave of absence for a patient"))
		eventList.append(event("ADT_A53", "Cancel patient returns from a leave of absence"))
		eventList.append(event("ADT_A54", "Change attending doctor"))
		eventList.append(event("ADT_A55", "Cancel change attending doctor"))
		eventList.append(event("ADT_A60", "Update allergy information"))
		eventList.append(event("ADT_A61", "Change consulting doctor"))
		eventList.append(event("ADT_A62", "Cancel change consulting doctor"))
		eventList.append(event("BAR_P01", "Add patient accounts"))
		eventList.append(event("BAR_P02", "Purge patient accounts"))
		eventList.append(event("BAR_P05", "Update account"))
		eventList.append(event("BAR_P06", "End account"))
		eventList.append(event("BAR_P10", "Transmit ambulatory payment classification(apc)"))
		eventList.append(event("BAR_P12", "Update diagnose/procedure"))
		eventList.append(event("BPS_O29", "Bps message"))
		eventList.append(event("BRP_O30", "Brp message"))
		eventList.append(event("BRT_O32", "Brt message"))
		eventList.append(event("BTS_O31", "Bts message"))
		eventList.append(event("CRM_C01", "Register a patient on a clinical trial"))
		eventList.append(event("CSU_C09", "Automated time intervals for reporting, like monthly"))
		eventList.append(event("DFT_P03", "Post detail financial transaction"))
		eventList.append(event("DFT_P11", "Detail financial transactions"))
		eventList.append(event("DOC_T12", "Document response"))
		eventList.append(event("DSR_Q01", "Display response message"))
		eventList.append(event("DSR_Q03", "Deferred response to a query"))
		eventList.append(event("EAC_U07", "Automated equipment command"))
		eventList.append(event("EAN_U09", "Automated equipment notification"))
		eventList.append(event("EAR_U08", "Automated equipment response"))
		eventList.append(event("EDR_R07", "Enhanced display response"))
		eventList.append(event("EQQ_Q04", "Embedded query language query"))
		eventList.append(event("ERP_R09", "Event replay response"))
		eventList.append(event("ESR_U02", "Automated equipment status request"))
		eventList.append(event("ESU_U01", "Automated equipment status update"))
		eventList.append(event("INR_U06", "Automated equipment inventory request"))
		eventList.append(event("INU_U05", "Automated equipment inventory update"))
		eventList.append(event("LSU_U12", "Automated equipment log/service update"))
		eventList.append(event("MDM_T01", "Original document notification"))
		eventList.append(event("MDM_T02", "Original document notification and content"))
		eventList.append(event("MFK_M01", "Master file application acknowledgment"))
		eventList.append(event("MFN_M02", "Master file - staff practitioner"))
		eventList.append(event("MFN_M04", "Master files charge description"))
		eventList.append(event("MFN_M05", "Patient location master file"))
		eventList.append(event("MFN_M06", "Clinical study with phases and schedules master file"))
		eventList.append(event("MFN_M07", "Clinical study without phases but with schedules master file"))
		eventList.append(event("MFN_M08", "Test/observation (numeric) master file"))
		eventList.append(event("MFN_M09", "Test/observation (categorical) master file"))
		eventList.append(event("MFN_M10", "Test/observation batteries master file"))
		eventList.append(event("MFN_M11", "Test/calculated observations master file"))
		eventList.append(event("MFN_M12", "Master file notification message"))
		eventList.append(event("MFN_M13", "Master files notification"))
		eventList.append(event("MFN_M15", "Master files notification"))
		eventList.append(event("MFQ_M01", "Query for master file record"))
		eventList.append(event("MFR_M04", "Master files response"))
		eventList.append(event("MFR_M05", "Master files response"))
		eventList.append(event("MFR_M06", "Master files response"))
		eventList.append(event("MFR_M07", "Master files response"))
		eventList.append(event("NMD_N02", "Application management data message"))
		eventList.append(event("NMQ_N01", "Application management query message"))
		eventList.append(event("NMR_N01", "Application management response"))
		eventList.append(event("OMB_O27", "Omb message"))
		eventList.append(event("OMD_O03", "Diet order"))
		eventList.append(event("OMG_O19", "General clinical order"))
		eventList.append(event("OMI_O23", "Omi message"))
		eventList.append(event("OML_O21", "Laboratory order"))
		eventList.append(event("OML_O33", "Laboratory order message"))
		eventList.append(event("OML_O35", "Laboratory order message"))
		eventList.append(event("OMN_O07", "Non-stock requisition order"))
		eventList.append(event("OMP_O09", "Pharmacy/treatment order"))
		eventList.append(event("OMS_O05", "Stock requisition order"))
		eventList.append(event("ORB_O28", "Orb message"))
		eventList.append(event("ORD_O04", "Diet order acknowledgement"))
		eventList.append(event("ORF_R04", "Response to query\", \" transmission of requested observation"))
		eventList.append(event("ORG_O20", "General clinical order response"))
		eventList.append(event("ORI_O24", "Ori message"))
		eventList.append(event("ORL_O22", "Response message to oml"))
		eventList.append(event("ORL_O36", "Laboratory acknowledgment message"))
		eventList.append(event("ORM_O01", "Order message"))
		eventList.append(event("ORN_O08", "Non-stock requisition acknowledgement"))
		eventList.append(event("ORP_O10", "Pharmacy/treatment order acknowledgement"))
		eventList.append(event("ORR_O02", "Order response"))
		eventList.append(event("ORS_O06", "Stock requisition acknowledgement"))
		eventList.append(event("ORU", "Unsolicited transmission of an observation message"))
		eventList.append(event("ORU_R01", "Unsolicited transmission of an observation message"))
		eventList.append(event("ORU_R30", "Unsolicited transmission of an observation message"))
		eventList.append(event("OSQ_Q06", "Query for order status"))
		eventList.append(event("OSR_Q06", "Query response for order status"))
		eventList.append(event("OUL_R21", "Unsolicited laboratory observation"))
		eventList.append(event("OUL_R22", "Unsolicited laboratory observation message"))
		eventList.append(event("OUL_R23", "Unsolicited laboratory observation message"))
		eventList.append(event("OUL_R24", "Unsolicited laboratory observation message"))
		eventList.append(event("PEX_P07", "Unsolicited initial individual product experience report"))
		eventList.append(event("PMU_B01", "Add personnel record"))
		eventList.append(event("PMU_B03", "Delete personnel re cord"))
		eventList.append(event("PMU_B04", "Active practicing person"))
		eventList.append(event("PMU_B07", "Add personnel record"))
		eventList.append(event("PMU_B08", "Add personnel record"))
		eventList.append(event("QBP_K13", "Query by parameter"))
		eventList.append(event("QBP_Q11", "Query by parameter"))
		eventList.append(event("QBP_Q13", "Query by parameter"))
		eventList.append(event("QBP_Q21", "Query by parameter"))
		eventList.append(event("QBP_Q22", "Query - Find Candidates"))
		eventList.append(event("QBP_Z73", "Query by parameter"))
		eventList.append(event("QCK_Q02", "Deferred query"))
		eventList.append(event("QCN_J01", "Cancel query/acknowledge message"))
		eventList.append(event("QRY", "Query"))
		eventList.append(event("QRY_A19", "Patient query"))
		eventList.append(event("QRY_PC4", "Problem query"))
		eventList.append(event("QRY_Q01", "Query sent for immediate response"))
		eventList.append(event("QRY_Q02", "Query sent for deferred response"))
		eventList.append(event("QRY_R02", "Query for results of observation"))
		eventList.append(event("QSB_Q16", "Create subscription"))
		eventList.append(event("RAR_RAR", "Pharmacy/treatment administration information"))
		eventList.append(event("RAS_O17", "Pharmacy/treatment administration"))
		eventList.append(event("RCI_I05", "Return clinical information"))
		eventList.append(event("RCL_I06", "Return clinical information"))
		eventList.append(event("RDE_O11", "Pharmacy/treatment encoded order"))
		eventList.append(event("RDR_RDR", "Pharmacy/treatment dispense information"))
		eventList.append(event("RDS_O13", "Pharmacy/treatment dispense"))
		eventList.append(event("RDY_K15", "Display based response"))
		eventList.append(event("REF_I12", "Patient referral"))
		eventList.append(event("RER_RER", "Pharmacy/treatment encoded order information"))
		eventList.append(event("RGR_RGR", "Pharmacy/treatment dose information"))
		eventList.append(event("RGV_O15", "Pharmacy/treatment give"))
		eventList.append(event("ROR_ROR", "Pharmacy prescription order query response"))
		eventList.append(event("RPA_I08", "Return patient authorization"))
		eventList.append(event("RPI_I01", "Return patient information"))
		eventList.append(event("RPI_I04", "Return patient information"))
		eventList.append(event("RPL_I02", "Return patient display list"))
		eventList.append(event("RPR_I03", "Return patient list"))
		eventList.append(event("RQA_I08", "Request for treatment authorization information"))
		eventList.append(event("RQC_I05", "Request for patient clinical information"))
		eventList.append(event("RQI_I01", "Request for insurance information"))
		eventList.append(event("RQP_I04", "Request patient demographics"))
		eventList.append(event("RQQ_Q09", "Event replay query"))
		eventList.append(event("RRA_O18", "Pharmacy/treatment administration acknowledgement"))
		eventList.append(event("RRD_O14", "Pharmacy/treatment dispense acknowledgement"))
		eventList.append(event("RRE_O12", "Pharmacy/treatment encoded order acknowledgement"))
		eventList.append(event("RRG_O16", "Pharmacy/treatment give acknowledgement"))
		eventList.append(event("RRI_I12", "Return referral information"))
		eventList.append(event("RSP_K11", "Segment pattern response"))
		eventList.append(event("RSP_K21", "Segment pattern response"))
		eventList.append(event("RSP_K22", "Segment pattern response"))
		eventList.append(event("RSP_K23", "Segment pattern response"))
		eventList.append(event("RSP_K25", "Segment pattern response"))
		eventList.append(event("RSP_K31", "Segment pattern response"))
		eventList.append(event("RSP_Q11", "Segment pattern response"))
		eventList.append(event("RSP_Z82", "Segment pattern response"))
		eventList.append(event("RSP_Z86", "Segment pattern response"))
		eventList.append(event("RSP_Z88", "Segment pattern response"))
		eventList.append(event("RSP_Z90", "Segment pattern response"))
		eventList.append(event("RTB_K13", "Tabular response"))
		eventList.append(event("RTB_Z74", "Tabular response"))
		eventList.append(event("SIU_S12", "Notification of new appointment booking"))
		eventList.append(event("SIU_S13", "Notification of Appointment Rescheduling"))
		eventList.append(event("SIU_S14", "Notification of Appointment Modification"))
		eventList.append(event("SIU_S15", "Notification of Appointment Cancellation"))
		eventList.append(event("SIU_S16", "Notification of Appointment Discontinuation"))
		eventList.append(event("SIU_S17", "Notification of Appointment Deletion"))
		eventList.append(event("SIU_S18", "Notification of Addition of Service/Resource on Appointment"))
		eventList.append(event("SIU_S19", "Notification of Modification of Service/Resource on Appointment"))
		eventList.append(event("SIU_S20", "Notification of Cancellation of Service/Resource on Appointment"))
		eventList.append(event("SIU_S21", "Notification of Discontinuation of Service/Resource on Appointment"))
		eventList.append(event("SIU_S22", "Notification of Deletion of Service/Resource on Appointment"))
		eventList.append(event("SIU_S23", "Notification of Blocked Schedule Time Slot(S)"))
		eventList.append(event("SIU_S24", "Notification of Opened (un-blocked) Schedule Time Slot(s)"))
		eventList.append(event("SIU_S26", "Notification That Patient Did Not Show Up for Scheduled Appointment"))
		eventList.append(event("SPQ_Q08", "Stored procedure request"))
		eventList.append(event("SQM_S25", "Schedule query message and response"))
		eventList.append(event("SQR_S25", "Schedule query message and response"))
		eventList.append(event("SRM_S01", "Request new appointment booking"))
		eventList.append(event("SRR_S01", "Scheduled request response"))
		eventList.append(event("SSR_U04", "Specimen status request"))
		eventList.append(event("SSU_U03", "Specimen status update"))
		eventList.append(event("TBR_R08", "Tabular data response"))
		eventList.append(event("TCU_U10", "Automated equipment test code settings update"))
		eventList.append(event("UDM_Q05", "Unsolicited display update message"))
		eventList.append(event("VQQ_Q07", "Virtual table query"))
		eventList.append(event("VXQ_V01", "Query for vaccination record"))
		eventList.append(event("VXR_V03", "Vaccination record response"))
		eventList.append(event("VXU_V04", "Unsolicited vaccination record update"))
		eventList.append(event("VXX_V02", "Response to vaccination query"))

		return eventList
