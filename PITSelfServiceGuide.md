# Page 1

 
 
1 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Version  
1.0 Release Candidate 2  
Date  
09/08/2019 
 
PIT Self Service Application Guide 
PAYE Modernisation 


![Image 1](image_x.png)
![Image 2](image_x.png)
![Image 3](image_x.png)

# Page 2

 
 
2 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
 
Version History 
Version 
Date 
Section 
Change Description 
0.1  
20/03/2018 
All  
Initial draft 
 
 
Appendices 
7.3 Known Issues section added 
1.0 Release 
Candidate 
2 
25/05/2018 
 
Version updated to 1.0 Release 
Candidate 2 
29/06/2018 
Section 7 
Added 
20/07/2018 
Section 6.1 
Added 
31/07/2018 
Appendix 
Added Returns Reconciliations 
endpoints 
29/04/2019 
Section 6 
Added customer with fada 
description 
09/08/2019 
Section 3 
Added detail about new 
employee overview screen and 
the new request specific 
certificate button 
Section 4.0 
Added section on employee 
overview 
Section 4.1 
Added section on edit 
employee 
Section 5.2 
Added section on Request 
Specific Employee button 
Audience  
This document is aimed at payroll software developers and testers who are updating their software packages to 
be compatible with PAYE reporting obligations from 2019 onwards. 


![Image 4](image_x.png)

# Page 3

 
 
3 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
## TABLE OF CONTENTS 
Audience ................................................................................................................................................................ 2 
1 
Introduction ....................................................................................................................................................... 4 
1.1 
Prerequisites .............................................................................................................................................. 4 
2 
Logging In ........................................................................................................................................................... 5 
3 
Viewing and Downloading Available Test Data ................................................................................................. 7 
4 
Employee Overview ........................................................................................................................................... 9 
4.1 
Edit Employee .......................................................................................................................................... 10 
5 
Requesting Additional Test Data ..................................................................................................................... 11 
5.1 
Request a new certificate ........................................................................................................................ 11 
5.2 
Request a specific certificate ................................................................................................................... 12 
6 
Deleting Test Data ........................................................................................................................................... 14 
7 
Creating Unemployed Customer Test Data ..................................................................................................... 15 
7.1 
Create New RPN for Unemployed Customer........................................................................................... 15 
8 
Requesting Agent Certificates ......................................................................................................................... 16 
9 
Appendix .......................................................................................................................................................... 17 
9.1 
REST API Endpoints .................................................................................................................................. 17 
9.1.1 
RPN Services .................................................................................................................................... 17 
9.1.2 
Payroll Services ................................................................................................................................ 18 
9.1.3 
Returns Reconciliations ................................................................................................................... 18 
9.2 
SOAP API Endpoints ................................................................................................................................. 19 
9.2.1 
RPN Services .................................................................................................................................... 19 
9.2.2 
Payroll Service .................................................................................................................................. 19 
9.2.3 
Returns Reconciliations ................................................................................................................... 19 
9.3 
Known Issues ........................................................................................................................................... 20 
9.3.1 
Self Service Application Login .......................................................................................................... 20 
 


![Image 5](image_5.png)

# Page 4

 
 
4 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
## 1 INTRODUCTION   
The purpose of this document is to serve as a guide to use the PIT Self Service Application.  This application 
provides developers and testers access to exclusive Revenue generated test data that is supported in the PIT 
environment. 
By using this application developers/testers can: 
• 
Download digital certificates associated with test employers required for conformance testing  
• 
Download JSON files containing data of the test employees associated with each test employer 
• 
Request additional certificates for testing 
• 
Delete test employer data 
• 
Create a test unemployed customer 
• 
Download test agent certificates with a test employer 
 
Each employer subsequently created in each environment exists only in that environment. Employers in the PIT 
current version environment will have a registration number of 8XXXXXXXH and the cert associated with them 
will be of the form 9999XXXXX. In the PIT next version environment, employers will have a registration number 
of 9XXXXXXXH and the cert associated with them will be of the form 8888XXXXX.  
 
