# Connectivity Testing

## Conformance Test Scenarios –
## Connectivity Testing


## PAYE Modernisation

### Contents

Version 1.0 Release Candidate 2 Version Date 19/06/2018


### Audience

This document is aimed at payroll software developers and testers who are updating their software packages to be compatible with PAYE reporting obligations from 2019 onwards.

### Document context

This document is one of the three documents published to describe the test scenarios that will be supported by Revenue in a dedicated Public Interface Testing environment for the PAYE Modernisation Programme.  The following documents will be published in regards of testing activities related to the PAYE Modernisation Programme:

1. PAYE Modernisation  - Connectivity testing (This document)
2. PAYE Modernisation  - Basic Business Process testing
3. PAYE Modernisation  - Complex Business Process testing

This document is designed to be read in conjunction with the SOAP and REST example files as well as the rest of the Revenue Commissioners’ PAYE Modernisation documentation suite including the relevant technical documents.

### Document purpose

This document defines the Revenue supported test scenarios that can be executed within the Public Interface Test environment.  This document does not outline the business processes to be followed when running payroll.




|  | Version History |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  | Version |  |  | Change Date |  |  | Section |  |  | Change Description |  |
|  | 0.1 |  |  | 26/02/2018 |  |  | All |  |  | Initial draft |  |
|  | 1.0 Release |  | 17/05/2018 | 17/05/2018 |  |  |  |  | Version updated to 1.0 Release Candidate 2 | Version updated to 1.0 Release |  |
|  | Candidate |  |  |  |  |  |  |  |  | Candidate 2 |  |
|  | 2 |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | 19/06/2018 |  |  | Payslip |  |  | Changed to ‘submission item’ |  |


|  | Document References |  |  |  |  |
|---|---|---|---|---|---|
|  | Reference |  |  | Document Link |  |
|  | 1. Documents Homepage |  |  | Documents Homepage |  |
|  |  |  |  |  |  |
|  | Acronym |  |  | Meaning |  |
|  | PIT |  |  | Public Interface Testing |  |
|  | PAYE |  |  | Pay As You Earn |  |
|  | RPN |  |  | Revenue Payroll Notification |  |
|  | SOAP |  |  | Simple Object Access Protocol |  |
|  | REST |  |  | Representational State Transfer |  |


## 1. Introduction

The Documents Homepage specified in Document References is home to all technical and functional specification documentation and examples for the PAYE Modernisation programme.  This documentation has been made available to enable payroll software developers update their software packages to be compatible with PAYE reporting obligations from January 2019. Path locations specified in this document are relative to this Homepage.

This document provides conformance test scenario examples that are supported by Revenue in its PIT environment to enable payroll software developers validate and verify that their software conforms to these Revenue specifications.

## 2. The Scope

The document specifically details the conformance test scenarios encompassing the Connectivity Testing phase for the PAYE Modernisation programme.

It is strongly recommended that that these scenarios are successfully executed before executing scenarios detailed in later Conformance Test documents.

## 3. Connectivity Test Prerequisites

A developer or tester who wishes to engage in Connectivity Testing in PIT must first ensure that they have:

1. Notified Revenue on their intention to test through registering for access to the Revenue

PAYE PIT Support Service Desk
2. Received their initial digicert that will enable them to access and reset Revenue supplied test

data from the PIT Test Data Management Service. This test data will consist of dummy employers, employees and ROS digicerts that will be supported in the PIT environment.
Further information on these tools, including access, will be provide on the Documents Homepage.

## 4. Conformance Test Scenarios for Connectivity Testing

Connectivity Testing consists of four test scenarios:

- Look Up Revenue Payroll Notification Request - Payroll Submission Request with a Single Submission Item - Revenue Payroll Notification for a New Employee - Error Message for Employer Number in incorrect format All conformance test scenarios apply to both SOAP and REST implementations unless otherwise specified.

Each test scenarios is defined using the following structure:




