# Migration Status

> Last updated: **2026-06-06 (end of day — pre-weekend checkpoint)**  
> Branch: `dev_traditionalNavbar` (1 commit ahead of origin — push before closing)

---

## Summary

**Progress:** 576 / 649 tracked assets migrated  
`█████████████████░░░` 89%

### Completed This Week
- ✅ `content/` directory restructure complete — mirrors source project PIT3/PIT4 layout
- ✅ PIT4 SOAP v1 files (WSDLs + XSDs) copied and paths corrected
- ✅ PIT3 & PIT4 bulk example files migrated to `content/PIT3/examples/`
- ✅ `node_modules` removed from tracking; `.gitignore` updated
- ✅ Navbar redesigned: traditional three-band REVDS layout with dropdown navigation on inner pages
- ✅ Home cards and inner section cards made fully clickable (stretched-link)
- ✅ Router updated: `_`-prefixed utility groups skipped correctly, routing conflicts resolved
- ✅ `MIGRATION_STATUS.md` tracker created (this file)

### Still Outstanding
- ❌ PDF → HTML conversion for all Guide, Data Items, REST/SOAP integration guide PDFs
- ❌ REVDS compiled CSS extraction (currently using Bootstrap 5 approximation)
- ❌ Migration script improvements (`--output` arg, font-size heading detection)
- ❌ `sitemap.json` move to project root (currently in `assets/js/`)
- ❌ Validation rules Excel files not yet linked from content pages
- ❌ ERR supporting docs pages (currently pointing to `demodocument.html` placeholder)

---

## PIT Guides (HTML Pages)

| Page | Status | Content Path |
|------|--------|-------------- |
| PAYE PIT Help Desk User Guide | ✅ | `content/pit/payepithelpdeskuserguide.html` |
| PIT Self-Service Guide | ✅ | `content/pit/pitselfserviceguide.html` |

## Bulk-Migrated Units

> These directories are migrated as complete units, not tracked file-by-file.

| Unit | Status | Detail |
|------|--------|--------|
| PIT3 SOAP schema reference (topic*.html + images) | ✅ | 1237 files present |
| PIT4 SOAP schema reference (topic*.html + images) | ✅ | 1236 files present |
| PIT3 SOAP v1 schemas & WSDLs | ✅ | 13 files present |
| PIT4 SOAP v1 schemas & WSDLs | ✅ | 13 files present |
| PIT3 REST API reference | ✅ | 5 files present |
| PIT4 REST API reference | ✅ | 5 files present |

## PIT3

### Data Items

| File | Status | Migrated Path |
|------|--------|---------------|
| `ERR - Enhanced Reporting Notification (ERN) Request Data Items.pdf` | ❌ | — |
| `ERR - Enhanced Reporting Request Monthly Report Data Items.pdf` | ❌ | — |
| `ERR - Enhanced Reporting Submission Request Data Items.pdf` | ❌ | — |
| `PAYE Modernisation - Payroll Submission Request Data Items.pdf` | ❌ | — |
| `PAYE Modernisation - RPN Data Items.pdf` | ❌ | — |
| `PAYE_Modernisation_Returns_Reconciliation_Service_DataItems.pdf` | ❌ | — |

### Examples

