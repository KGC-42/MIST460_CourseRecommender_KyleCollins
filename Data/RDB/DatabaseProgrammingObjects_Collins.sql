USE Mist460_RDB_Collins;
GO

DECLARE @SubjectCode NVARCHAR(10) = N'MIST';
DECLARE @CourseNumber NVARCHAR(10) = N'460';

SELECT 
    c.SubjectCode + N' ' + c.CourseNumber AS Course,
    c.Title AS CourseTitle,
    s.SectionNumber,
    s.CRN,
    i.FirstName + N' ' + i.LastName AS Instructor,
    s.SectionSemester,
    s.SectionYear,
    s.RemainingOpenings,
    s.SectionAverageRating
FROM Course c
INNER JOIN Section s ON c.CourseID = s.CourseID
INNER JOIN Instructor i ON s.InstructorID = i.InstructorID
WHERE c.SubjectCode = @SubjectCode 
  AND c.CourseNumber = @CourseNumber
  AND s.SectionSemester = N'Spring'
  AND s.SectionYear = 2026
ORDER BY s.SectionNumber;
GO


USE Mist460_RDB_Collins;
GO

DECLARE @SubjectCode NVARCHAR(10) = N'MIST';
DECLARE @CourseNumber NVARCHAR(10) = N'460';

SELECT 
    c1.SubjectCode + N' ' + c1.CourseNumber AS Course,
    c1.Title AS CourseTitle,
    c2.SubjectCode + N' ' + c2.CourseNumber AS PrerequisiteCourse,
    c2.Title AS PrerequisiteTitle,
    cp.MinGrade AS MinimumGrade
FROM Course c1
INNER JOIN CoursePrereq cp ON c1.CourseID = cp.CourseID
INNER JOIN Course c2 ON cp.PrereqID = c2.CourseID
WHERE c1.SubjectCode = @SubjectCode 
  AND c1.CourseNumber = @CourseNumber
ORDER BY c2.SubjectCode, c2.CourseNumber;
GO

USE Mist460_RDB_Collins;
GO

DECLARE @StudentID INT = 1;  -- Change to test different students
DECLARE @SubjectCode NVARCHAR(10) = N'MIST';
DECLARE @CourseNumber NVARCHAR(10) = N'460';

-- Get the course we're checking
DECLARE @CourseID INT;
SELECT @CourseID = CourseID 
FROM Course 
WHERE SubjectCode = @SubjectCode AND CourseNumber = @CourseNumber;

-- Check if student has completed all prerequisites
SELECT 
    @SubjectCode + N' ' + @CourseNumber AS CourseChecking,
    c.SubjectCode + N' ' + c.CourseNumber AS PrerequisiteCourse,
    c.Title AS PrerequisiteTitle,
    cp.MinGrade AS MinGradeRequired,
    CASE 
        WHEN EXISTS (
            SELECT 1 
            FROM Registration r
            INNER JOIN Section s ON r.SectionID = s.SectionID
            WHERE r.StudentID = @StudentID 
              AND s.CourseID = c.CourseID
        ) THEN N'Completed'
        ELSE N'Not Completed'
    END AS Status
FROM CoursePrereq cp
INNER JOIN Course c ON cp.PrereqID = c.CourseID
WHERE cp.CourseID = @CourseID
ORDER BY c.SubjectCode, c.CourseNumber;

-- Summary: Can student register?
SELECT 
    CASE 
        WHEN NOT EXISTS (
            SELECT 1 
            FROM CoursePrereq cp
            WHERE cp.CourseID = @CourseID
            AND cp.PrereqID NOT IN (
                SELECT DISTINCT s.CourseID
                FROM Registration r
                INNER JOIN Section s ON r.SectionID = s.SectionID
                WHERE r.StudentID = @StudentID
            )
        ) THEN N'Yes - All prerequisites completed'
        ELSE N'No - Missing prerequisites'
    END AS CanRegister;
GO
```

---

# WHAT THIS DOES

**Part 1:** Shows each prerequisite and whether the student completed it
**Part 2:** Final Yes/No answer - can the student register?

**Example output:**
```
PrerequisiteCourse | Status
MIST 360          | Completed
CS 101            | Not Completed

CanRegister: No - Missing prerequisites