| Test Identifier | Test Scenario reference. If raising a specific query on a test scenario to Revenue please include this identifier in the query as this indicates whether the query relates to the SOAP or REST implementation of the scenario. |
|---|---|
| Test Purpose | A brief outline of the purpose of the test scenario. |
| Test Data Prerequisite | Required test data to execute the test scenario. |
| Test Steps | Details of the steps involved in executing the test scenario. |
| Expected Result | The expected successful outcome of the test scenario. |


### 4.1 Look Up Revenue Payroll Notification Request

### 4.2 Payroll Submission Request with a Single Submission Item




| Test Identifier | CON_LookUp_RPN_SOAP, CON_LookUp_RPN_REST |
|---|---|
| Test Purpose | Test that Revenue will respond with a Revenue Payroll Notification (RPN) response message to a Look Up Revenue Payroll Notification (RPN) Request message from an Employer |
| Test Data Prerequisite | Prepare Valid Look up RPN Request Message based on Test Employer Digi-certs and associated Test Employee Data provided by Revenue. Sample messages can be found in the following document: PAYE Modernisation Description Of Web Service Examples |
| Test Steps | 1. The Employer prepares the Look up RPN Request message for a given valid Employer Registration Number 2. The Employer submits the message to the Look up RPN webservice 3. Revenue responds with RPN Response message containing valid RPNs for each employee associated with the Employer Registration Number |
| Expected Result | The Employer receives the RPN response message with the expected set of RPNs for the given Employer Registration Number. |
| Test Purpose | Test that Revenue will respond with an Acknowledgement response message for a valid Payroll Submission Request message. |
| Test Data Prerequisite | Prepare Valid Payroll Submission Request message based on Test Employer Digi-certs and associated Test Employee Data provided by Revenue. Sample messages can be found in the following document: PAYE Modernisation Description Of Web Service Examples |
| Test Steps | 1. The Employer prepares the Payroll Submission Request message with a single submission item for a given valid Employer Registration Number 2. The Employer submits the message to the Payroll Submission webservice 3. Revenue responds with a Payroll Submission Acknowledgement Response message |
| Expected Result | The Employer receives a Payroll Submission Acknowledgement Response message. |


### 4.3 Revenue Payroll Notification for a New Employee



| Test Identifier | CON_NewRPN_SOAP, CON_NewRPN_REST, |
|---|---|
| Test Purpose | Test that Revenue will respond with a new RPN Response message for the specified valid Employer Registration Number containing specified valid new Employee PPSN |
| Test Data Prerequisite | There must be no Employer-Employee link (i.e. no employment with the employer). Data specific to this scenario is supplied via the Test Data Management Tool. A new data request will be necessary via the Test Data Management Tool to re-execute this scenario. Prepare Valid New RPN Request Message based on Test Employer Digi-certs and associated Test Employee Data provided by Revenue. Sample messages can be found in the following document: PAYE Modernisation Description Of Web Service Examples |
| Test Steps | 1. The Employer prepares the New RPN Request message for a given valid Employer Registration Number and a valid PPSN 2. The Employer submits the message to the New RPN webservice 3. Revenue responds with New RPN Response message containing the new RPN for the specified employee |
| Expected Result | The Employer receives a new RPN Response message for the given Employee PPSN. |


### 4.4 Error Message for Employer Number in incorrect format



|  | Test Identifier |  | CON_EmployerNumberValidation_SOAP, CON_EmployerNumberValidation_REST |
|---|---|---|---|
| Test Purpose |  |  | Test that Revenue will respond with an error message and description when an incorrectly formatted Employer Number is used to make a request to any of the webservices (example used below: Look up RPN Request) <e.g. 123456789> |
| Test Data Prerequisite |  |  | Prepare invalid Look up RPN Request Message (incorrectly formatted Employer Number) based on Test Certs and associated Test Employee Data provided by Revenue. Sample messages can be found in the following document: PAYE Modernisation Description Of Web Service Examples |
| Test Steps |  |  | 1. The Employer prepares a invalid Look up RPN Request message (incorrectly formatted Employer Number) using a Cert with for a given valid Employer Registration Number 2. The Employer submits the message to the Look up RPN webservice 3. Revenue responds with the validation error code 1004 and a description of the error. |
| Expected Result |  |  | The Employer receives a response message containing the error code 1004 and a description of the error. |


