# Temporary Wage Subsidy Scheme Reconciliation

## Temporary Wage Subsidy Scheme Reconciliation



## PAYE Modernisation

Version 1.0 Version Date

12/06/2020

### Column Descriptions


### Latest Version History

### Audience

This document is for any employer who has registered for the Temporary Wage Subsidy Scheme (TWSS) and wishes to upload a CSV file with the details of the subsidy paid to each of their employees.

### Document context

This document provides a description for each column on the Temporary Wage Subsidy Scheme Reconciliation CSV calculation file.




|  | Column |  |  | Description |  |
|---|---|---|---|---|---|
| Column Name |  |  | Name of data column |  |  |
| Description |  |  | Description of the data element and the format that will be applied |  |  |
| Notes |  |  | Any additional detail |  |  |


|  | Version |  |  | Change Date |  |  | Element |  |  | Change Description |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 |  |  | 12/06/2020 |  |  | N/A |  |  | Document published |  |  |


|  | Column Name |  |  | Description |  |  | Notes |  |
|---|---|---|---|---|---|---|---|---|
| Employer Name |  |  | Header: Employer name, max length 100 characters |  |  | Use to identify the employer and confirm that the employer name matches with Revenue records. This field should always be populated. |  |  |
| Employer Registration number |  |  | Header: Used to identify employer to which the submission relates, max length 100 characters |  |  | This field should always be populated. |  |  |
| Tax Year |  |  | Header: Used to identify the tax year to which the TWSS lookup relates (YYYY) |  |  | This field should always be populated. |  |  |
| Software Used |  |  | Header: Used to identify the software used. |  |  | Max length 100 |  |  |
| Software Version |  |  | Header: Used to identify the software version. |  |  | Max length 100 |  |  |
| Payroll Run Reference |  |  | Used to identify the Payroll event that the subsidy update refers to. |  |  | This field should always be populated. Max length 50 |  |  |
| Line Item ID |  |  | Used to identify the Payroll line item that the subsidy update refers to. |  |  | This field should always be populated. Max length 50 |  |  |
| Employer Reference |  |  | Employee's internal staff identifier/reference. |  |  | This field is optional; if provided, Max length 50. |  |  |
| Employee PPSN |  |  | The employee PPSN number. |  |  | This field should always be populated. Format is 7 digits (including leading zeros) followed by either 1 or 2 letters. |  |  |
| Employment ID |  |  | The value of this field will be the Employment ID provided to Revenue by the employer when setting up the employment. |  |  | This field should always be populated. Max length 20 |  |  |
| Pay Date |  |  | Date Employee was being paid (DD/MM/YYYY). |  |  | This field should always be populated. Max length 10 (dd/mm/yyyy) |  |  |


| Subsidy Paid | The amount of subsidy paid to the employee. | This field should always be populated. Zero is a valid value. |
|---|---|---|
| ARNWP | Employee's Average Revenue Net Weekly Pay | This field is optional and if provided, should always be populated with an amount greater than 0. |


