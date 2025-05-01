# Page 1

 
 
 
 
 
PAYE Modernisation 
RPN Request Response: CSV Schema  


![Image 1](/migrationScripts/RPNRequestCSVFileResponse/images/image_1.png)
![Image 2](/migrationScripts/RPNRequestCSVFileResponse/images/image_2.png)
![Image 3](/migrationScripts/RPNRequestCSVFileResponse/images/image_3.png)

# Page 2

 
2 
PAYE Modernisation – RPN Request: CSV file Response 
Version  
1.0 Release Candidate 2 
Version Date  
02/03/2020 
 
Column Descriptions 
Column 
Description 
Data Item 
Name of data item 
Description and Validation 
Description of the data element and the validation rules that will be applied 
Context 
How the data element will be used by Revenue 
 
Latest Version History 
Version 
Change Date 
Element 
Change Description 
0.10 
02/02/2018 
## N/A 
Document published 
1.0 Release 
Candidate 2 
24/05/2018 
 
Version updated to 1.0 Release Candidate 2 
 
02/03/2020 
Employment Cessation Date 
Item added 
 
22/01/2025 
State Pension (Contributory) 
Item added 
 
Note on ‘Conditional’ data items:  
Where the data item is applicable, the field is mandatory and must be completed. Where the data item is not applicable, the field is not 
required to be completed. For example, the Pensions Tracing Number field is conditional. This means that if the employer operates an employer 
sponsored pension scheme, this field is mandatory. 
 


![Image 4](/migrationScripts/RPNRequestCSVFileResponse/images/image_4.png)

# Page 3

 
3 
PAYE Modernisation – RPN Request: CSV file Response 
RPN request: CSV file Response 
Name 
Column 
Name 
Description and validation 
Context  
Employer Name 
employerNa
me 
Header: Employer name, max length 100 
characters 
Use to identify the employer and confirm that the 
employer name matches with Revenue records 
Employer 
Registration 
number 
employerRe
gistrationN
umber 
Header: Used to identify employer to which 
the submission relates, max length 100 
characters. 
Used to identify employer to which the submission 
relates. 
Agent Tain 
agentTain 
Header: Tax Advisor Identification Number. 
Required if RPN is queried by agent on behalf 
of employer. 
 
Tax Year 
taxYear 
Header: Used to identify the tax year to which 
the RPN lookup relates (YYYY) 
The Tax Year RPN relates to 
Total RPN count 
totalRPNCo
unt 
Header: Total number of RPNs returned  
The total number of RPN that are associated with the 
RPN request submitted. 
Date time 
Effective 
dateTimeEff
ective 
Header: The date and time at which the RPN 
returned is correct/was issued (YYYY-MM-
DDThh:mm:ss.sss±hhmm). max length 28  
Date & time from when the RPN is effective from 
RPN Number 
rpnNumber 
RPN: The number of the RPN issued to the 
employer in respect of an employee. 
Or value Not Found 
Max length 20 
 
RPN: List of RPN that make up a valid lookup RPN 
response. 
NoRPN: EmployeePPSNs and EmploymentIDs of 
employees who do not currently have an RPN 
associated with the employer. New RPN need to be 
requested for these employees using the 
NewRPNRequest service. 
Used in conjunction with the Employee PPSN to 
uniquely identify the instruction issued. 
Employee PPSN 
employeeP
## PSN 
Format is 7 digits (including leading zeros) 
followed by either 1 or 2 letters.  
Max length 10 
Used to identify employee to which the RPN relates. 


![Image 5](/migrationScripts/RPNRequestCSVFileResponse/images/image_5.png)

# Page 4

 
4 
PAYE Modernisation – RPN Request: CSV file Response 
Name 
Column 
Name 
Description and validation 
Context  
Employment ID 
employmen
tID 
The value of this field will be the Employment 
ID provided to Revenue by the employer when 
setting up the employment. If the RPN is being 
triggered as a result of the employee setting up 
the employment via Jobs and Pension or 
contacting Revenue, the value of this field will 
not be populated. Max length 20 
Used to uniquely identify each employment for the 
employee. 
RPN Issue Date 
rpnIssueDat
e 
RPN: Date format yyyy-mm-dd. Max length 10 
The date the RPN issued. 
Employer 
Reference 
employerRe
ference 
Employee internal staff identifier. 
 
Used to uniquely identify the unique employment for 
the employer and employee. 
First Name 
firstName 
First name of the employee. Max length 100 
characters  
Employee first name 
Family Name 
familyNam
e 
Family name of the employee.  
Max length 100 characters 
Employee family name  
Previous 
Employee PPSN 
 