| File | Status | Migrated Path |
|------|--------|---------------|
| `ERR Scenarios.zip` | ✅ | `content/PIT3/examples/ERR Scenarios.zip` |
| `ERR_Submission_Multiple_Employees_Single_And_Multiple_Expenses_Request.json` | ✅ | `content/PIT3/examples/ERR_Submission_Multiple_Employees_Single_And_Multiple_Expenses_Request.json` |
| `ERR_Submission_Multiple_Employees_Single_And_Multiple_Expenses_Response.json` | ✅ | `content/PIT3/examples/ERR_Submission_Multiple_Employees_Single_And_Multiple_Expenses_Response.json` |
| `Check_Run_Multiple_Employees_Response.json` | ✅ | `content/PIT3/examples/Check_Run_Multiple_Employees_Response.json` |
| `Check_Submission_Multiple_Employees_Response.json.json` | ✅ | `content/PIT3/examples/Check_Submission_Multiple_Employees_Response.json.json` |
| `ERR_Submission_Multiple_Employees_Single_Expenses_Request.json` | ✅ | `content/PIT3/examples/ERR_Submission_Multiple_Employees_Single_Expenses_Request.json` |
| `ERR_Submission_Multiple_Employees_Single_Expenses_Response.json` | ✅ | `content/PIT3/examples/ERR_Submission_Multiple_Employees_Single_Expenses_Response.json` |
| `Lookup_ERN_Multiple_Employees_Response.json` | ✅ | `content/PIT3/examples/Lookup_ERN_Multiple_Employees_Response.json` |
| `ERR_Submission_Single_Employee_Multiple_Expenses_Request.json` | ✅ | `content/PIT3/examples/ERR_Submission_Single_Employee_Multiple_Expenses_Request.json` |
| `ERR_Submission_Single_Employee_Multiple_Expenses_Response.JSON` | ✅ | `content/PIT3/examples/ERR_Submission_Single_Employee_Multiple_Expenses_Response.JSON` |
| `ERR_File_Upload_CSV_Conversion.zip` | ✅ | `content/PIT3/examples/ERR_File_Upload_CSV_Conversion.zip` |
| `CSV_ExpensesBenefits_Template.csv` | ❌ | — |
| `CSV_LineItemIDsToDelete_Template.csv` | ❌ | — |
| `ERR_File_Upload_Manual_Conversion.pdf` | ❌ | — |
| `Expected_ERR_Upload_Template.json` | ✅ | `content/PIT3/examples/Expected_ERR_Upload_Template.json` |
| `JSON_ExpensesBenefits_Converted_Example.json` | ✅ | `content/PIT3/examples/JSON_ExpensesBenefits_Converted_Example.json` |
| `JSON_LineItemIDsToDelete_Converted_Example.json` | ✅ | `content/PIT3/examples/JSON_LineItemIDsToDelete_Converted_Example.json` |
| `JSON_Root_Template.json` | ✅ | `content/PIT3/examples/JSON_Root_Template.json` |
| `ERR_Scenarios.zip` | ✅ | `content/PIT3/examples/ERR_Scenarios.zip` |
| `Enhanced Reporting Requirements - Overview of Web Service Examples.pdf` | ❌ | — |
| `Example 1_Full_ERR_Life_Cycle.zip` | ✅ | `content/PIT3/examples/Example 1_Full_ERR_Life_Cycle.zip` |
| `1.10_Lookup_ERR_Monthly_Report_Response.JSON` | ✅ | `content/PIT3/examples/1.10_Lookup_ERR_Monthly_Report_Response.JSON` |
| `1.1_Lookup_ERN.JSON` | ✅ | `content/PIT3/examples/1.1_Lookup_ERN.JSON` |
| `1.2_Lookup_ERN_Response.JSON` | ✅ | `content/PIT3/examples/1.2_Lookup_ERN_Response.JSON` |
| `1.3_ERR_Submission_Request.JSON` | ✅ | `content/PIT3/examples/1.3_ERR_Submission_Request.JSON` |
| `1.4_ERR_Submission_Response.JSON` | ✅ | `content/PIT3/examples/1.4_ERR_Submission_Response.JSON` |
| `1.6_Check_ERR_Submission_Response.JSON` | ✅ | `content/PIT3/examples/1.6_Check_ERR_Submission_Response.JSON` |
| `1.8_Check_ERR_Run_Response.JSON` | ✅ | `content/PIT3/examples/1.8_Check_ERR_Run_Response.JSON` |
| `Example 2_Overpayment_Correction.zip` | ✅ | `content/PIT3/examples/Example 2_Overpayment_Correction.zip` |
| `2.1_ERR_Submission_Overpayment_Example.json` | ✅ | `content/PIT3/examples/2.1_ERR_Submission_Overpayment_Example.json` |
| `2.2_Correction_of_ERRSubmission_Overpayment_Example.json` | ✅ | `content/PIT3/examples/2.2_Correction_of_ERRSubmission_Overpayment_Example.json` |
| `Example 3_Underpayment_Correction.zip` | ✅ | `content/PIT3/examples/Example 3_Underpayment_Correction.zip` |
| `3.1_ERR_Submission_Underpayment_Example.json` | ✅ | `content/PIT3/examples/3.1_ERR_Submission_Underpayment_Example.json` |
| `3.2_Correction_of_ERR_Submission_Underpayment_Example.json` | ✅ | `content/PIT3/examples/3.2_Correction_of_ERR_Submission_Underpayment_Example.json` |
| `Example 4_Amendment_of_Incorrect_ERR_Submission.zip` | ✅ | `content/PIT3/examples/Example 4_Amendment_of_Incorrect_ERR_Submission.zip` |
| `4.1_Invalid_ERR_Submission.json` | ✅ | `content/PIT3/examples/4.1_Invalid_ERR_Submission.json` |
| `4.2_Amendment_Using_Previous_LineItemId.json` | ✅ | `content/PIT3/examples/4.2_Amendment_Using_Previous_LineItemId.json` |
| `4.3_Amendment_Using_LineItemIds_To_Delete.json` | ✅ | `content/PIT3/examples/4.3_Amendment_Using_LineItemIds_To_Delete.json` |
| `Example 5_New Sub_Category_ADVANCE_PAYMENT.zip` | ✅ | `content/PIT3/examples/Example 5_New Sub_Category_ADVANCE_PAYMENT.zip` |
| `5_1 ERR Submission Request with an Advance Payment.json` | ✅ | `content/PIT3/examples/5_1 ERR Submission Request with an Advance Payment.json` |
| `5_2_a ERR Submission Request Reconciling an Advance Payment to 1 expense.json` | ✅ | `content/PIT3/examples/5_2_a ERR Submission Request Reconciling an Advance Payment to 1 expense.json` |
| `5_2_b ERR Submission Request Reconciling an Advance Payment to multiple expenses.json` | ✅ | `content/PIT3/examples/5_2_b ERR Submission Request Reconciling an Advance Payment to multiple expenses.json` |
| `Example_1 Full_PAYE_Modernisation_Life_Cycle.zip` | ✅ | `content/PIT3/examples/Example_1 Full_PAYE_Modernisation_Life_Cycle.zip` |
| `1.2_LookupRPNResponse.json` | ✅ | `content/PIT3/examples/1.2_LookupRPNResponse.json` |
| `1.3_PayrollSubmissionRequest.json` | ✅ | `content/PIT3/examples/1.3_PayrollSubmissionRequest.json` |
| `1.4_PayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/1.4_PayrollSubmissionResponse.json` |
| `1.6_CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/1.6_CheckPayrollSubmissionResponse.json` |
| `1.8_CheckPayrollRunResponse.json` | ✅ | `content/PIT3/examples/1.8_CheckPayrollRunResponse.json` |
| `Example_10_Lookup_Payroll_Return_By_Period.zip` | ✅ | `content/PIT3/examples/Example_10_Lookup_Payroll_Return_By_Period.zip` |
| `10.2_Lookup_Payroll_Details_By_Return_Period_Response.json` | ✅ | `content/PIT3/examples/10.2_Lookup_Payroll_Details_By_Return_Period_Response.json` |
| `Example_2_Overpayment_To_Employee.zip` | ✅ | `content/PIT3/examples/Example_2_Overpayment_To_Employee.zip` |
| `2.1_PayrollSubmissionOverpayment.json` | ✅ | `content/PIT3/examples/2.1_PayrollSubmissionOverpayment.json` |
| `2.2_CorrectionOfPayrollSubmissionOverpayment.json` | ✅ | `content/PIT3/examples/2.2_CorrectionOfPayrollSubmissionOverpayment.json` |
| `Example_3_Underpayment_To_Employee.zip` | ✅ | `content/PIT3/examples/Example_3_Underpayment_To_Employee.zip` |
| `3.1_PayrollSubmissionUnderpayment.json` | ✅ | `content/PIT3/examples/3.1_PayrollSubmissionUnderpayment.json` |
| `3.2_CorrectionOfPayrollSubmissionUnderpaymen.json` | ✅ | `content/PIT3/examples/3.2_CorrectionOfPayrollSubmissionUnderpaymen.json` |
| `Example_4_Amendment_Of_Invalid_Payroll_Submission.zip` | ✅ | `content/PIT3/examples/Example_4_Amendment_Of_Invalid_Payroll_Submission.zip` |
| `4.1_InvalidPayrollSubmission.json` | ✅ | `content/PIT3/examples/4.1_InvalidPayrollSubmission.json` |
| `4.2_AmendmentUsingPreviousLineItemID.json` | ✅ | `content/PIT3/examples/4.2_AmendmentUsingPreviousLineItemID.json` |
| `4.3_AmendmentUsingLineItemIDsToDelete.json` | ✅ | `content/PIT3/examples/4.3_AmendmentUsingLineItemIDsToDelete.json` |
| `Example_4_Deletion_Of_Invalid_Payroll_Submission.zip` | ✅ | `content/PIT3/examples/Example_4_Deletion_Of_Invalid_Payroll_Submission.zip` |
| `Example_5_Employer_With_Multiple_Employees.zip` | ✅ | `content/PIT3/examples/Example_5_Employer_With_Multiple_Employees.zip` |
| `5.10_NewRPNResponse.json` | ✅ | `content/PIT3/examples/5.10_NewRPNResponse.json` |
| `5.2_LookupRPNResponse.json` | ✅ | `content/PIT3/examples/5.2_LookupRPNResponse.json` |
| `5.3_PayrollSubmissionRequest.json` | ✅ | `content/PIT3/examples/5.3_PayrollSubmissionRequest.json` |
| `5.4_PayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/5.4_PayrollSubmissionResponse.json` |
| `5.6_CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/5.6_CheckPayrollSubmissionResponse.json` |
| `5.8_CheckPayrollRunResponse.json` | ✅ | `content/PIT3/examples/5.8_CheckPayrollRunResponse.json` |
| `5.9_NewRPNRequest.json` | ✅ | `content/PIT3/examples/5.9_NewRPNRequest.json` |
| `Example_6_Check_Payroll_Run_Response.zip` | ✅ | `content/PIT3/examples/Example_6_Check_Payroll_Run_Response.zip` |
| `6.1_CheckPayrollRunResponse_1.json` | ✅ | `content/PIT3/examples/6.1_CheckPayrollRunResponse_1.json` |
| `6.2_CheckPayrollRunResponse_2.json` | ✅ | `content/PIT3/examples/6.2_CheckPayrollRunResponse_2.json` |
| `6.3_CheckPayrollRunResponse_3.json` | ✅ | `content/PIT3/examples/6.3_CheckPayrollRunResponse_3.json` |
| `Example_7_Payroll_Submission_with_Invalid_Payslips.zip` | ✅ | `content/PIT3/examples/Example_7_Payroll_Submission_with_Invalid_Payslips.zip` |
| `7.1_CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/7.1_CheckPayrollSubmissionResponse.json` |
| `7.2_CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/7.2_CheckPayrollSubmissionResponse.json` |
| `7.3_CheckPayrollRunResponse.json` | ✅ | `content/PIT3/examples/7.3_CheckPayrollRunResponse.json` |
| `Example_8_Batched_Submissions.zip` | ✅ | `content/PIT3/examples/Example_8_Batched_Submissions.zip` |
| `Example_9_Deletion_Of_Incorrect_Payslip_From_Submission.zip` | ✅ | `content/PIT3/examples/Example_9_Deletion_Of_Incorrect_Payslip_From_Submission.zip` |
| `9.1_IncorrectPayslipFromSubmission.json` | ✅ | `content/PIT3/examples/9.1_IncorrectPayslipFromSubmission.json` |
| `9.2_DeletionOFIncorrectPayslipFromSubmission.json` | ✅ | `content/PIT3/examples/9.2_DeletionOFIncorrectPayslipFromSubmission.json` |
| `PAYE Modernisation - Overview of Web Service Examples.pdf` | ❌ | — |
| `REST Request Authentication_V1.pptx` | ❌ | — |
| `REST_Request_Authentication_V1.pdf` | ❌ | — |
| `SOAP_Schema_Reference_Examples.zip` | ✅ | `content/PIT3/examples/SOAP_Schema_Reference_Examples.zip` |
| `Screen_Upload_Examples.zip` | ✅ | `content/PIT3/examples/Screen_Upload_Examples.zip` |
| `ErrSubmission.json` | ✅ | `content/PIT3/examples/ErrSubmission.json` |
| `ErrSubmissionMultipleEmployeesMultipleExpenses.json` | ✅ | `content/PIT3/examples/ErrSubmissionMultipleEmployeesMultipleExpenses.json` |
| `ErrSubmissionMultipleEmployeesSingleExpenses.json` | ✅ | `content/PIT3/examples/ErrSubmissionMultipleEmployeesSingleExpenses.json` |
| `ErrSubmissionSingleEmployeeMultipleExpenses.json` | ✅ | `content/PIT3/examples/ErrSubmissionSingleEmployeeMultipleExpenses.json` |
| `ErrSubmission_Agent.json` | ✅ | `content/PIT3/examples/ErrSubmission_Agent.json` |
| `LookUpERN_Agent.json` | ✅ | `content/PIT3/examples/LookUpERN_Agent.json` |
| `LookupERN.json` | ✅ | `content/PIT3/examples/LookupERN.json` |

### Guide

| File | Status | Migrated Path |
|------|--------|---------------|
| `Compression_Guide_PIT.pdf` | ❌ | — |
| `Documentation_Guide.pdf` | ❌ | — |
| `Employment_ID_Guide.pdf` | ❌ | — |
| `Error_Structure_Guide.pdf` | ❌ | — |
| `Line_Item_Correction_Rules.pdf` | ❌ | — |
| `PIT_Employment_Data_Creation_Guide.pdf` | ❌ | — |

### Rest

| File | Status | Migrated Path |
|------|--------|---------------|
| `REST_Connectivity_Handshake_Guide.pdf` | ❌ | — |
| `REST_Web_Service_Integration_Guide.pdf` | ❌ | — |
| `REST_Web_Service_Integration_Guide_Sample_Http_Messages.zip` | ✅ | `content/PIT3/rest/REST_Web_Service_Integration_Guide_Sample_Http_Messages.zip` |
| `Sample HTTP Override Request.json` | ✅ | `content/PIT3/rest/Sample HTTP Override Request.json` |
| `Sample HTTP Override Request_8001274QH.json` | ✅ | `content/PIT3/rest/Sample HTTP Override Request_8001274QH.json` |
| `paye-employers-rest-api-pit3.html` | ✅ | `content/PIT3/rest/paye-employers-rest-api-pit3.html` |
| `paye-employers-rest-api-pit3.json` | ✅ | `content/PIT3/rest/paye-employers-rest-api-pit3.json` |

### Scenarios

