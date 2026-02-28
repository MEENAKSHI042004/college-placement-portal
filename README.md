# College Placement Portal  
A Full-Stack Placement Management System Built with Django

Project Overview

The College Placement Portal is a role-based web application designed to automate and manage the complete placement lifecycle within an educational institution.

The system centralizes student management, company hiring workflows, job applications, and placement analytics into a single structured platform.

It supports three primary roles:
- Admin
- Student
- Company (via job management system)


## Technology Stack

Backend:
- Django
- Django REST Framework

Database:
- PostgreSQL

Frontend:
- Bootstrap 5
- Django Templates

Authentication:
- Django Authentication System
- Role-Based Access Control

Reporting:
- Excel Export (Multi-sheet structured reports)

## System Architecture

The project follows a modular Django architecture with separation of concerns across apps:

- accounts
- students
- companies
- applications
- reports
- stats

Each module encapsulates specific business logic to maintain scalability and clean design.

## Module Breakdown

### Module 1: Authentication & Role Management
- Secure login system
- Role-based access control (Admin / Student)
- Session management
- Protected routes
- Access restrictions based on user type



### Module 2: Student Management System
- Student profile creation and editing
- Academic record management
- Skill tracking
- Resume upload support
- Structured student dashboard



### Module 3: Company & Job Management
- Company registration and management
- Job post creation
- Eligibility criteria (Branch / Year / CGPA)
- Job listings dashboard
- Detailed job views


### Module 4: Application & Status Tracking
- Students apply to eligible jobs
- Application lifecycle tracking
- Status updates
- Admin-level application management
- Detailed application view (student and admin)



### Module 5: Placement Analytics Dashboard
- Company-wise placement statistics
- Branch-wise analysis
- Year-wise placement insights
- Placement ratio tracking
- Structured reporting interface


### Module 6: Excel Reporting Engine
- Multiple types of downloadable reports
- Automated Excel generation
- Multi-sheet comprehensive report
- Structured tabular data export


### Module 7: UI & Dashboard System
- Dedicated Admin Dashboard
- Student Dashboard
- Dynamic navigation system
- Flash messages
- Responsive layout structure
- Clean template hierarchy


## Core Features

- Full role-based system
- Complete placement workflow implementation
- Centralized student and company management
- Application tracking system
- Reporting and analytics module
- Production-ready project structure




