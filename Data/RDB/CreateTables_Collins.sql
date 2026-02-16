use Mist460_RDB_Collins;
GO

-- Drop tables if they exist
if object_id('Student') is not null
    drop table Student;
if object_id('Appuser') is not null
    drop table Appuser;
GO

create table Appuser
(
    AppuserID int identity(1,1),
    FirstName nvarchar(50) not null,
    LastName nvarchar(50) not null,
    Email nvarchar(255) not null,
    PhoneNumber nvarchar(20) null,
    PasswordHash nvarchar(255) not null,
    UserRole nvarchar(20) not null,
    CONSTRAINT PK_Appuser primary key (AppuserID),
    CONSTRAINT UE_Appuser_Email UNIQUE (Email),
    CONSTRAINT CK_Appuser_UserRole CHECK (UserRole in ('Student', 'Advisor', 'Admin'))
);
GO

create table Student
(
    StudentID int identity(1,1),
    AppuserID int not null,
    TotalCreditsCompleted int not null default 0,
    GraduateYear nvarchar(4) not null,
    OverallGPA decimal(3,2) not null default 0.00,
    AdjustedGPA decimal(3,2) not null default 0.00,
    CONSTRAINT PK_Student primary key (StudentID),
    CONSTRAINT FK_Student_Appuser foreign key (AppuserID) references Appuser(AppuserID)
);
GO

-- Verify tables were created
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
GO