| File | Status | Migrated Path |
|------|--------|---------------|
| `JSON.zip` | ✅ | `content/PIT3/scenarios/JSON.zip` |
| `Scenario_01_Check_Run_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_01_Check_Run_Response.json` |
| `Scenario_01_Check_Submission_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_01_Check_Submission_Response.json` |
| `Scenario_01_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_01_Request.json` |
| `Scenario_01_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_01_Response.json` |
| `Scenario_11_Correction_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Correction_CPR_Response.json` |
| `Scenario_11_Correction_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Correction_CPS_Response.json` |
| `Scenario_11_Correction_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Correction_Request.json` |
| `Scenario_11_Correction_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Correction_Response.json` |
| `Scenario_11_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Original_CPR_Response.json` |
| `Scenario_11_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Original_CPS_Response.json` |
| `Scenario_11_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Original_Request.json` |
| `Scenario_11_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Original_Response.json` |
| `Scenario_12_0_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_0_Original_CPR_Response.json` |
| `Scenario_12_0_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_0_Original_CPS_Response.json` |
| `Scenario_12_0_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_12_0_Original_Request.json` |
| `Scenario_12_0_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_0_Original_Response.json` |
| `Scenario_12_1_Correction_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_1_Correction_CPR_Response.json` |
| `Scenario_12_1_Correction_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_1_Correction_CPS_Response.json` |
| `Scenario_12_1_Correction_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_12_1_Correction_Request.json` |
| `Scenario_12_1_Correction_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_1_Correction_Response.json` |
| `Scenario_12_2_Corrective_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_2_Corrective_CPR_Response.json` |
| `Scenario_12_2_Corrective_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_2_Corrective_CPS_Response.json` |
| `Scenario_12_2_Corrective_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_12_2_Corrective_Request.json` |
| `Scenario_12_2_Corrective_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_2_Corrective_Response.json` |
| `Scenario_13_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_13_CPR_Response.json` |
| `Scenario_13_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_13_CPS_Response.json` |
| `Scenario_13_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_13_Request.json` |
| `Scenario_13_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_13_Response.json` |
| `Scenario_14_1_Overpayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_1_Overpayment_CPR_Response.json` |
| `Scenario_14_1_Overpayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_1_Overpayment_CPS_Response.json` |
| `Scenario_14_1_Overpayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_14_1_Overpayment_Request.json` |
| `Scenario_14_1_Overpayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_1_Overpayment_Response.json` |
| `Scenario_14_2_CorrectivePayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_2_CorrectivePayment_CPR_Response.json` |
| `Scenario_14_2_CorrectivePayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_2_CorrectivePayment_CPS_Response.json` |
| `Scenario_14_2_CorrectivePayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_14_2_CorrectivePayment_Request.json` |
| `Scenario_14_2_CorrectivePayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_2_CorrectivePayment_Response.json` |
| `Scenario_14_3_CorrectivePayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_3_CorrectivePayment_CPR_Response.json` |
| `Scenario_14_3_CorrectivePayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_3_CorrectivePayment_CPS_Response.json` |
| `Scenario_14_3_CorrectivePayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_14_3_CorrectivePayment_Request.json` |
| `Scenario_14_3_CorrectivePayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_3_CorrectivePayment_Response.json` |
| `Scenario_15_0_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_0_Original_CPR_Response.json` |
| `Scenario_15_0_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_0_Original_CPS_Response.json` |
| `Scenario_15_0_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_15_0_Original_Request.json` |
| `Scenario_15_0_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_0_Original_Response.json` |
| `Scenario_15_1_Correction_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_1_Correction_CPR_Response.json` |
| `Scenario_15_1_Correction_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_1_Correction_CPS_Response.json` |
| `Scenario_15_1_Correction_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_15_1_Correction_Request.json` |
| `Scenario_15_1_Correction_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_1_Correction_Response.json` |
| `Scenario_15_2_JanuaryPayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_2_JanuaryPayment_CPR_Response.json` |
| `Scenario_15_2_JanuaryPayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_2_JanuaryPayment_CPS_Response.json` |
| `Scenario_15_2_JanuaryPayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_15_2_JanuaryPayment_Request.json` |
| `Scenario_15_2_JanuaryPayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_2_JanuaryPayment_Response.json` |
| `02-CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/scenarios/02-CheckPayrollSubmissionResponse.json` |
| `Scenario_16_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_16_CPR_Response.json` |
| `Scenario_16_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_16_CPS_Response.json` |
| `Scenario_16_PayrollSubmissionRequest.json` | ✅ | `content/PIT3/scenarios/Scenario_16_PayrollSubmissionRequest.json` |
| `Scenario_16_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_16_Request.json` |
| `Scenario_16_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_16_Response.json` |
| `Scenario_17_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_17_CPR_Response.json` |
| `Scenario_17_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_17_CPS_Response.json` |
| `Scenario_17_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_17_Request.json` |
| `Scenario_17_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_17_Response.json` |
| `Scenario_18_A_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_18_A_CPR_Response.json` |
| `Scenario_18_A_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_18_A_CPS_Response.json` |
| `Scenario_18_A_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_18_A_Request.json` |
| `Scenario_18_A_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_18_A_Response.json` |
| `Scenario_19_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_19_CPR_Response.json` |
| `Scenario_19_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_19_CPS_Response.json` |
| `Scenario_19_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_19_Request.json` |
| `Scenario_19_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_19_Response.json` |
| `Scenario_02_leave_payslip_CheckPayrollRun_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_02_leave_payslip_CheckPayrollRun_Response.json` |
| `Scenario_02_leave_payslip_CheckPayrollSubmission_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_02_leave_payslip_CheckPayrollSubmission_Response.json` |
| `Scenario_02_leave_payslip_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_02_leave_payslip_Request.json` |
| `Scenario_02_leave_payslip_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_02_leave_payslip_Response.json` |
| `Scenario_20_1_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_1_CPR_Response.json` |
| `Scenario_20_1_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_1_CPS_Response.json` |
| `Scenario_20_1_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_20_1_Request.json` |
| `Scenario_20_1_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_1_Response.json` |
| `Scenario_20_2_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_2_CPR_Response.json` |
| `Scenario_20_2_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_2_CPS_Response.json` |
| `Scenario_20_2_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_20_2_Request.json` |
| `Scenario_20_2_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_2_Response.json` |
| `Scenario_20_3_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_3_CPR_Response.json` |
| `Scenario_20_3_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_3_CPS_Response.json` |
| `Scenario_20_3_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_20_3_Request.json` |
| `Scenario_20_3_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_3_Response.json` |
| `Scenario_21_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_21_CPR_Response.json` |
| `Scenario_21_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_21_CPS_Response.json` |
| `Scenario_21_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_21_Request.json` |
| `Scenario_21_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_21_Response.json` |
| `Scenario_22_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_22_CPR_Response.json` |
| `Scenario_22_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_22_CPS_Response.json` |
| `Scenario_22_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_22_Request.json` |
| `Scenario_22_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_22_Response.json` |
| `Scenario_24_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_24_CPR_Response.json` |
| `Scenario_24_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_24_CPS_Response.json` |
| `Scenario_24_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_24_Request.json` |
| `Scenario_24_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_24_Response.json` |
| `Scenario_25_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_25_CPR_Response.json` |
| `Scenario_25_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_25_CPS_Response.json` |
| `Scenario_25_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_25_Request.json` |
| `Scenario_25_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_25_Response.json` |
| `Scenario_26_A_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_26_A_CPR_Response.json` |
| `Scenario_26_A_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_26_A_CPS_Response.json` |
| `Scenario_26_A_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_26_A_Request.json` |
| `Scenario_26_A_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_26_A_Response.json` |
| `Scenario_29_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_29_CPR_Response.json` |
| `Scenario_29_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_29_CPS_Response.json` |
| `Scenario_29_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_29_Request.json` |
| `Scenario_29_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_29_Response.json` |
| `Scenario_03_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_03_CPR_Response.json` |
| `Scenario_03_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_03_CPS_Response.json` |
| `Scenario_03_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_03_Request.json` |
| `Scenario_03_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_03_Response.json` |
| `Scenario_30_Duplicate_New_RPN_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_30_Duplicate_New_RPN_Response.json` |
| `Scenario_30_Duplicate_Payroll_Submission_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_30_Duplicate_Payroll_Submission_Response.json` |
| `Scenario_31_Correction_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Correction_CPR_Response.json` |
| `Scenario_31_Correction_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Correction_CPS_Response.json` |
| `Scenario_31_Correction_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Correction_Request.json` |
| `Scenario_31_Correction_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Correction_Response.json` |
| `Scenario_31_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Original_CPR_Response.json` |
| `Scenario_31_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Original_CPS_Response.json` |
| `Scenario_31_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Original_Request.json` |
| `Scenario_31_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Original_Response.json` |
| `Scenario_32_LookUpRPN_SPC.json` | ✅ | `content/PIT3/scenarios/Scenario_32_LookUpRPN_SPC.json` |
| `Scenario_32_LookUpRPN_SPC_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_32_LookUpRPN_SPC_Response.json` |
| `Scenario_04a_Single_Payslip_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04a_Single_Payslip_CPR_Response.json` |
| `Scenario_04a_Single_Payslip_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04a_Single_Payslip_CPS_Response.json` |
| `Scenario_04a_Single_Payslip_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_04a_Single_Payslip_Request.json` |
| `Scenario_04a_Single_Payslip_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04a_Single_Payslip_Response.json` |
| `Scenario_04b_Multiple_Payslips_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04b_Multiple_Payslips_CPR_Response.json` |
| `Scenario_04b_Multiple_Payslips_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04b_Multiple_Payslips_CPS_Response.json` |
| `Scenario_04b_Multiple_Payslips_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_04b_Multiple_Payslips_Request.json` |
| `Scenario_04b_Multiple_Payslips_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04b_Multiple_Payslips_Response.json` |
| `Scenario_05_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_05_CPR_Response.json` |
| `Scenario_05_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_05_CPS_Response.json` |
| `Scenario_05_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_05_Request.json` |
| `Scenario_05_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_05_Response.json` |
| `Scenario_06_a_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_a_Original_CPR_Response.json` |
| `Scenario_06_a_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_a_Original_CPS_Response.json` |
| `Scenario_06_a_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_06_a_Original_Request.json` |
| `Scenario_06_a_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_a_Original_Response.json` |
| `Scenario_06_b_Corrective_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_b_Corrective_CPR_Response.json` |
| `Scenario_06_b_Corrective_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_b_Corrective_CPS_Response.json` |
| `Scenario_06_b_Corrective_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_06_b_Corrective_Request.json` |
| `Scenario_06_b_Corrective_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_b_Corrective_Response.json` |
| `Scenario_07_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_Response.json` |
| `Scenario_07_a_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_a_Original_CPR_Response.json` |
| `Scenario_07_a_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_a_Original_CPS_Response.json` |
| `Scenario_07_a_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_07_a_Original_Request.json` |
| `Scenario_07_a_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_a_Original_Response.json` |
| `Scenario_07_b_Corrective_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_b_Corrective_CPR_Response.json` |
| `Scenario_07_b_Corrective_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_b_Corrective_CPS_Response.json` |
| `Scenario_07_b_Corrective_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_07_b_Corrective_Request.json` |
| `Scenario_07_b_Corrective_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_b_Corrective_Response.json` |
| `Scenario_08_A_Underpayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_A_Underpayment_CPR_Response.json` |
| `Scenario_08_A_Underpayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_A_Underpayment_CPS_Response.json` |
| `Scenario_08_A_Underpayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_08_A_Underpayment_Request.json` |
| `Scenario_08_A_Underpayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_A_Underpayment_Response.json` |
| `Scenario_08_B_Additional_Payment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_B_Additional_Payment_CPR_Response.json` |
| `Scenario_08_B_Additional_Payment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_B_Additional_Payment_CPS_Response.json` |
| `Scenario_08_B_Additional_Payment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_08_B_Additional_Payment_Request.json` |
| `Scenario_08_B_Additional_Payment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_B_Additional_Payment_Response.json` |
| `Scenario_08_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_Response.json` |
| `Scenario_09_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_Response.json` |
| `Scenario_09_a_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_a_Original_CPR_Response.json` |
| `Scenario_09_a_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_a_Original_CPS_Response.json` |
| `Scenario_09_a_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_09_a_Original_Request.json` |
| `Scenario_09_a_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_a_Original_Response.json` |
| `Scenario_09_b_Bonus_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_b_Bonus_CPR_Response.json` |
| `Scenario_09_b_Bonus_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_b_Bonus_CPS_Response.json` |
| `Scenario_09_b_Bonus_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_09_b_Bonus_Request.json` |
| `Scenario_09_b_Bonus_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_b_Bonus_Response.json` |
| `PSDA_Scenarios.pdf` | ❌ | — |
| `XML.zip` | ✅ | `content/PIT3/scenarios/XML.zip` |