previousEm
ployeePPSN 
Must be valid PPS number (up to 9 chars). 
Format is 7 digits (including leading zeros) 
followed by either 1 or 2 letters. 
Used to identify employees previous PPS number if 
applicable e.g. W PPS number. Should only appear if 
changed since previous submission This will appear 
until Revenue knows that the payroll operator has 
updated the Employee PPSN in their own system i.e. 
until Revenue receives a submission with the new 
Employee PPSN 
Effective Date 
effectiveDa
te 
 
First day on which the RPN specified will apply. 
Max length 10 
 • If the RPN is issued before the start of the 
tax year in question this will be set to January 
1st of the tax year.  
• If the RPN is issued during the tax year in 
question the date is dependent on the 
The instruction can be used from this date until 
updated again. 
 


![Image 6](/migrationScripts/RPNRequestCSVFileResponse/images/image_6.png)

# Page 5

 
5 
PAYE Modernisation – RPN Request: CSV file Response 
Name 
Column 
Name 
Description and validation 
Context  
calculation basis of the RPN as follows: o If the 
calculation basis is Cumulative the date will be 
set to January 1st of the year. o If the 
calculation basis is Week 1 the date will be set 
to the date the RPN issued.  
Date format yyyy-mm-dd  
Min date 2019-01-01 
Date can be in the future 
End Date 
endDate 
The date the RPN ends.  
Date format yyyy-mm-dd  
Min date 2019-01-01 
Max length 10 
Last date on which the RPN specified will 
apply. After this date a new RPN should be 
requested. 
Applicable to Tax Basis Week 1. For Cumulative 
instruction the date will be the XXXX-12-31. This will 
appear if applicable. 
Employment 
Cessation Date 
employmen
tCessationD
ate 
This is the date the employment ceased.  
It is a conditional data item and will only 
appear when the employment to which the 
RPN relates was ceased either by the 
employer or the employee during the current 
year.  
Date format yyyy-mm-dd  
Min date 202X-01-01 
RPNs for ceased employments are required if a post 
cessation payment is being made. The Employment 
Cessation Date allows the employer/payroll operator 
to distinguish between RPNs for live employments 
and ceased employments.   
Income Tax 
Calculation Basis 
incomeTax
Calculation
Basis 
 
PAYE calculation basis used in the submission. 
Options allowed are Cumulative, Week1 and 
Emergency. 
Used to indicate the correct tax basis to be applied. 
Exclusion Order 
exclusionOr
der 
Set to “true” if an exclusion order is on file for 
the employee. This field is not included if an 
exclusion order is not on file for the employee 
Used to indicate if there is an exclusion order on file 
for the employee for the specified period. 


![Image 7](/migrationScripts/RPNRequestCSVFileResponse/images/image_7.png)

# Page 6

 
6 
PAYE Modernisation – RPN Request: CSV file Response 
Name 
Column 
Name 
Description and validation 
Context  
 
Yearly Tax Credit 
yearlyTaxCr
edits 
Amount of tax credits available to the 
employee for the year the RPN relates to. This 
number will contain two decimal places. 
Positive number only 
Net Tax Credits. Amount of tax credits available to the 
employee for the year the RPN relates to. Amount of 
tax credits available for use in the PAYE calculation. 
Breakdown is displayed to employee through PAYE 
Services. 
Tax Rate 1 
Percent 
taxRatePer
cent1 
The lower rate of tax for the year the RPN 
relates to. Positive number only 
Rate to be applied for any income below Rate 1 Cut 
Off. 
Yearly Rate 1 Cut 
Off 
yearlyRateC
utoff1 
Rate 1 cut off for the year the RPN relates. 
Positive number only 
Breakdown is displayed to employee through PAYE 
Services 
Tax Rate 2 
Percent 
taxRatePer
cent2 
The higher rate of tax for the year the RPN 
relates to. Positive number only. 
Rate to be applied for any income above Rate 1 Cut 
Off 
Pay for Income 
Tax to Date 
payForInco
meTaxToDa
te 
This will include total income liable to Income 
Tax to date – including previous employment 
income. In the case of recommencements, this 
includes previous pay from that employer in 
the same tax year. This number will contain 
two decimal places. This field will be 
populated where the Income Tax Calculation 
Basis is cumulative. 
When multiple employments exist, RPN must include 
correct previous employment income. This will 
include only the previous Pay and Tax that should be 
applied. 
Income Tax 
Deducted to 
Date 
incomeTax
DeductedT
oDate 
Total amount of employee’s Income Tax 
deducted to date. In the case of 
recommencements, this includes previous tax 
from that employer in the same tax year. This 
number will contain two decimal places. This 
field will be populated where the Income Tax 
Calculation Basis is cumulative. 
Total Income Tax paid to date. Taking into account any 
PAYE refunded through any unemployment 
repayment claim(s). 
USC Status 
uscStatus 
Ordinary  
Exempt 
Used to deduct correct amount of USC. 


