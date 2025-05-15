# Page 1

 
 
 
 
 
 
 
 
Documentation Guide 
PAYE Modernisation 


![Image 1](/migrationScripts/Documentation_Guide/images/image_1.png)
![Image 2](/migrationScripts/Documentation_Guide/images/image_2.png)
![Image 3](/migrationScripts/Documentation_Guide/images/image_3.png)
![Image 4](/migrationScripts/Documentation_Guide/images/image_4.png)
![Image 5](/migrationScripts/Documentation_Guide/images/image_5.png)

# Page 2

 
2 
 
 
 
 
 
  Documentation Guide 
Contents 
 
1. 
Introduction ......................................................................................................................... 5 
2. 
Using the documents ............................................................................................................ 5 
PAYE Web Service Examples ........................................................................................................... 5 
## SOAP/XML ....................................................................................................................................... 5 
## REST/JSON ....................................................................................................................................... 6 
3. 
Version Strategy ................................................................................................................... 6 
 
 
Audience ................................................................................................................................................. 3 
Document context .................................................................................................................................. 3 
Technical documentation ....................................................................................................................... 5 
Business documentation ........................................................................................................................ 6 


![Image 6](/migrationScripts/Documentation_Guide/images/image_6.png)

# Page 3

 
3 
 
 
 
 
 
  Documentation Guide 
 
Version  
 
1.0 Release Candidate 2 
Version Date  
 
24/05/2018 
 
Version History 
Version 
Change Date 
Section 
Change Description 
1.0 
Milestone 1 
17/11/2017 
All  
Document published. 
 
 
 
Audience and Document Context 
sections added. 
 
 
 
Changed the sources of the links 
1.0 Release 
Candidate 2 
24/05/2018 
 
Version updated to 1.0 Release 
Candidate 2 
 
 
 
 
 
Audience  
This document is for any software provider who has chosen to build or update their products to 
allow for PAYE Modernisation.  
Document context  
This document provides a non-technical overview of how to use Revenue’s PAYE Modernisation 
documentation.  
 
 


![Image 7](/migrationScripts/Documentation_Guide/images/image_7.png)

# Page 4

 
4 
 
 
 
 
 
  Documentation Guide 
Document References 
Reference 
Document Link 
1. Documents Homepage 
Documents Homepage 
 
 
 
 
 
 
 
 
 
 


![Image 8](/migrationScripts/Documentation_Guide/images/image_8.png)

# Page 5

 
5 
 
 
 
 
 
  Documentation Guide 
1. Introduction 
This document is a guide to Revenue’s PAYE Modernisation documentation. It specifies the intended 
audience of the published documents and provides guidance on how the documents could be used. 
2. Using the documents 
The collection of documents is divided across four categories and two types: 
Table 1 
*The PAYE Modernisation Description Of Web Service Examples PDF may be of interest to non-
technical users – it contains business scenarios involving submission, corrections and deletions. 
Technical documentation 
Our technical documentation is intended for developers and provides technical message flows, 
SOAP/XML and REST/JSON examples of scenarios, XML schemas and REST API definitions.  
PAYE Web Service Examples 
The PAYE Modernisation Description Of Web Service Examples document provides an overview of 
the example ZIP files. Each zip file contains both XML and JSON requests and responses required to 
complete the full scenario. 
## SOAP/XML 
If developing for the SOAP/XML API Revenue would see the documentation being used as follows 
1. SOAP Web Service Integration Guide – this will provide a high level technical overview of all 
of our public APIs as well as a guide to making valid, signed and secure requests. This 
document can be used to quickly get up to speed with our SOAP API and get a high level 
view of the capabilities it provides. 
2. SOAP Web Service Integration Guide Examples – this will provide examples of specific 
scenarios. This document will give a more in-depth view of how our API is intended to work 
with specific scenario examples. 
3. SOAP Schema Reference – this is documentation generated automatically from the Payroll 
and RPN WSDL and Schema files. This would be seen as the primary development guide as it 
combines examples with easy to read versions of our WSDL and schema files. 
4. Payroll Web Service Definition , RPN Web Service Definition and Returns Web Service 
Definition provide Web Service Definition Language specifications of both the payroll and 
Category 
Type 
Audience 
PAYE Web Service Specifications (SOAP/XML) 
Technical 
Developers 
PAYE Web Service Specifications (REST/JSON) 
Technical 
Developers 
Supporting Documentation 
Non-technical 
Business 
PAYE Web Service Examples* 
Technical 
Developers 


![Image 9](/migrationScripts/Documentation_Guide/images/image_9.png)

# Page 6

 
6 
 
 
 
 
 
  Documentation Guide 
Revenue Payroll Notification services. These files will give a technical view of what services 
are being provided and the corresponding request and response types.  
5. Payroll Schema, RPN Schema , Returns Schema, and the Common PAYE Types Schema 
provide detailed breakdowns of the request and response types used in the WSDL.  
## REST/JSON 
If developing for the REST/JSON API Revenue would see the documentation being used as follows 
1. REST API Integration guide - this will provide a high level technical overview of all of our 
public APIs as well as a guide to making valid, signed and secure requests. This document 
can be used to quickly get up to speed with our REST API and get a high level view of the 
capabilities it provides. 
2. REST API Integration Guide Examples - this will provide examples of specific scenarios. This 
document will give a more in-depth view of how our API is intended to work with specific 
scenario examples. 
3. REST API Reference – this provides a complete, searchable reference for all API lookups and 
responses 
4. REST Open API Specification – this file is the Open API specification file. This file should be 
compatible with any Open API capable viewer 
Business documentation 
Our business documentation is intended to provide additional context for technical users as well as 
information for business users on the data that Revenue will be collecting and providing to run 
payroll and how this data will be validated. These documents are not intended to be comprehensive 
as they only refer to items with a business use and/or a specific validation rule. 
Business documentation is made up of the three documents under the Supporting Documentation 
category: 
• 
Payroll Submission Request: Data Items 
• 
RPN Response: Data Items 
• 
Returns and Reconciliations: Data Items 
• 
Validation Rules: Employer Submission And RPN 
 
Additionally the PAYE Modernisation Description Of Web Service Examples may be of some interest 
to business users. 
3. Version Strategy 
Our versioning strategy for both documents and schemas is as follows  
• 
Updates before our Public Interface Testing release at the end of March 2018 would 
increment the version to “1.0 Milestone 2” etc. 
• 
On the release of our services to PIT documents and schemas would update to version “1.0 
Release Candidate 1” 
• 
This change in version denotes that the services have passed internal testing and are 
available for public testing 


![Image 10](/migrationScripts/Documentation_Guide/images/image_10.png)

# Page 7

 
7 
 
 
 
 
 
  Documentation Guide 
• 
Any updates between the PIT release and go-live would increment the version to “1.0 
Release Candidate 2” etc. 
• The live release will change the version to “1.0 Final”


![Image 11](/migrationScripts/Documentation_Guide/images/image_11.png)