### Schema Publication Changelog.Xlsx

| File | Status | Migrated Path |
|------|--------|---------------|
| `Schema Publication Changelog.xlsx` | ✅ | `content/PIT3/schema publication changelog.xlsx/Schema Publication Changelog.xlsx` |

### Screens

| File | Status | Migrated Path |
|------|--------|---------------|
| `CSV_RPNFormat.csv` | ❌ | — |
| `Overview_of_ROS_Payroll_Reporting.pdf` | ❌ | — |
| `PITSelfServiceGuide.pdf` | ❌ | — |
| `ROS_Payroll_Reporting_JSON_Envelope_schema_pit3.json` | ✅ | `content/PIT3/screens/ROS_Payroll_Reporting_JSON_Envelope_schema_pit3.json` |
| `ROS_Payroll_Reporting_Message_guide.pdf` | ❌ | — |
| `RPN_CSV_Example.csv` | ❌ | — |
| `RPN_Request_CSV_File_Response.pdf` | ❌ | — |
| `examples.zip` | ✅ | `content/PIT3/screens/examples.zip` |
| `createRPN.json` | ✅ | `content/PIT3/screens/createRPN.json` |
| `lookupRPN.json` | ✅ | `content/PIT3/screens/lookupRPN.json` |
| `payrollSubmission.json` | ✅ | `content/PIT3/screens/payrollSubmission.json` |

### Soap

| File | Status | Migrated Path |
|------|--------|---------------|
| `SOAP_Connectivity_Handshake_Guide.pdf` | ❌ | — |
| `SOAP_Lookup_RPNs_by_Range_Guide.pdf` | ❌ | — |
| `SOAP_Request_Authentication_V1.pdf` | ❌ | — |
| `SOAP_Web_Service_Integration_Guide.pdf` | ❌ | — |
| `SOAP_Web_Service_Integration_Guide_Examples.zip` | ✅ | `content/PIT3/soap/SOAP_Web_Service_Integration_Guide_Examples.zip` |
| `paye-types-pit3.xsd` | ✅ | `content/PIT3/soap/v1/common/paye-types-pit3.xsd` |
| `enhanced_reporting-schema-pit3.xsd` | ✅ | `content/PIT3/soap/v1/enhanced_reporting/enhanced_reporting-schema-pit3.xsd` |
| `enhanced_reporting_pit3.wsdl` | ✅ | `content/PIT3/soap/v1/enhanced_reporting_pit3.wsdl` |
| `ern-schema-pit3.xsd` | ✅ | `content/PIT3/soap/v1/ern/ern-schema-pit3.xsd` |
| `ern_pit3.wsdl` | ✅ | `content/PIT3/soap/v1/ern_pit3.wsdl` |
| `handshake-schema-pit3.xsd` | ✅ | `content/PIT3/soap/v1/handshake/handshake-schema-pit3.xsd` |
| `handshake_pit3.wsdl` | ✅ | `content/PIT3/soap/v1/handshake_pit3.wsdl` |
| `payroll-schema-pit3.xsd` | ✅ | `content/PIT3/soap/v1/payroll/payroll-schema-pit3.xsd` |
| `payroll_pit3.wsdl` | ✅ | `content/PIT3/soap/v1/payroll_pit3.wsdl` |
| `returns_reconciliation-schema-pit3.xsd` | ✅ | `content/PIT3/soap/v1/returns_reconciliation/returns_reconciliation-schema-pit3.xsd` |
| `returns_reconciliation_pit3.wsdl` | ✅ | `content/PIT3/soap/v1/returns_reconciliation_pit3.wsdl` |
| `rpn-schema-pit3.xsd` | ✅ | `content/PIT3/soap/v1/rpn/rpn-schema-pit3.xsd` |
| `rpn_pit3.wsdl` | ✅ | `content/PIT3/soap/v1/rpn_pit3.wsdl` |

### Validation Rules

| File | Status | Migrated Path |
|------|--------|---------------|
| `Employer_Submission_RPN_Validation_Rules.xlsx` | ✅ | `content/PIT3/validation-rules/Employer_Submission_RPN_Validation_Rules.xlsx` |
| `Enhanced Reporting Validation Rules.xlsx` | ✅ | `content/PIT3/validation-rules/Enhanced Reporting Validation Rules.xlsx` |

## PIT4

### Data Items

| File | Status | Migrated Path |
|------|--------|---------------|
| `ERR - Enhanced Reporting Notification (ERN) Request Data Items.pdf` | ❌ | — |
| `ERR - Enhanced Reporting Request Monthly Report Data Items.pdf` | ❌ | — |
| `ERR - Enhanced Reporting Submission Request Data Items.pdf` | ❌ | — |
| `PAYE Modernisation - Payroll Submission Request Data Items.pdf` | ❌ | — |
| `PAYE Modernisation - RPN Data Items.pdf` | ❌ | — |
| `PAYE_Modernisation_Returns_Reconciliation_Service_DataItems.pdf` | ❌ | — |

### Examples

