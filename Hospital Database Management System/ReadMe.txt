# Hospital Database Management System

## Overview
The **Hospital Database Management System** is a MySQL-based project designed to efficiently store and manage data related to hospitals, job positions, candidates, and interviews. This system allows hospitals to advertise open positions, track candidate applications, schedule interviews, and manage hiring decisions.

## Features
### Data Structure
- **Hospital Details**
  - Unique Hospital Identifier
  - Hospital Name
  - Address
  - Contact Information
- **Candidate Details**
  - Unique Candidate Identifier
  - First Name, Last Name
  - Address & Contact Information
  - List of Skills
- **Job Position Details**
  - Unique Position Identifier
  - Position Type
  - Associated Hospital
  - Required Skills
- **Interview Management**
  - Scheduling of Interviews
  - Candidate-Position Mapping
  - Hiring Status Tracking

### Relationships and Constraints
- Hospitals can request multiple interviews for a position.
- Candidates can be invited to multiple interviews.
- Hospitals can hire multiple candidates for various positions.
- Each candidate can have multiple skills.
- Each position can require multiple skills.
- Interviews take place on specific dates.

## Implementation Details
### 1. Database Creation
- Developed using **MySQL Workbench**.
- The database follows a structured relational model with primary and foreign key constraints.

### 2. Table Structure
- Properly normalized tables ensuring data integrity.
- Data types optimized for performance.
- Minimum **10 sample records** per table for demonstration.

### 3. Stored Procedures
- Custom **stored procedures** to insert new records efficiently.
- Parametric queries to facilitate controlled data insertion.

### 4. Query Functionality
The system provides key insights and functionalities, including:
1. Search hospitals by their unique identifier or name.
2. Search candidates by surname.
3. Identify candidates with skills required for specific positions.
4. Count the number of candidates who have received job offers.
5. Identify positions requiring a specific skill.
6. Track the number of positions that require nursing skills.
7. List positions sorted by their advertising hospitals.
8. Retrieve interviews that occurred on a given date.
9. Identify candidates interviewed only on a specific date.
10. Find candidates who were interviewed at least twice.

### 5. Database Export
- The project is exported as a **self-contained `.sql` file**.
- The file is structured for easy import into MySQL Workbench.

### 6. Project Documentation
Comprehensive documentation includes:
- **Project Overview**
- **Assumptions and Constraints**
- **Entity-Relationship (ER) Diagram**
- **Database Schema Explanation**

## Getting Started
### Prerequisites
- **MySQL Server & MySQL Workbench** installed.
- Basic understanding of SQL queries and database design.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hospital-db.git
   ```
2. Import the `.sql` file into MySQL Workbench.
3. Run the queries and stored procedures as needed.

### Running Queries
1. Open MySQL Workbench.
2. Load the database.
3. Execute the stored procedures for data retrieval and management.

## Future Enhancements
- Implement a web-based UI for hospital and candidate interactions.
- Add authentication and role-based access control.
- Integrate analytics for better decision-making.

---
Developed and maintained by Herman Dolhyi as part of **UCD HDip in Computer Science** coursework.