![Image 8](/migrationScripts/RPNRequestCSVFileResponse/images/image_8.png)

# Page 7

 
7 
PAYE Modernisation – RPN Request: CSV file Response 
Name 
Column 
Name 
Description and validation 
Context  
USC Rate 1 
Percent 
uscRatePer
cent1 
USC Rate 1 Percent applicable to USC Status 
Ordinary in the year the RPN relates to. This 
number will contain two decimal places. 
Positive number only 
Current rate 0.5%. 
Yearly USC Rate 1 
Cut Off 
yearlyUSCR
ateCutoff1 
Yearly USC rate 1 cut off applicable to USC 
Status Ordinary in the year the RPN relates to. 
This number will contain two decimal places. 
Positive number only. 
 
USC Rate 2 
Percent 
uscRatePer
cent2 
USC Rate 2 Percent applicable to USC Status 
Ordinary in the year the RPN relates to. This 
number will contain two decimal places. 
Positive number only. 
Current rate 2.5%. 
Yearly USC Rate 2 
Cut Off 
yearlyUSCR
ateCutoff2 
Yearly USC rate 2 cut off applicable to USC 
Status Ordinary in the year the RPN relates to. 
This number will contain two decimal places. 
Positive number only 
 
USC Rate 3 
Percent 
uscRatePer
cent3 
USC Rate 3 Percent applicable to USC Status 
Ordinary in the year the RPN relates to. This 
number will contain two decimal places. 
Positive number only 
Current rate 5%. 
Yearly USC Rate 3 
Cut Off 
yearlyUSCR
ateCutoff3 
Yearly USC rate 3 cut off applicable to USC 
Status Ordinary in the year the RPN relates to. 
This number will contain two decimal places. 
Positive number only 
 
USC Rate 4 
Percent 
uscRatePer
cent4 
Yearly USC rate 4 cut off applicable to USC 
Status Ordinary in the year the RPN relates to. 
This number will contain two decimal places. 
Positive number only 
Current rate 8%. 
Yearly USC Rate 4 
yearlyUSCR
Yearly USC rate 4 applicable to USC Status 
 


![Image 9](/migrationScripts/RPNRequestCSVFileResponse/images/image_9.png)

# Page 8

 
8 
PAYE Modernisation – RPN Request: CSV file Response 
Name 
Column 
Name 
Description and validation 
Context  
Cut Off 
ateCutoff4 
Ordinary in the year the RPN relates to. This 
number will contain two decimal places. 
Positive number only 
Pay for USC to 
Date 
payForUSCT
oDate 
Net pay subject to USC. This number will 
contain two decimal places. This field will be 
populated where the Income Tax Calculation 
Basis is cumulative. 
This will include total income liable to USC to date – 
including previous employment income and any 
additional declared income liable to USC e.g. Rental 
Income. This will appear if available. 
USC Deducted To 
Date 
uscDeducte
dToDate 
Total amount of employee’s USC deducted to 
date. This number will contain two decimal 
places. This field will be populated where the 
Income Tax Calculation Basis is cumulative. 
Positive number only 
Total USC paid to date. Taking into account any USC 
refunded through any unemployment repayment 
claim(s). This will appear if available 
LPT to be 
Deducted 
lptToDeduc
t 
Local Property Tax amount due. Positive 
number only 
Amount of LPT to be deducted through payroll. 
State Pension 
(Contributory) 
statePensio
nCont 
Set to TRUE or FALSE indicating that the 
person is receiving their state pension. This 
field will be required to be TRUE on all RPNs 
for people that are drawing down their state 
contributory pension. 
This field will default to false on all RPNs for people 
that are not drawing down their state contributory 
pension. 
Employee is 
exempt from 
PRSI in Ireland 
prsiExempt 
Set to “true” if employee has been granted an 
exemption from paying PRSI in Ireland. This 
field is not included if employee is not exempt 
from paying PRSI. 
This will appear only where DSP carries out a review 
and determines that the individual should be exempt 
from paying PRSI in Ireland. This must not be 
confused with PRSI exempt income. Will only appear 
where available. 
PRSI Class and 
Subclass 
prsiClass 
PRSI Class and Subclass that the employee 
should be updated to. 
This will appear only where DSP updates the class or 
where DSP knows the individual is on the wrong class 
(i.e. where a review has been carried out by DSP) Will 
only appear where available. 
 


![Image 10](/migrationScripts/RPNRequestCSVFileResponse/images/image_10.png)