| File | Status | Migrated Path |
|------|--------|---------------|
| `ERR Scenarios.zip` | ✅ | `content/PIT3/examples/ERR Scenarios.zip` |
| `ERR_Submission_Multiple_Employees_Single_And_Multiple_Expenses_Request.json` | ✅ | `content/PIT3/examples/ERR_Submission_Multiple_Employees_Single_And_Multiple_Expenses_Request.json` |
| `ERR_Submission_Multiple_Employees_Single_And_Multiple_Expenses_Response.json` | ✅ | `content/PIT3/examples/ERR_Submission_Multiple_Employees_Single_And_Multiple_Expenses_Response.json` |
| `Check_Run_Multiple_Employees_Response.json` | ✅ | `content/PIT3/examples/Check_Run_Multiple_Employees_Response.json` |
| `Check_Submission_Multiple_Employees_Response.json.json` | ✅ | `content/PIT3/examples/Check_Submission_Multiple_Employees_Response.json.json` |
| `ERR_Submission_Multiple_Employees_Single_Expenses_Request.json` | ✅ | `content/PIT3/examples/ERR_Submission_Multiple_Employees_Single_Expenses_Request.json` |
| `ERR_Submission_Multiple_Employees_Single_Expenses_Response.json` | ✅ | `content/PIT3/examples/ERR_Submission_Multiple_Employees_Single_Expenses_Response.json` |
| `Lookup_ERN_Multiple_Employees_Response.json` | ✅ | `content/PIT3/examples/Lookup_ERN_Multiple_Employees_Response.json` |
| `ERR_Submission_Single_Employee_Multiple_Expenses_Request.json` | ✅ | `content/PIT3/examples/ERR_Submission_Single_Employee_Multiple_Expenses_Request.json` |
| `ERR_Submission_Single_Employee_Multiple_Expenses_Response.JSON` | ✅ | `content/PIT3/examples/ERR_Submission_Single_Employee_Multiple_Expenses_Response.JSON` |
| `ERR_File_Upload_CSV_Conversion.zip` | ✅ | `content/PIT3/examples/ERR_File_Upload_CSV_Conversion.zip` |
| `CSV_ExpensesBenefits_Template.csv` | ❌ | — |
| `CSV_LineItemIDsToDelete_Template.csv` | ❌ | — |
| `ERR_File_Upload_Manual_Conversion.pdf` | ❌ | — |
| `Expected_ERR_Upload_Template.json` | ✅ | `content/PIT3/examples/Expected_ERR_Upload_Template.json` |
| `JSON_ExpensesBenefits_Converted_Example.json` | ✅ | `content/PIT3/examples/JSON_ExpensesBenefits_Converted_Example.json` |
| `JSON_LineItemIDsToDelete_Converted_Example.json` | ✅ | `content/PIT3/examples/JSON_LineItemIDsToDelete_Converted_Example.json` |
| `JSON_Root_Template.json` | ✅ | `content/PIT3/examples/JSON_Root_Template.json` |
| `ERR_Scenarios.zip` | ✅ | `content/PIT3/examples/ERR_Scenarios.zip` |
| `Enhanced Reporting Requirements - Overview of Web Service Examples.pdf` | ❌ | — |
| `Example 1_Full_ERR_Life_Cycle.zip` | ✅ | `content/PIT3/examples/Example 1_Full_ERR_Life_Cycle.zip` |
| `1.10_Lookup_ERR_Monthly_Report_Response.JSON` | ✅ | `content/PIT3/examples/1.10_Lookup_ERR_Monthly_Report_Response.JSON` |
| `1.1_Lookup_ERN.JSON` | ✅ | `content/PIT3/examples/1.1_Lookup_ERN.JSON` |
| `1.2_Lookup_ERN_Response.JSON` | ✅ | `content/PIT3/examples/1.2_Lookup_ERN_Response.JSON` |
| `1.3_ERR_Submission_Request.JSON` | ✅ | `content/PIT3/examples/1.3_ERR_Submission_Request.JSON` |
| `1.4_ERR_Submission_Response.JSON` | ✅ | `content/PIT3/examples/1.4_ERR_Submission_Response.JSON` |
| `1.6_Check_ERR_Submission_Response.JSON` | ✅ | `content/PIT3/examples/1.6_Check_ERR_Submission_Response.JSON` |
| `1.8_Check_ERR_Run_Response.JSON` | ✅ | `content/PIT3/examples/1.8_Check_ERR_Run_Response.JSON` |
| `Example 2_Overpayment_Correction.zip` | ✅ | `content/PIT3/examples/Example 2_Overpayment_Correction.zip` |
| `2.1_ERR_Submission_Overpayment_Example.json` | ✅ | `content/PIT3/examples/2.1_ERR_Submission_Overpayment_Example.json` |
| `2.2_Correction_of_ERRSubmission_Overpayment_Example.json` | ✅ | `content/PIT3/examples/2.2_Correction_of_ERRSubmission_Overpayment_Example.json` |
| `Example 3_Underpayment_Correction.zip` | ✅ | `content/PIT3/examples/Example 3_Underpayment_Correction.zip` |
| `3.1_ERR_Submission_Underpayment_Example.json` | ✅ | `content/PIT3/examples/3.1_ERR_Submission_Underpayment_Example.json` |
| `3.2_Correction_of_ERR_Submission_Underpayment_Example.json` | ✅ | `content/PIT3/examples/3.2_Correction_of_ERR_Submission_Underpayment_Example.json` |
| `Example 4_Amendment_of_Incorrect_ERR_Submission.zip` | ✅ | `content/PIT3/examples/Example 4_Amendment_of_Incorrect_ERR_Submission.zip` |
| `4.1_Invalid_ERR_Submission.json` | ✅ | `content/PIT3/examples/4.1_Invalid_ERR_Submission.json` |
| `4.2_Amendment_Using_Previous_LineItemId.json` | ✅ | `content/PIT3/examples/4.2_Amendment_Using_Previous_LineItemId.json` |
| `4.3_Amendment_Using_LineItemIds_To_Delete.json` | ✅ | `content/PIT3/examples/4.3_Amendment_Using_LineItemIds_To_Delete.json` |
| `Example 5_New Sub_Category_ADVANCE_PAYMENT.zip` | ✅ | `content/PIT3/examples/Example 5_New Sub_Category_ADVANCE_PAYMENT.zip` |
| `5_1 ERR Submission Request with an Advance Payment.json` | ✅ | `content/PIT3/examples/5_1 ERR Submission Request with an Advance Payment.json` |
| `5_2_a ERR Submission Request Reconciling an Advance Payment to 1 expense.json` | ✅ | `content/PIT3/examples/5_2_a ERR Submission Request Reconciling an Advance Payment to 1 expense.json` |
| `5_2_b ERR Submission Request Reconciling an Advance Payment to multiple expenses.json` | ✅ | `content/PIT3/examples/5_2_b ERR Submission Request Reconciling an Advance Payment to multiple expenses.json` |
| `Example_1 Full_PAYE_Modernisation_Life_Cycle.zip` | ✅ | `content/PIT3/examples/Example_1 Full_PAYE_Modernisation_Life_Cycle.zip` |
| `1.2_LookupRPNResponse.json` | ✅ | `content/PIT3/examples/1.2_LookupRPNResponse.json` |
| `1.3_PayrollSubmissionRequest.json` | ✅ | `content/PIT3/examples/1.3_PayrollSubmissionRequest.json` |
| `1.4_PayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/1.4_PayrollSubmissionResponse.json` |
| `1.6_CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/1.6_CheckPayrollSubmissionResponse.json` |
| `1.8_CheckPayrollRunResponse.json` | ✅ | `content/PIT3/examples/1.8_CheckPayrollRunResponse.json` |
| `Example_10_Lookup_Payroll_Return_By_Period.zip` | ✅ | `content/PIT3/examples/Example_10_Lookup_Payroll_Return_By_Period.zip` |
| `10.2_Lookup_Payroll_Details_By_Return_Period_Response.json` | ✅ | `content/PIT3/examples/10.2_Lookup_Payroll_Details_By_Return_Period_Response.json` |
| `Example_2_Overpayment_To_Employee.zip` | ✅ | `content/PIT3/examples/Example_2_Overpayment_To_Employee.zip` |
| `2.1_PayrollSubmissionOverpayment.json` | ✅ | `content/PIT3/examples/2.1_PayrollSubmissionOverpayment.json` |
| `2.2_CorrectionOfPayrollSubmissionOverpayment.json` | ✅ | `content/PIT3/examples/2.2_CorrectionOfPayrollSubmissionOverpayment.json` |
| `Example_3_Underpayment_To_Employee.zip` | ✅ | `content/PIT3/examples/Example_3_Underpayment_To_Employee.zip` |
| `3.1_PayrollSubmissionUnderpayment.json` | ✅ | `content/PIT3/examples/3.1_PayrollSubmissionUnderpayment.json` |
| `3.2_CorrectionOfPayrollSubmissionUnderpaymen.json` | ✅ | `content/PIT3/examples/3.2_CorrectionOfPayrollSubmissionUnderpaymen.json` |
| `Example_4_Amendment_Of_Invalid_Payroll_Submission.zip` | ✅ | `content/PIT3/examples/Example_4_Amendment_Of_Invalid_Payroll_Submission.zip` |
| `4.1_InvalidPayrollSubmission.json` | ✅ | `content/PIT3/examples/4.1_InvalidPayrollSubmission.json` |
| `4.2_AmendmentUsingPreviousLineItemID.json` | ✅ | `content/PIT3/examples/4.2_AmendmentUsingPreviousLineItemID.json` |
| `4.3_AmendmentUsingLineItemIDsToDelete.json` | ✅ | `content/PIT3/examples/4.3_AmendmentUsingLineItemIDsToDelete.json` |
| `Example_4_Deletion_Of_Invalid_Payroll_Submission.zip` | ✅ | `content/PIT3/examples/Example_4_Deletion_Of_Invalid_Payroll_Submission.zip` |
| `Example_5_Employer_With_Multiple_Employees.zip` | ✅ | `content/PIT3/examples/Example_5_Employer_With_Multiple_Employees.zip` |
| `5.10_NewRPNResponse.json` | ✅ | `content/PIT3/examples/5.10_NewRPNResponse.json` |
| `5.2_LookupRPNResponse.json` | ✅ | `content/PIT3/examples/5.2_LookupRPNResponse.json` |
| `5.3_PayrollSubmissionRequest.json` | ✅ | `content/PIT3/examples/5.3_PayrollSubmissionRequest.json` |
| `5.4_PayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/5.4_PayrollSubmissionResponse.json` |
| `5.6_CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/5.6_CheckPayrollSubmissionResponse.json` |
| `5.8_CheckPayrollRunResponse.json` | ✅ | `content/PIT3/examples/5.8_CheckPayrollRunResponse.json` |
| `5.9_NewRPNRequest.json` | ✅ | `content/PIT3/examples/5.9_NewRPNRequest.json` |
| `Example_6_Check_Payroll_Run_Response.zip` | ✅ | `content/PIT3/examples/Example_6_Check_Payroll_Run_Response.zip` |
| `6.1_CheckPayrollRunResponse_1.json` | ✅ | `content/PIT3/examples/6.1_CheckPayrollRunResponse_1.json` |
| `6.2_CheckPayrollRunResponse_2.json` | ✅ | `content/PIT3/examples/6.2_CheckPayrollRunResponse_2.json` |
| `6.3_CheckPayrollRunResponse_3.json` | ✅ | `content/PIT3/examples/6.3_CheckPayrollRunResponse_3.json` |
| `Example_7_Payroll_Submission_with_Invalid_Payslips.zip` | ✅ | `content/PIT3/examples/Example_7_Payroll_Submission_with_Invalid_Payslips.zip` |
| `7.1_CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/7.1_CheckPayrollSubmissionResponse.json` |
| `7.2_CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/examples/7.2_CheckPayrollSubmissionResponse.json` |
| `7.3_CheckPayrollRunResponse.json` | ✅ | `content/PIT3/examples/7.3_CheckPayrollRunResponse.json` |
| `Example_8_Batched_Submissions.zip` | ✅ | `content/PIT3/examples/Example_8_Batched_Submissions.zip` |
| `Example_9_Deletion_Of_Incorrect_Payslip_From_Submission.zip` | ✅ | `content/PIT3/examples/Example_9_Deletion_Of_Incorrect_Payslip_From_Submission.zip` |
| `9.1_IncorrectPayslipFromSubmission.json` | ✅ | `content/PIT3/examples/9.1_IncorrectPayslipFromSubmission.json` |
| `9.2_DeletionOFIncorrectPayslipFromSubmission.json` | ✅ | `content/PIT3/examples/9.2_DeletionOFIncorrectPayslipFromSubmission.json` |
| `PAYE Modernisation - Overview of Web Service Examples.pdf` | ❌ | — |
| `REST Request Authentication_V1.pptx` | ❌ | — |
| `REST_Request_Authentication_V1.pdf` | ❌ | — |
| `SOAP_Schema_Reference_Examples.zip` | ✅ | `content/PIT3/examples/SOAP_Schema_Reference_Examples.zip` |
| `Screen_Upload_Examples.zip` | ✅ | `content/PIT3/examples/Screen_Upload_Examples.zip` |
| `ErrSubmission.json` | ✅ | `content/PIT3/examples/ErrSubmission.json` |
| `ErrSubmissionMultipleEmployeesMultipleExpenses.json` | ✅ | `content/PIT3/examples/ErrSubmissionMultipleEmployeesMultipleExpenses.json` |
| `ErrSubmissionMultipleEmployeesSingleExpenses.json` | ✅ | `content/PIT3/examples/ErrSubmissionMultipleEmployeesSingleExpenses.json` |
| `ErrSubmissionSingleEmployeeMultipleExpenses.json` | ✅ | `content/PIT3/examples/ErrSubmissionSingleEmployeeMultipleExpenses.json` |
| `ErrSubmission_Agent.json` | ✅ | `content/PIT3/examples/ErrSubmission_Agent.json` |
| `LookUpERN_Agent.json` | ✅ | `content/PIT3/examples/LookUpERN_Agent.json` |
| `LookupERN.json` | ✅ | `content/PIT3/examples/LookupERN.json` |

