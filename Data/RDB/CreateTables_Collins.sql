use Mist460_RDB_Collins;

GO

-- Drop tables if they exist to avoid errors when running the script multiple times
if object_id('Student') is not null
    drop table Student
if object_id('Appuser') is not null
    drop table Appuser

GO

create table Appuser
(
    AppuserID int identity(1,1),
    CONSTRAINT PK_Appuser primary key,
    FirstName nvarchar(50) not null,
    LastName nvarchar(50) not null,
    Email nvarchar(255) not null,
    CONSTRAINT UE_Appuser_Email UNIQUE(Email),
    PhoneNumber nvarchar(20) null,
    PasswordHash nvarchar(255) not null,
    UserRole nvarchar(20) not null,
    CONSTRAINT CK_Appuser_UserRole CHECK (UserRole in ('Student', 'Advisor', 'Admin'))
);

GO

create table Student
(
    StudentID int identity(1,1)
    CONSTRAINT PK_Student primary key,
    CONSTRAINT FK_Student_Appuser foreign key references Appuser(AppuserID),
    TotalCreditsCompleted int not null,
    CONSTRAINT CK_Student_CreditsCompleted default 0,
    GraduateYear nvarchar(4) not null,
    OverallGPA decimal(3,2) not null,
    CONSTRAINT CK_Student_OverallGPA default 0.00,
    AdjustedGPA decimal(3,2) not null,
    CONSTRAINT CK_Student_AdjustedGPA default 0.00
);

GO