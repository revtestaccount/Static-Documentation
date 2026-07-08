# Temporary Wage Subsidy Scheme Operational Phase

## Temporary Wage Subsidy Scheme Operational Phase



## PAYE Modernisation

Version 1.0 Version Date

28/04/2020

### Column Descriptions


### Latest Version History

### Audience

This document is for any employer who has registered for the Temporary Wage Subsidy Scheme (TWSS) and wishes to download a CSV file with a calculation of the maximum subsidy payment amounts for each of their employees, based on their Average Revenue Net Weekly Pay (ARNWP).


|  | Column |  |  | Description |  |
|---|---|---|---|---|---|
| Column Name |  |  | Name of data column |  |  |
| Description |  |  | Description of the data element and the format that will be applied |  |  |
| Notes |  |  | Any additional detail |  |  |


|  | Version |  |  | Change Date |  |  | Element |  |  | Change Description |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 |  |  | 24/04/2020 |  |  | N/A |  |  | Document published |  |  |
|  |  |  | 27/04/2020 |  |  | Tier 1 Tier 2 MWWS |  |  | Updated description |  |  |
|  |  |  |  |  |  | Eligible Employee |  |  | Updated submission date |  |  |
|  |  |  | 28/04/2020 |  |  | Tier 1 MWWS Tier 2 Tier 2 MWWS Tier 3 |  |  | Updated description |  |  |


### Document context

This document provides a description for each column on the Temporary Wage Subsidy Scheme Operational Phase CSV calculation file, available through the Request Revenue Payroll Notifications page in ROS.

|  | Column Name |  |  | Description |  |  | Notes |  |
|---|---|---|---|---|---|---|---|---|
| Employer Name |  |  | Header: Employer name, max length 100 characters |  |  | Use to identify the employer and confirm that the employer name matches with Revenue records |  |  |
| Employer Registration number |  |  | Header: Used to identify employer to which the submission relates, max length 100 characters |  |  | Used to identify employer to which the submission relates. |  |  |
| Agent Tain |  |  | Header: Agent Tax Advisor Identification Number. Required if TWSS is requested by agent on behalf of employer |  |  | Required if TWSS is queried by agent on behalf of employer |  |  |
| Tax Year |  |  | Header: Used to identify the tax year to which the TWSS lookup relates (YYYY) |  |  | The Tax Year TWSS relates to |  |  |
| Date time Effective |  |  | Date & time from when the TWSS calculation is effective from |  |  | The date and time at which the TWSS returned is correct/was issued (YYYY- MMDDThh:mm:ss.sss±hhmm). max length 28 |  |  |
| Employee PPSN |  |  | Format is 7 digits (including leading zeros) followed by either 1 or 2 letters. |  |  | This field will always be populated |  |  |
| Employment ID |  |  | The value of this field will be the Employment ID provided to Revenue by the employer when setting up the employment |  |  | This field will always be populated. For re-hires this will be the employment id from the active employment. |  |  |
| Employer Reference |  |  | Employer reference set by the employer |  |  | This field may be empty and will be populated with employer reference first provided by employer. For re-hires this will be the employer reference from the active employment. |  |  |


| Eligible Employee | This states if employee is eligible or ineligible for the scheme and marks employee as Y/N | An employee is eligible if they have payslips with pay dates between 1st-29th February and submitted before the 1st April for the given employer. These payslips must have included the employee’s PPSN. |
|---|---|---|
| Firstname | First name of the employee | This will be taken from Revenue’s core registration system but if the employee is not registered for PAYE but has provided an PPSN for payroll then it will be the first name as reported by the employer on the payroll. |
| FamilyName | Family name of the employee | This will be taken from Revenue’s core registration system but if the employee is not registered for PAYE but has provided an PPSN for payroll then it will be the first name as reported by the employer on the payroll. |
| Gross Pay | The sum of gross pay on active payslips for pay dates between 01/01/2020 and 29/02/2020 inclusive. | Where employee is ineligible this will be blank. Zero is a valid value. This number will contain two decimal places. For re-hires this will be from the last active employment the employee had with this employer. |
| Income tax paid | The sum of Income tax deducted on active payslips for pay dates between 01/01/2020 and 29/02/2020 inclusive. | Where employee is ineligible this will be blank. Zero is a valid value. This number will contain two decimal places. For re-hires this will be from the last active employment the employee had with this employer. |
| UscPaid | The sum of USC deducted on active payslips for pay dates between 01/01/2020 and 29/02/2020 inclusive. | Where employee is ineligible this will be blank. Zero is a valid value. This number will contain two decimal places. For re-hires this will be from the last active employment the employee had with this employer. |
| Divisor | This is the sum total of the number of insurable weeks as reported on each payslips for pay dates between 01/01/2020 and 29/02/2020 inclusive. This is the number used to calculate the average revenue net weekly pay (ARNWP) | If the number of insurable weeks is 0 or > 9 the divisor will be set to 9. Otherwise this is the sum of the insurable weeks reported on payslips received with pay dates between 01/01/2020 and 29/02/2020. For re-hires this will be from the last active employment the employee had with this employer. |
| ARNWP | This is the sum of the Gross pay minus the sum of Income tax paid, USC paid and EE PRSI paid between 01/01/2020 and 29/02/2020 inclusive divided by the ‘divisor’ figures | Average Revenue Net Weekly Pay This number will contain two decimal places. |
| Tier 1 | Where an employee’s total ARNWP means that more than 1 tier is applicable this provides the maximum gross employer pay applicable for the Tier 1 MWWS. This will be blank if the employee’s total ARNWP means that only 1 tier is applicable. | This number will contain two decimal places. |
| Tier 1 MWWS | Where Tier 1 is blank this is the maximum weekly wage subsidy applicable for the employee. | MWWS – Maximum Weekly Wage Subsidy This number will contain two decimal places. |


|  | Where Tier 1 is populated this provides the maximum weekly wage subsidy applicable for the employee where the gross employer pay is <= Tier 1 |  |
|---|---|---|
| Tier 1 MWEPBT | This is the maximum gross employer pay before tapering that will apply to Tier 1 MWWS. | Maximum Weekly Employer Pay before Tapering at Tier 1 This number will contain two decimal places. |
| Tier 2 | This will be blank if the employee’s total ARNWP means that only 1 tier is applicable. Where an employee’s total ARNWP means that more than 1 tier is applicable this provides the maximum gross employer pay applicable for the Tier 2 MWWS. | This number will contain two decimal places. |
| Tier 2 MWWS | Where Tier 2 is populated this provides the maximum weekly wage subsidy applicable for the employee where the gross employer pay is greater than Tier 1 and less than or equal to Tier 2 | Maximum Weekly Wage Subsidy at Tier 2 This number will contain two decimal places. |
| Tier 2 MWEPBT | This is the maximum gross employer pay before tapering that will apply to Tier 2 MWWS. | Maximum Weekly Employer Pay before Tapering at Tier 2 This number will contain two decimal places. |
| Tier 3 | Where Tier 2 is blank or is 960.01 this will be blank | Temporary Weekly Wage Subsidy Tier 3 This number will contain two decimal places. |
| Tier 3 MWWS | Where Tier 3 is not blank this will be set to 0 | Maximum Weekly Wage Subsidy at Tier 3 This number will contain two decimal places. |