### Guide

| File | Status | Migrated Path |
|------|--------|---------------|
| `Compression_Guide_PIT.pdf` | ❌ | — |
| `Documentation_Guide.pdf` | ❌ | — |
| `Employment_ID_Guide.pdf` | ❌ | — |
| `Error_Structure_Guide.pdf` | ❌ | — |
| `Line_Item_Correction_Rules.pdf` | ❌ | — |
| `PIT_Employment_Data_Creation_Guide.pdf` | ❌ | — |

### Rest

| File | Status | Migrated Path |
|------|--------|---------------|
| `REST_Connectivity_Handshake_Guide.pdf` | ❌ | — |
| `REST_Web_Service_Integration_Guide.pdf` | ❌ | — |
| `REST_Web_Service_Integration_Guide_Sample_Http_Messages.zip` | ✅ | `content/PIT3/rest/REST_Web_Service_Integration_Guide_Sample_Http_Messages.zip` |
| `Sample HTTP Override Request.json` | ✅ | `content/PIT3/rest/Sample HTTP Override Request.json` |
| `Sample HTTP Override Request_8001274QH.json` | ✅ | `content/PIT3/rest/Sample HTTP Override Request_8001274QH.json` |
| `paye-employers-rest-api-pit4.html` | ✅ | `content/PIT4/rest/paye-employers-rest-api-pit4.html` |
| `paye-employers-rest-api-pit4.json` | ✅ | `content/PIT4/rest/paye-employers-rest-api-pit4.json` |

### Scenarios

