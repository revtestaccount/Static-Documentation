# Reconciliation

## Reconciliation



## Temporary Wage Subsidy Scheme

Version 1.0 Version Date

30/07/2020

### Latest Version History

### Audience

This document is for any employer who has registered for the Temporary Wage Subsidy Scheme (TWSS) and wishes to upload a CSV file with the details of the subsidy paid to each of their employees.

### Document context

This document provides a description of a set of validations that would be performed when a CSV file is uploaded.










|  | Version |  |  | Change Date |  |  | Element |  |  | Change Description |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 |  |  | 30/07/2020 |  |  | N/A |  |  | Document published |  |  |


### Pre-submission Validation






|  | Validation Rule |  |  | Validation Error Message |  |
|---|---|---|---|---|---|
| When the selected file is not .csv |  |  | We are unable to process your file. Please ensure the file is in a valid CSV format. |  |  |
| If file size is larger than 10MB |  |  | Your file has exceeded the maximum size allowable, please ensure your file is less than 10MB. |  |  |
| If max number of line items is more than 50k. This number checks against the line items for a payslip and excludes the headers rows |  |  | Your file has exceeded the maximum amount of line items allowed, please ensure there are no more than 50,000. |  |  |
| Validation against first line headings of CSV |  |  | There are errors with your headings on line 1 of CSV. Allowed values are: employerName, employerRegistrationNumber, taxYear, softwareUsed, softwareVersion. Values are case sensitive. |  |  |
| Validation against third line of CSV for second level headings |  |  | There are errors with your headings on line 3 of CSV. Allowed values are: payrollRunReference, lineItemID, employerReference, employeePpsn, employmentID, payDate, subsidyPaid, arnwp. Values are case sensitive. |  |  |
| Unable to parse the file the file content |  |  | There are errors in your file. Please ensure the data within the file is in a valid format or contact your payroll software provider. |  |  |


### File Format / Schema Validation

** Field size, data format and characters are all schema errors and the submission will be rejected and a file downloaded with the details.
** The error messages would appear in the CSV response file





|  | Field Name |  |  | Mandatory / Optional |  |  | Field Size |  |  |
|---|---|---|---|---|---|---|---|---|---|
| Employer Name |  |  | Mandatory |  |  |  |  | Max Length – 100 characters |  |
| Employer Registration Number |  |  | Mandatory |  |  |  |  | Max Length – 100 characters |  |
| Tax Year |  |  | Mandatory |  |  |  |  | Numerical, 4-digits, valid year |  |
| Software Used |  |  | Optional |  |  |  |  | Max Length – 100 characters |  |
| Software Version |  |  | Optional |  |  |  |  | Max Length – 100 characters |  |
| Payroll Run Reference |  |  | Mandatory |  |  |  |  | Max Length – 50 characters |  |
| Line Item ID |  |  | Mandatory |  |  |  |  | Max Length – 50 characters |  |
| Employer Reference |  |  | Optional |  |  |  |  | Max Length – 50 characters |  |
| Employee PPSN |  |  | Mandatory |  |  |  |  | Format is 7 digits (including leading zeros) followed by either 1 or 2 letters |  |
| Employment ID |  |  | Mandatory |  |  |  |  | Max Length – 20 characters |  |
| Pay Date |  |  | Mandatory |  |  |  |  | Max Length – 10 characters (dd/mm/yyyy) |  |
| Subsidy Paid |  |  | Mandatory |  |  |  |  | Zero is a valid value; negative values unacceptable |  |
| ARNWP |  |  | Optional |  |  |  |  | If provided, value should be greater than 0 |  |


### Business Rules Validation

** Only one business error would trigger at a time ** The error messages would appear in the CSV response file


|  | Validation Rule |  |  | Validation Error Message |  |
|---|---|---|---|---|---|
| Payslip doesn’t exist – Payslip lookup is based on Employer Registration Number + Tax Year + Payroll Run Reference + Line Item ID |  |  | The payslip referenced in the subsidy data does not exist. If this is a valid payslip, please report this as a payroll submission. |  |  |
| Payslip is unlinked – scenario when all the required information is supplied on the CSV, but payslip doesn’t have the Employee ID when looked up |  |  | The payslip referenced in the subsidy data does not include an Employee ID. |  |  |
| PPSN doesn’t match |  |  | The subsidy detail PPSN does not match the PPSN on the referenced payslip. |  |  |
| Employment ID doesn’t match |  |  | The subsidy detail employment ID does not match the employment ID on the referenced payslip. |  |  |
| Pay date doesn’t match |  |  | The subsidy detail pay date does not match the pay date on the referenced payslip |  |  |