The PIT Self Service Application can be accessed at the following URL:  
[https://softwaretest.ros.ie/paye-employers-self-service/intro](https://softwaretest.ros.ie/paye-employers-self-service/intro) 
 
 
1.1 Prerequisites  
In order to access and use the PIT Self Service Application, you need to have completed the registration process 
for the PAYE Modernisation PIT Help Desk  and indicated that you require access to PAYE Modernisation testing. 
On completion of the registration process, you will receive a digital certificate and password which will allow 
access to the PIT self service application. 
 


![Image 6](image_6.png)

# Page 5

 
 
5 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
## 2 LOGGING IN 
The login screen requires users to sign in with their Test Data Management (TDM) digital certificate and 
password provided during the registration process1.  
In order to make the digital certificate that was issued as part of the PIT registration process available in the 
‘Select Certificate’ drop down menu, it needs to be loaded into the web browser. The ‘Manage My Certificates’ 
link provides a screen that allows users to select the certificate and load it into the web browser. 
 
 
Figure 1 Login Screen Layout for PIT Current Version 
 
 
From the Login screen, a user can use the ‘Select Certificate’ drop down menu to choose the certificate to use. 
Once the appropriate certificate is selected and password is entered, clicking the ‘Authenticate’ button 
completes the sign in. On successful sign in the application takes the user to the Introduction screen of the PIT 
Self Service application.  This screen contains information about the PIT Self Service Application and the PIT 
testing process.  
 
 
1 Please note that this login screen is shared with the ROS Payroll reporting screens. User’s will be directed to the PIT 
Self Service application from this login screen if they use the Test Data Management (TDM) digital certificate/password 
provided as part of PIT registration. However, if they use digital certificates provided by the PIT Self Service application 
they will be directed to the ROS Payroll Reporting screens. 


![Image 7](image_7.png)
![Image 8](image_8.png)

# Page 6

 
 
6 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
 
Figure 2  Screen Layout of the Introduction Screen 
 
 
 
 
 
 


![Image 9](image_9.png)
![Image 10](image_10.png)

# Page 7

 
 
7 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
## 3 VIEWING AND DOWNLOADING AVAILABLE TEST DATA 
The Dashboard page as seen in Figure 4, displays a table of digital certificates and each row contains: 
• 
The Employer Number associated with the digital certificate 
• 
The number of employees linked to the employer 
• 
A link to download the digital certificate  
• 
The password for the digital certificate 
• 
The digital certificate type and status 
• 
A link to a JSON file which contains Employee details 
o First name, Surname and PPSN of all the employees linked to the employer 
• 
A link to an Employee Overview which provides simple overview of employee status and a link to modify 
employee details 
o Name, PPSN, Tac Calculation Basis, USC Status, RPN Type and a link to modify 
 
The screen also allows users to: 
• 
Request New Certificates with random RPNs assigned to each employee.  
• 
Request Specific Certificates with specified RPNs assigned to each employee.  
• 
Delete an employer  
• 
Create an unemployed customer - a PPSN not linked to a digital certificate and so can be used as part of 
testing the Request New RPN process.  
• 
Create an unemployed customer with a fada guaranteed to be in their name.  
• 
Please note that on first login, the dashboard will contain a single digital certificate however additional 
certificates can be added by using the ‘Request New Certificates’ or ‘Request Specific Certificates 
buttons’. 
             
 
 
 
 


![Image 11](image_11.png)

# Page 8

 
 
8 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
Figure 3 Screen Layout of the Dashboard 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


![Image 12](image_12.png)
![Image 13](image_13.png)

# Page 9

 
 
9 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
## 4 EMPLOYEE OVERVIEW 
The Employee overview page is accessed by clicking either the employer’s name link or the ‘overview’ link on 
the dashboard. This page shows users an overview of all employees associated with this employer, as seen in 
Figure 5. By clicking ‘Edit’ in the Modify column of this page, the user can modify the RPN of this specific 
employee. Any field that is populated with ‘undefined’ has not had that value set yet, which is the case for any 
employer created using the ‘Request Certificate’ button.  
 
 
Figure 4 


![Image 14](image_14.png)
![Image 15](image_15.png)

# Page 10

 
 
10 
 
 
PAYE Modernisation – PIT Self Service Application Guide 
4.1 Edit Employee 
This page will display the name, PPSN, Tax Calculation Basis, USC Status and RPN Type for the selected 
employee. From here, users can also change the RPN Profile of the selected employee by selecting tax 
calculation basis, USC Status and the desired RPN type from the drop down to simulate transitions in the 
employee’s circumstances. This will increment the RPN number of this employment. It will also automatically 
make the employee to have a single relationship status and a single employment status as these RPN types only 
count for such employees.  
 
 
Figure 4 .1 Screen Layout of the Edit Employee 
 
 
 
 
 


![Image 16](image_16.png)
![Image 17](image_17.png)

# Page 11

 
 
 
11 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
## 5 REQUESTING ADDITIONAL TEST DATA 
Users can request a new certificate by clicking the ‘Request New Certificates’ or ‘Request Specific Certificates’ 
buttons available on the Dashboard.  
5.1 Request a new certificate 
The user can create a new certificate by clicking on the ‘Request a new certificate’ button available on the 
Dashboard.  The user is brought to a new screen where they can select certificate type and the number of 
employees required. The new certificate will be created for a new Employer. This certificate and the employee 
data will be available on the Dashboard. 
 
 
Figure 5 .1 Screen Layout of the Create Custom Certificate 


![Image 18](image_18.png)
![Image 19](image_19.png)

# Page 12

 
 
 
12 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
5.2 Request a specific certificate 
The user can create an employer with employees that have a specific RPN type by clicking on the ‘Request 
Specific Certificate’ button available on the Dashboard.  The user is brought to a new screen where they can 
select the number of employees required, the tax calculation basis, USC status, RPN type and previous 
employment tax details if they need. If previous pay and tax details are not entered, the values will default to 0. 
Upon clicking the ‘Request Certificate’ button, the new certificate will be created for a new Employer. This 
certificate and the employee data will be available on the Dashboard. 
 
 
 
 
 


![Image 20](image_20.png)

# Page 13

 
 
 
13 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
 
Figure 5.2 Screen Layout of Request Specific Certificate 


![Image 21](image_21.png)
![Image 22](image_22.png)

# Page 14

 
 
 
14 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
## 6 DELETING TEST DATA 
The user can delete test data by clicking on the ‘Delete Employer’ button available on the Dashboard.  The user 
is brought to a new screen where they can select an Employer Tax Registration Number from the drop-down list 
and delete all data related to that Employer. The list of Employer Tax Registration Numbers corresponds to the 
available Employer Tax Registration Numbers on the Dashboard. 
 
 
Figure 6 Screen Layout of the Delete Employer Screen  
 
 


![Image 23](image_23.png)
![Image 24](image_24.png)

# Page 15

 
 
 
15 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
## 7 CREATING UNEMPLOYED CUSTOMER TEST DATA 
Users can create test employees who have yet to be associated with any test employment by clicking on the 
‘Create Unemployed Customer’ button available on the Dashboard. The user is brought to a new screen where 
they can view the result2 of their request to create a new employee not linked to an employment.  Unemployed 
customers can be used as part of testing the New RPN process.  
 
Figure 7 Screen Layout of the Create Unemployed Customer Screen 
 
Customers who will have a fada in their name can also be created using the self-service application. The process 
for adding an employment for this new customer is described in the next section. 
 
7.1 Create New RPN for Unemployed Customer 
Once you have created an unemployed customer and recorded their details. Create New RPN request should be 
sent with the details of the unemployed customer to have them added as an employee under an employer. 
A Create New RPN request should be submitted before trying to Lookup RPN for that customer. The endpoint to 
send the request to can be found below in the appendix section. 
 
 
 
2 It is recommended that the returned test employee details are noted by the user as clicking the ‘Create Unemployed 
Customer’ button again will result in a new test employee being displayed here. 


![Image 25](image_25.png)
![Image 26](image_26.png)

# Page 16

 
 
 
16 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
## 8 REQUESTING AGENT CERTIFICATES 
Users can request a new Agent certificate by clicking the ‘Request New Certificates’ button available on the 
Dashboard. They can specify the Agent certificate type and the number of employees required. The new Agent 
certificate will be created along with a new Employer. This certificate and the employee data will be available on 
the Dashboard. 
 
 
Figure 8 Screen Layout of the Create Custom Agent Certificate 
 
 


![Image 27](image_27.png)
![Image 28](image_28.png)

# Page 17

 
 
 
17 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
## 9 APPENDIX 
This appendix provides the set of REST and SOAP web service endpoints for the Payroll and RPN services 
available for testing in the Public Interface Testing environment. 
 
9.1 REST API Endpoints  
 
9.1.1 RPN Services  
9.1.1.1 
POST – Create New RPN 
[https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}?softwareUsed={SoftwareName}&softwareVer
sion={softwareVersion} 
 
Example: [https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/rpn/00001013N/2018?softwareUsed=abc&softwareVersion=1.0  
 
9.1.1.2 
GET – Look Up RPN 
[https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}?softwareUsed={SoftwareName}&softwareVer
sion={softwareVersion} 
Example: [https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/rpn/03390656OH/2018?softwareUsed=1&softwareVersion=1.0   
 
9.1.1.3 
GET – Look Up RPN by employee 
[https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}/{employeeId}?softwareUsed={SoftwareName}
&softwareVersion={softwareVersion} 
Example: [https://softwaretest.ros.ie/paye-employers/v1/rest/rpn/03390656OH/2018/01092485G-](https://softwaretest.ros.ie/paye-employers/v1/rest/rpn/03390656OH/2018/01092485G-)
2?softwareUsed=1&softwareVersion=1.0  
 
9.1.1.4 
GET – Look Up RPN by employer using optional filters date last updated and/or employee Ids 
[https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}?softwareUsed={SoftwareName}&softwareVer
sion={softwareVersion}&employeeIDs={employeeId1},{employeeId2}&dateLastUpdated={date}  
Example: [https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/rpn/03390656OH/2018?softwareUsed=1&softwareVersion=1&employeeIDs=00202020PA-
1,7002439CA-2&dateLastUpdated=2018-02-01   
 


![Image 29](image_29.png)

# Page 18

 
 
 
18 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
9.1.2 Payroll Services 
9.1.2.1 
POST - Payroll Submission 
[https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/payroll/{employerRegistrationNumber}/{taxYear}/{payrollRunReference}/{SubmissionID}?sof
twareUsed={softwareName}&softwareVersion={softwareVersion}   
Example: [https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/payroll/00087900D/2018/PayrollRun1/Submission01?softwareUsed=abc&softwareVersion=
1.0   
9.1.2.2 
GET – Check Payroll Submission 
[https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/payroll/{employerRegistrationNumber}/{taxYear}/{PayrollRunReference}/{SubmissionID}?sof
twareUsed={softwareName}&softwareVersion={softwareVersion}  
Example: [https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/payroll/00087900D/2018/PayrollRun1/Submission01?softwareUsed=abc&softwareVersion=
1.0  
 
9.1.2.3 
GET – Check Payroll Run 
[https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/payroll/{employerRegistration}/{taxYear}/{PayrollRunReference}?softwareUsed={softwareNa
me}&softwareVersion={softwareVersion}   
Example: [https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/payroll/00087900D/2018/PayrollRun1?softwareUsed=abc&softwareVersion=1.0  
 
9.1.3 Returns Reconciliations 
[https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/returns_reconciliation/{employerRegistration}?softwareUsed={softwareName}&periodStart
Date={periodStartDate}&periodEndDate={periodEndDate}&softwareVersion={softwareVersion} 
Example: [https://softwaretest.ros.ie/paye-](https://softwaretest.ros.ie/paye-)
employers/v1/rest/returns_reconciliation/03497992DH?softwareUsed=abc&periodStartDate=2019-04-
01&periodEndDate=2019-04-30&softwareVersion=1 
 
 
 
 


![Image 30](image_30.png)

# Page 19

 
 
 
19 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
9.2 SOAP API Endpoints 
 
9.2.1 RPN Services  
[https://softwaretest.ros.ie/paye-employers/v1/soap/rpn](https://softwaretest.ros.ie/paye-employers/v1/soap/rpn)  
 
9.2.2 Payroll Service 
[https://softwaretest.ros.ie/paye-employers/v1/soap/payroll](https://softwaretest.ros.ie/paye-employers/v1/soap/payroll)  
 
9.2.3 Returns Reconciliations 
[https://softwaretest.ros.ie/paye-employers/v1/soap/returns_reconciliation](https://softwaretest.ros.ie/paye-employers/v1/soap/returns_reconciliation) 
 
 
 
 


![Image 31](image_31.png)

# Page 20

 
 
 
20 
 
 
PAYE Modernisation – PIT Self-Service Application Guide 
9.3 Known Issues 
 
9.3.1 Self Service Application Login  
On clicking the ‘register for ROS’ link on the Self Service Application login page in PIT3 a ‘503 service unavailable’ 
page is displayed to the user. 
 
 
 


![Image 32](image_32.png)