| File | Status | Migrated Path |
|------|--------|---------------|
| `JSON.zip` | ✅ | `content/PIT3/scenarios/JSON.zip` |
| `Scenario_01_Check_Run_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_01_Check_Run_Response.json` |
| `Scenario_01_Check_Submission_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_01_Check_Submission_Response.json` |
| `Scenario_01_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_01_Request.json` |
| `Scenario_01_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_01_Response.json` |
| `Scenario_11_Correction_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Correction_CPR_Response.json` |
| `Scenario_11_Correction_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Correction_CPS_Response.json` |
| `Scenario_11_Correction_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Correction_Request.json` |
| `Scenario_11_Correction_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Correction_Response.json` |
| `Scenario_11_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Original_CPR_Response.json` |
| `Scenario_11_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Original_CPS_Response.json` |
| `Scenario_11_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Original_Request.json` |
| `Scenario_11_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_11_Original_Response.json` |
| `Scenario_12_0_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_0_Original_CPR_Response.json` |
| `Scenario_12_0_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_0_Original_CPS_Response.json` |
| `Scenario_12_0_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_12_0_Original_Request.json` |
| `Scenario_12_0_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_0_Original_Response.json` |
| `Scenario_12_1_Correction_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_1_Correction_CPR_Response.json` |
| `Scenario_12_1_Correction_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_1_Correction_CPS_Response.json` |
| `Scenario_12_1_Correction_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_12_1_Correction_Request.json` |
| `Scenario_12_1_Correction_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_1_Correction_Response.json` |
| `Scenario_12_2_Corrective_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_2_Corrective_CPR_Response.json` |
| `Scenario_12_2_Corrective_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_2_Corrective_CPS_Response.json` |
| `Scenario_12_2_Corrective_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_12_2_Corrective_Request.json` |
| `Scenario_12_2_Corrective_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_12_2_Corrective_Response.json` |
| `Scenario_13_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_13_CPR_Response.json` |
| `Scenario_13_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_13_CPS_Response.json` |
| `Scenario_13_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_13_Request.json` |
| `Scenario_13_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_13_Response.json` |
| `Scenario_14_1_Overpayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_1_Overpayment_CPR_Response.json` |
| `Scenario_14_1_Overpayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_1_Overpayment_CPS_Response.json` |
| `Scenario_14_1_Overpayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_14_1_Overpayment_Request.json` |
| `Scenario_14_1_Overpayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_1_Overpayment_Response.json` |
| `Scenario_14_2_CorrectivePayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_2_CorrectivePayment_CPR_Response.json` |
| `Scenario_14_2_CorrectivePayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_2_CorrectivePayment_CPS_Response.json` |
| `Scenario_14_2_CorrectivePayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_14_2_CorrectivePayment_Request.json` |
| `Scenario_14_2_CorrectivePayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_2_CorrectivePayment_Response.json` |
| `Scenario_14_3_CorrectivePayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_3_CorrectivePayment_CPR_Response.json` |
| `Scenario_14_3_CorrectivePayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_3_CorrectivePayment_CPS_Response.json` |
| `Scenario_14_3_CorrectivePayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_14_3_CorrectivePayment_Request.json` |
| `Scenario_14_3_CorrectivePayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_14_3_CorrectivePayment_Response.json` |
| `Scenario_15_0_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_0_Original_CPR_Response.json` |
| `Scenario_15_0_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_0_Original_CPS_Response.json` |
| `Scenario_15_0_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_15_0_Original_Request.json` |
| `Scenario_15_0_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_0_Original_Response.json` |
| `Scenario_15_1_Correction_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_1_Correction_CPR_Response.json` |
| `Scenario_15_1_Correction_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_1_Correction_CPS_Response.json` |
| `Scenario_15_1_Correction_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_15_1_Correction_Request.json` |
| `Scenario_15_1_Correction_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_1_Correction_Response.json` |
| `Scenario_15_2_JanuaryPayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_2_JanuaryPayment_CPR_Response.json` |
| `Scenario_15_2_JanuaryPayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_2_JanuaryPayment_CPS_Response.json` |
| `Scenario_15_2_JanuaryPayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_15_2_JanuaryPayment_Request.json` |
| `Scenario_15_2_JanuaryPayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_15_2_JanuaryPayment_Response.json` |
| `02-CheckPayrollSubmissionResponse.json` | ✅ | `content/PIT3/scenarios/02-CheckPayrollSubmissionResponse.json` |
| `Scenario_16_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_16_CPR_Response.json` |
| `Scenario_16_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_16_CPS_Response.json` |
| `Scenario_16_PayrollSubmissionRequest.json` | ✅ | `content/PIT3/scenarios/Scenario_16_PayrollSubmissionRequest.json` |
| `Scenario_16_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_16_Request.json` |
| `Scenario_16_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_16_Response.json` |
| `Scenario_17_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_17_CPR_Response.json` |
| `Scenario_17_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_17_CPS_Response.json` |
| `Scenario_17_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_17_Request.json` |
| `Scenario_17_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_17_Response.json` |
| `Scenario_18_A_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_18_A_CPR_Response.json` |
| `Scenario_18_A_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_18_A_CPS_Response.json` |
| `Scenario_18_A_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_18_A_Request.json` |
| `Scenario_18_A_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_18_A_Response.json` |
| `Scenario_19_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_19_CPR_Response.json` |
| `Scenario_19_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_19_CPS_Response.json` |
| `Scenario_19_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_19_Request.json` |
| `Scenario_19_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_19_Response.json` |
| `Scenario_02_leave_payslip_CheckPayrollRun_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_02_leave_payslip_CheckPayrollRun_Response.json` |
| `Scenario_02_leave_payslip_CheckPayrollSubmission_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_02_leave_payslip_CheckPayrollSubmission_Response.json` |
| `Scenario_02_leave_payslip_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_02_leave_payslip_Request.json` |
| `Scenario_02_leave_payslip_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_02_leave_payslip_Response.json` |
| `Scenario_20_1_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_1_CPR_Response.json` |
| `Scenario_20_1_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_1_CPS_Response.json` |
| `Scenario_20_1_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_20_1_Request.json` |
| `Scenario_20_1_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_1_Response.json` |
| `Scenario_20_2_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_2_CPR_Response.json` |
| `Scenario_20_2_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_2_CPS_Response.json` |
| `Scenario_20_2_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_20_2_Request.json` |
| `Scenario_20_2_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_2_Response.json` |
| `Scenario_20_3_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_3_CPR_Response.json` |
| `Scenario_20_3_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_3_CPS_Response.json` |
| `Scenario_20_3_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_20_3_Request.json` |
| `Scenario_20_3_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_20_3_Response.json` |
| `Scenario_21_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_21_CPR_Response.json` |
| `Scenario_21_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_21_CPS_Response.json` |
| `Scenario_21_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_21_Request.json` |
| `Scenario_21_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_21_Response.json` |
| `Scenario_22_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_22_CPR_Response.json` |
| `Scenario_22_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_22_CPS_Response.json` |
| `Scenario_22_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_22_Request.json` |
| `Scenario_22_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_22_Response.json` |
| `Scenario_24_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_24_CPR_Response.json` |
| `Scenario_24_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_24_CPS_Response.json` |
| `Scenario_24_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_24_Request.json` |
| `Scenario_24_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_24_Response.json` |
| `Scenario_25_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_25_CPR_Response.json` |
| `Scenario_25_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_25_CPS_Response.json` |
| `Scenario_25_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_25_Request.json` |
| `Scenario_25_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_25_Response.json` |
| `Scenario_26_A_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_26_A_CPR_Response.json` |
| `Scenario_26_A_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_26_A_CPS_Response.json` |
| `Scenario_26_A_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_26_A_Request.json` |
| `Scenario_26_A_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_26_A_Response.json` |
| `Scenario_29_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_29_CPR_Response.json` |
| `Scenario_29_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_29_CPS_Response.json` |
| `Scenario_29_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_29_Request.json` |
| `Scenario_29_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_29_Response.json` |
| `Scenario_03_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_03_CPR_Response.json` |
| `Scenario_03_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_03_CPS_Response.json` |
| `Scenario_03_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_03_Request.json` |
| `Scenario_03_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_03_Response.json` |
| `Scenario_30_Duplicate_New_RPN_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_30_Duplicate_New_RPN_Response.json` |
| `Scenario_30_Duplicate_Payroll_Submission_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_30_Duplicate_Payroll_Submission_Response.json` |
| `Scenario_31_Correction_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Correction_CPR_Response.json` |
| `Scenario_31_Correction_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Correction_CPS_Response.json` |
| `Scenario_31_Correction_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Correction_Request.json` |
| `Scenario_31_Correction_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Correction_Response.json` |
| `Scenario_31_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Original_CPR_Response.json` |
| `Scenario_31_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Original_CPS_Response.json` |
| `Scenario_31_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Original_Request.json` |
| `Scenario_31_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_31_Original_Response.json` |
| `Scenario_32_LookUpRPN_SPC.json` | ✅ | `content/PIT3/scenarios/Scenario_32_LookUpRPN_SPC.json` |
| `Scenario_32_LookUpRPN_SPC_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_32_LookUpRPN_SPC_Response.json` |
| `Scenario_04a_Single_Payslip_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04a_Single_Payslip_CPR_Response.json` |
| `Scenario_04a_Single_Payslip_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04a_Single_Payslip_CPS_Response.json` |
| `Scenario_04a_Single_Payslip_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_04a_Single_Payslip_Request.json` |
| `Scenario_04a_Single_Payslip_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04a_Single_Payslip_Response.json` |
| `Scenario_04b_Multiple_Payslips_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04b_Multiple_Payslips_CPR_Response.json` |
| `Scenario_04b_Multiple_Payslips_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04b_Multiple_Payslips_CPS_Response.json` |
| `Scenario_04b_Multiple_Payslips_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_04b_Multiple_Payslips_Request.json` |
| `Scenario_04b_Multiple_Payslips_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_04b_Multiple_Payslips_Response.json` |
| `Scenario_05_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_05_CPR_Response.json` |
| `Scenario_05_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_05_CPS_Response.json` |
| `Scenario_05_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_05_Request.json` |
| `Scenario_05_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_05_Response.json` |
| `Scenario_06_a_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_a_Original_CPR_Response.json` |
| `Scenario_06_a_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_a_Original_CPS_Response.json` |
| `Scenario_06_a_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_06_a_Original_Request.json` |
| `Scenario_06_a_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_a_Original_Response.json` |
| `Scenario_06_b_Corrective_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_b_Corrective_CPR_Response.json` |
| `Scenario_06_b_Corrective_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_b_Corrective_CPS_Response.json` |
| `Scenario_06_b_Corrective_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_06_b_Corrective_Request.json` |
| `Scenario_06_b_Corrective_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_06_b_Corrective_Response.json` |
| `Scenario_07_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_Response.json` |
| `Scenario_07_a_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_a_Original_CPR_Response.json` |
| `Scenario_07_a_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_a_Original_CPS_Response.json` |
| `Scenario_07_a_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_07_a_Original_Request.json` |
| `Scenario_07_a_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_a_Original_Response.json` |
| `Scenario_07_b_Corrective_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_b_Corrective_CPR_Response.json` |
| `Scenario_07_b_Corrective_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_b_Corrective_CPS_Response.json` |
| `Scenario_07_b_Corrective_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_07_b_Corrective_Request.json` |
| `Scenario_07_b_Corrective_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_07_b_Corrective_Response.json` |
| `Scenario_08_A_Underpayment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_A_Underpayment_CPR_Response.json` |
| `Scenario_08_A_Underpayment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_A_Underpayment_CPS_Response.json` |
| `Scenario_08_A_Underpayment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_08_A_Underpayment_Request.json` |
| `Scenario_08_A_Underpayment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_A_Underpayment_Response.json` |
| `Scenario_08_B_Additional_Payment_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_B_Additional_Payment_CPR_Response.json` |
| `Scenario_08_B_Additional_Payment_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_B_Additional_Payment_CPS_Response.json` |
| `Scenario_08_B_Additional_Payment_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_08_B_Additional_Payment_Request.json` |
| `Scenario_08_B_Additional_Payment_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_B_Additional_Payment_Response.json` |
| `Scenario_08_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_08_Response.json` |
| `Scenario_09_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_Response.json` |
| `Scenario_09_a_Original_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_a_Original_CPR_Response.json` |
| `Scenario_09_a_Original_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_a_Original_CPS_Response.json` |
| `Scenario_09_a_Original_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_09_a_Original_Request.json` |
| `Scenario_09_a_Original_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_a_Original_Response.json` |
| `Scenario_09_b_Bonus_CPR_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_b_Bonus_CPR_Response.json` |
| `Scenario_09_b_Bonus_CPS_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_b_Bonus_CPS_Response.json` |
| `Scenario_09_b_Bonus_Request.json` | ✅ | `content/PIT3/scenarios/Scenario_09_b_Bonus_Request.json` |
| `Scenario_09_b_Bonus_Response.json` | ✅ | `content/PIT3/scenarios/Scenario_09_b_Bonus_Response.json` |
| `PSDA_Scenarios.pdf` | ❌ | — |
| `XML.zip` | ✅ | `content/PIT3/scenarios/XML.zip` |

### Schema Publication Changelog.Xlsx

| File | Status | Migrated Path |
|------|--------|---------------|
| `Schema Publication Changelog.xlsx` | ✅ | `content/PIT3/schema publication changelog.xlsx/Schema Publication Changelog.xlsx` |

### Screens

| File | Status | Migrated Path |
|------|--------|---------------|
| `CSV_RPNFormat.csv` | ❌ | — |
| `Overview_of_ROS_Payroll_Reporting.pdf` | ❌ | — |
| `PITSelfServiceGuide.pdf` | ❌ | — |
| `ROS_Payroll_Reporting_JSON_Envelope_schema_pit4.json` | ✅ | `content/PIT4/screens/ROS_Payroll_Reporting_JSON_Envelope_schema_pit4.json` |
| `ROS_Payroll_Reporting_Message_guide.pdf` | ❌ | — |
| `RPN_CSV_Example.csv` | ❌ | — |
| `RPN_Request_CSV_File_Response.pdf` | ❌ | — |
| `TWSS_CSV_Example.csv` | ❌ | — |
| `TWSS_CSV_Format.csv` | ❌ | — |
| `TWSS_Operational_Phase_CSV_Description.pdf` | ❌ | — |
| `TWSS_Reconciliation_CSV_Description.pdf` | ❌ | — |
| `TWSS_Reconciliation_CSV_Example.csv` | ❌ | — |
| `TWSS_Reconciliation_CSV_Format.csv` | ❌ | — |
| `TWSS_Reconciliation_CSV_Validation.pdf` | ❌ | — |
| `TWSS_Reconciliation_Detail_Download_Example.csv` | ❌ | — |
| `TWSS_Reconciliation_Download_Example.csv` | ❌ | — |
| `examples.zip` | ✅ | `content/PIT3/screens/examples.zip` |
| `createRPN.json` | ✅ | `content/PIT3/screens/createRPN.json` |
| `lookupRPN.json` | ✅ | `content/PIT3/screens/lookupRPN.json` |
| `payrollSubmission.json` | ✅ | `content/PIT3/screens/payrollSubmission.json` |

