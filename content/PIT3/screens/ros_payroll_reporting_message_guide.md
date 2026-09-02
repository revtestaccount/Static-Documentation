# ROS Payroll Reporting Message Guide

## PAYE Modernisation

## ROS Payroll Reporting Message Guide

Version Date 24/05/2018



### Audience

This document is for any software provider who has chosen to build or update their products to allow for PAYE Modernisation and intend to submit/ or request data via ROS Payroll Reporting screens.

### Document Context

This document provides a technical overview of how to create request messages for submission to the Revenue’s PAYE Modernisation Services from the ROS Payroll Reporting screens.
This document is intended to be read in conjunction with schema definitions and example files as well as the rest of the Revenue’s PAYE Modernisation technical documentation.


|  | Latest Version History |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  | Version |  |  | Change Date |  |  | Section |  |  | Change Description |  |
|  | 1.0 |  |  |  |  |  | All |  |  | Document published. |  |
|  | 1.0 Release |  | 24/05/2018 | 24/05/2018 |  |  |  |  | Version updated to 1.0 Release Candidate 2 | Version updated to 1.0 Release |  |
|  | Candidate |  |  |  |  |  |  |  |  | Candidate 2 |  |
|  | 2 |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |


## 1. Introduction

This document is a guide on to how to create messages for submission to the PAYE Modernisation Payroll and RPN services via Revenue’s Payroll Reporting screens.



|  | Document References |  |  |  |  |
|---|---|---|---|---|---|
|  | Reference |  |  | Document Link |  |
| 1. Documents Homepage | 1. Documents Homepage |  |  | https://revenue-ie.github.io/paye-employers-documentation/ |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |


## 2. JSON Messages

A JSON envelope schema has been defined which will facilitate using JSON message format for file upload on the ROS Payroll Reporting screens to complete the following actions:

- Look up RPNs for existing employees - Create RPNs for new employees - Make a payroll submission This JSON envelope schema is required as takes in data items for these services which are provided as part of the URL if the service is invoked from the REST API.

### JSON Message – Data Items


|  | Name |  |  | Description |  |  | Applicable Message |  |
|---|---|---|---|---|---|---|---|---|
| Request type | Request type |  |  | Specifies the service to be called. Supported values : |  | All | All |  |
|  |  |  |  | "lookupRPN", "createRPN", "payrollSubmission" |  |  |  |  |
| Employer Registration Number |  |  |  | The registration of the employer (up to 9 chars). |  | All |  |  |
|  |  |  |  | Must be valid Employer Registered number. Format |  |  |  |  |
|  |  |  |  | is 7 digits (including leading zeros) followed by either |  |  |  |  |
|  |  |  |  | 1 or 2 letters |  |  |  |  |
|  | Tax Year |  |  | Tax Year to which the submission or request relates |  |  | All |  |
|  | Date Last |  | Date to lookup for RPNs updated on or since | Date to lookup for RPNs updated on or since |  | Look up RPN | Look up RPN |  |
|  | Updated |  |  |  |  |  |  |  |
| Software Used | Software Used |  |  | References to third party software used to make |  | All |  |  |
|  |  |  |  | RPN request / payroll submission |  |  |  |  |
| Software Version |  |  |  | Version of software used to make request RPN |  | All |  |  |
|  |  |  |  | request/ submission |  |  |  |  |
| Agent TAIN |  |  | Used to identify the agent submitting on behalf of the employer and to ensure that an agent link exists for this employer agent relationship for the period that the payroll submission relates to. | Used to identify the agent submitting on behalf of |  |  | To be included if the |  |
|  |  |  |  | the employer and to ensure that an agent link exists |  |  | RPN request or |  |
|  |  |  |  | for this employer agent relationship for the period |  |  | Payroll submission |  |
|  |  |  |  | that the payroll submission relates to. |  |  | is being performed |  |
|  |  |  |  |  |  |  | by an agent on |  |
|  |  |  |  |  |  |  | behalf of an |  |
|  |  |  |  |  |  |  | Employer |  |
|  | Payroll Run |  |  | Used to identify the Payroll event that the |  | Payroll Submission | Payroll Submission |  |
|  | Reference |  |  | submission refers to e.g. ‘Site 1 Week 1’. |  |  |  |  |
| Submission ID | Submission ID |  |  | Unique submission identifier. Must be unique for |  | Payroll Submission |  |  |
|  |  |  |  | submissions under a given employer's PAYE |  |  |  |  |
|  |  |  |  | registration number. For batch submissions, all |  |  |  |  |
|  |  |  |  | submissions should have the same SubmissionID and |  |  |  |  |
|  |  |  |  | should have the BatchID and BatchCount populated. |  |  |  |  |
| Employee IDs |  |  |  | Employee's PPS Number and Employee's |  |  | Look up RPN – To |  |
|  |  |  |  | Employment ID(Unique identifier for each distinct |  |  | be included if |  |
|  |  |  |  | employment for an employee) are joined using a |  |  | request is for |  |
|  |  |  |  | hyphen (eg.'1234567T-1'). |  |  | specific Employees |  |
| Request Body |  |  |  | For Payroll submissions, this contains the Employee |  |  | Payroll Submission, |  |
|  |  |  |  | level details. For Create RPNs (NewRPN), this |  |  | Create RPN |  |


| Employer |
|---|
| Registration |
| Number |


## 3. XML Messages

There is no requirement for an XML envelope schema as the schemas defined for PAYE Modernisation web services can also be used to create messages for upload through the ROS Payroll Reporting screens. The following XML messages are supported through the ROS Payroll Reporting screens:

- Look up RPNs for existing employees - Create RPNs for new employees - Make a payroll submission

## 4. Schemas

## 5. Digital Signature

Messages uploaded through the ROS Payroll Reporting screens do not need to be digitally signed prior to the upload. The ROS Payroll Reporting screens will perform the digital signing as part of the upload process.



|  | contains the Employee level details. |  | (NewRPN) |  |
|---|---|---|---|---|
|  |  |  |  |  |


|  | Reference |  |  | Document Link |  |
|---|---|---|---|---|---|
| JSON Envelope Schema | JSON Envelope Schema |  |  | https://revenue-ie.github.io/paye-employers- |  |
|  |  |  |  | documentation//Screens/ROS_Payroll_Reporting_JSON_Envelope_schema.json |  |
|  |  |  |  |  |  |
| JSON Create RPN (Request body) |  |  |  | https://revenue-ie.github.io/paye-employers-documentation/rest/paye- |  |
|  |  |  |  | employers-rest-api.json |  |
|  |  |  |  |  |  |
| JSON Payroll Submission (Request body) |  |  |  | https://revenue-ie.github.io/paye-employers-documentation/rest/paye- |  |
|  |  |  |  | employers-rest-api.json |  |
|  |  |  |  |  |  |
| XML Look up RPNs |  |  |  | https://revenue-ie.github.io/paye-employers-documentation/soap/v1/rpn/rpn- |  |
|  |  |  |  | schema.xsd |  |
|  |  |  |  |  |  |
|  | XML Create RPNs for |  |  | https://revenue-ie.github.io/paye-employers-documentation/soap/v1/rpn/rpn- |  |
|  | new employees (New |  |  | schema.xsd |  |
|  | RPNs) |  |  |  |  |
| XML Payroll submission | XML Payroll submission |  |  | https://revenue-ie.github.io/paye-employers- |  |
|  |  |  |  | documentation/soap/v1/payroll/payroll-schema.xsd |  |
|  |  |  |  |  |  |


| JSON Create RPN |
|---|
| (Request body) |
| (Request body) |