### Soap

| File | Status | Migrated Path |
|------|--------|---------------|
| `SOAP_Connectivity_Handshake_Guide.pdf` | ❌ | — |
| `SOAP_Lookup_RPNs_by_Range_Guide.pdf` | ❌ | — |
| `SOAP_Request_Authentication_V1.pdf` | ❌ | — |
| `SOAP_Web_Service_Integration_Guide.pdf` | ❌ | — |
| `SOAP_Web_Service_Integration_Guide_Examples.zip` | ✅ | `content/PIT3/soap/SOAP_Web_Service_Integration_Guide_Examples.zip` |
| `paye-types-pit4.xsd` | ✅ | `content/PIT4/soap/v1/common/paye-types-pit4.xsd` |
| `enhanced_reporting-schema-pit4.xsd` | ✅ | `content/PIT4/soap/v1/enhanced_reporting/enhanced_reporting-schema-pit4.xsd` |
| `enhanced_reporting_pit4.wsdl` | ✅ | `content/PIT4/soap/v1/enhanced_reporting_pit4.wsdl` |
| `ern-schema-pit4.xsd` | ✅ | `content/PIT4/soap/v1/ern/ern-schema-pit4.xsd` |
| `ern_pit4.wsdl` | ✅ | `content/PIT4/soap/v1/ern_pit4.wsdl` |
| `handshake-schema-pit4.xsd` | ✅ | `content/PIT4/soap/v1/handshake/handshake-schema-pit4.xsd` |
| `handshake_pit4.wsdl` | ✅ | `content/PIT4/soap/v1/handshake_pit4.wsdl` |
| `payroll-schema-pit4.xsd` | ✅ | `content/PIT4/soap/v1/payroll/payroll-schema-pit4.xsd` |
| `payroll_pit4.wsdl` | ✅ | `content/PIT4/soap/v1/payroll_pit4.wsdl` |
| `returns_reconciliation-schema-pit4.xsd` | ✅ | `content/PIT4/soap/v1/returns_reconciliation/returns_reconciliation-schema-pit4.xsd` |
| `returns_reconciliation_pit4.wsdl` | ✅ | `content/PIT4/soap/v1/returns_reconciliation_pit4.wsdl` |
| `rpn-schema-pit4.xsd` | ✅ | `content/PIT4/soap/v1/rpn/rpn-schema-pit4.xsd` |
| `rpn_pit4.wsdl` | ✅ | `content/PIT4/soap/v1/rpn_pit4.wsdl` |

### Validation Rules

| File | Status | Migrated Path |
|------|--------|---------------|
| `Employer_Submission_RPN_Validation_Rules.xlsx` | ✅ | `content/PIT3/validation-rules/Employer_Submission_RPN_Validation_Rules.xlsx` |
| `Enhanced Reporting Validation Rules.xlsx` | ✅ | `content/PIT3/validation-rules/Enhanced Reporting Validation Rules.xlsx` |

## Not Yet Migrated

| Version | Category | File |
|---------|----------|------|
| PIT3 | Scenarios | `PSDA_Scenarios.pdf` |
| PIT3 | Screens | `CSV_RPNFormat.csv` |
| PIT3 | Screens | `Overview_of_ROS_Payroll_Reporting.pdf` |
| PIT3 | Screens | `PITSelfServiceGuide.pdf` |
| PIT3 | Screens | `ROS_Payroll_Reporting_Message_guide.pdf` |
| PIT3 | Screens | `RPN_CSV_Example.csv` |
| PIT3 | Screens | `RPN_Request_CSV_File_Response.pdf` |
| PIT3 | Data Items | `ERR - Enhanced Reporting Notification (ERN) Request Data Items.pdf` |
| PIT3 | Data Items | `ERR - Enhanced Reporting Request Monthly Report Data Items.pdf` |
| PIT3 | Data Items | `ERR - Enhanced Reporting Submission Request Data Items.pdf` |
| PIT3 | Data Items | `PAYE Modernisation - Payroll Submission Request Data Items.pdf` |
| PIT3 | Data Items | `PAYE Modernisation - RPN Data Items.pdf` |
| PIT3 | Data Items | `PAYE_Modernisation_Returns_Reconciliation_Service_DataItems.pdf` |
| PIT3 | Examples | `CSV_ExpensesBenefits_Template.csv` |
| PIT3 | Examples | `CSV_LineItemIDsToDelete_Template.csv` |
| PIT3 | Examples | `ERR_File_Upload_Manual_Conversion.pdf` |
| PIT3 | Examples | `Enhanced Reporting Requirements - Overview of Web Service Examples.pdf` |
| PIT3 | Examples | `PAYE Modernisation - Overview of Web Service Examples.pdf` |
| PIT3 | Examples | `REST Request Authentication_V1.pptx` |
| PIT3 | Examples | `REST_Request_Authentication_V1.pdf` |
| PIT3 | Guide | `Compression_Guide_PIT.pdf` |
| PIT3 | Guide | `Documentation_Guide.pdf` |
| PIT3 | Guide | `Employment_ID_Guide.pdf` |
| PIT3 | Guide | `Error_Structure_Guide.pdf` |
| PIT3 | Guide | `Line_Item_Correction_Rules.pdf` |
| PIT3 | Guide | `PIT_Employment_Data_Creation_Guide.pdf` |
| PIT3 | Rest | `REST_Connectivity_Handshake_Guide.pdf` |
| PIT3 | Rest | `REST_Web_Service_Integration_Guide.pdf` |
| PIT3 | Soap | `SOAP_Connectivity_Handshake_Guide.pdf` |
| PIT3 | Soap | `SOAP_Lookup_RPNs_by_Range_Guide.pdf` |
| PIT3 | Soap | `SOAP_Request_Authentication_V1.pdf` |
| PIT3 | Soap | `SOAP_Web_Service_Integration_Guide.pdf` |
| PIT4 | Scenarios | `PSDA_Scenarios.pdf` |
| PIT4 | Screens | `CSV_RPNFormat.csv` |
| PIT4 | Screens | `Overview_of_ROS_Payroll_Reporting.pdf` |
| PIT4 | Screens | `PITSelfServiceGuide.pdf` |
| PIT4 | Screens | `ROS_Payroll_Reporting_Message_guide.pdf` |
| PIT4 | Screens | `RPN_CSV_Example.csv` |
| PIT4 | Screens | `RPN_Request_CSV_File_Response.pdf` |
| PIT4 | Screens | `TWSS_CSV_Example.csv` |
| PIT4 | Screens | `TWSS_CSV_Format.csv` |
| PIT4 | Screens | `TWSS_Operational_Phase_CSV_Description.pdf` |
| PIT4 | Screens | `TWSS_Reconciliation_CSV_Description.pdf` |
| PIT4 | Screens | `TWSS_Reconciliation_CSV_Example.csv` |
| PIT4 | Screens | `TWSS_Reconciliation_CSV_Format.csv` |
| PIT4 | Screens | `TWSS_Reconciliation_CSV_Validation.pdf` |
| PIT4 | Screens | `TWSS_Reconciliation_Detail_Download_Example.csv` |
| PIT4 | Screens | `TWSS_Reconciliation_Download_Example.csv` |
| PIT4 | Data Items | `ERR - Enhanced Reporting Notification (ERN) Request Data Items.pdf` |
| PIT4 | Data Items | `ERR - Enhanced Reporting Request Monthly Report Data Items.pdf` |
| PIT4 | Data Items | `ERR - Enhanced Reporting Submission Request Data Items.pdf` |
| PIT4 | Data Items | `PAYE Modernisation - Payroll Submission Request Data Items.pdf` |
| PIT4 | Data Items | `PAYE Modernisation - RPN Data Items.pdf` |
| PIT4 | Data Items | `PAYE_Modernisation_Returns_Reconciliation_Service_DataItems.pdf` |
| PIT4 | Examples | `CSV_ExpensesBenefits_Template.csv` |
| PIT4 | Examples | `CSV_LineItemIDsToDelete_Template.csv` |
| PIT4 | Examples | `ERR_File_Upload_Manual_Conversion.pdf` |
| PIT4 | Examples | `Enhanced Reporting Requirements - Overview of Web Service Examples.pdf` |
| PIT4 | Examples | `PAYE Modernisation - Overview of Web Service Examples.pdf` |
| PIT4 | Examples | `REST Request Authentication_V1.pptx` |
| PIT4 | Examples | `REST_Request_Authentication_V1.pdf` |
| PIT4 | Guide | `Compression_Guide_PIT.pdf` |
| PIT4 | Guide | `Documentation_Guide.pdf` |
| PIT4 | Guide | `Employment_ID_Guide.pdf` |
| PIT4 | Guide | `Error_Structure_Guide.pdf` |
| PIT4 | Guide | `Line_Item_Correction_Rules.pdf` |
| PIT4 | Guide | `PIT_Employment_Data_Creation_Guide.pdf` |
| PIT4 | Rest | `REST_Connectivity_Handshake_Guide.pdf` |
| PIT4 | Rest | `REST_Web_Service_Integration_Guide.pdf` |
| PIT4 | Soap | `SOAP_Connectivity_Handshake_Guide.pdf` |
| PIT4 | Soap | `SOAP_Lookup_RPNs_by_Range_Guide.pdf` |
| PIT4 | Soap | `SOAP_Request_Authentication_V1.pdf` |
| PIT4 | Soap | `SOAP_Web_Service_Integration_Guide.pdf` |
