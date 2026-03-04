-- Database Programming Objects (Stored Procedures, User-Defined Functions)
-- MIST460_CourseRecommender_Surendra
-- Kyle Collins

USE Mist460_RDB_Collins;
GO

-- ============================================
-- Scalar Function: Get semester name from month number
-- Returns: 'Spring', 'Summer', or 'Fall'
-- ============================================

CREATE OR ALTER FUNCTION dbo.GetSemesterFromMonth
(
    @MonthNumber int
)
RETURNS nvarchar(10)
AS
BEGIN
    DECLARE @Semester nvarchar(10);
    
    IF @MonthNumber IN (1, 2, 3, 4, 5)
        SET @Semester = 'Spring';
    ELSE IF @MonthNumber IN (6, 7)
        SET @Semester = 'Summer';
    ELSE
        SET @Semester = 'Fall';
    
    RETURN @Semester;
END;
GO

-- ============================================
-- Query 1: What are the sections of a specific course offered this semester (Spring 2026)?
-- Inputs: SubjectCode and CourseNumber (Course)
-- Conditions: Offered in Spring 2026 (Section)
-- Output: SectionID, InstructorName, SeatsAvailable (Section + Instructor)
-- ============================================

CREATE OR ALTER PROCEDURE GetCourseSectionsForSpecifiedCourse
    @SubjectCode nvarchar(10) = null,
    @CourseNumber nvarchar(10) = null
AS
BEGIN
    -- Validate inputs
    IF (@SubjectCode IS NULL AND @CourseNumber IS NOT NULL) OR 
       (@SubjectCode IS NOT NULL AND @CourseNumber IS NULL)
    BEGIN
        RAISERROR('Both @SubjectCode and @CourseNumber must be provided together, or both left NULL', 16, 1);
        RETURN;
    END;

    SELECT 
        c.SubjectCode,
        c.CourseNumber,
        c.Title AS CourseTitle,
        s.SectionNumber,
        s.CRN,
        i.FirstName + ' ' + i.LastName AS InstructorName,
        s.SectionSemester,
        s.SectionYear,
        s.RemainingOpenings AS SeatsAvailable,
        s.SectionAverageRating
    FROM Course c
    INNER JOIN Section s ON c.CourseID = s.CourseID
    INNER JOIN Instructor i ON s.InstructorID = i.InstructorID
    WHERE s.SectionSemester = 'Spring'
      AND s.SectionYear = 2026
      AND c.SubjectCode = ISNULL(@SubjectCode, c.SubjectCode)
      AND c.CourseNumber = ISNULL(@CourseNumber, c.CourseNumber)
    ORDER BY c.SubjectCode, c.CourseNumber, s.SectionNumber;
END;
GO

-- ============================================
-- Query 2: What are the prerequisites for a specific course (optional entry)?
-- ============================================

CREATE OR ALTER PROCEDURE GetCoursePrerequisites
    @SubjectCode nvarchar(10) = NULL,
    @CourseNumber nvarchar(10) = NULL
AS
BEGIN
    -- Validate inputs
    IF (@SubjectCode IS NULL AND @CourseNumber IS NOT NULL) OR 
       (@SubjectCode IS NOT NULL AND @CourseNumber IS NULL)
    BEGIN
        RAISERROR('Both @SubjectCode and @CourseNumber must be provided together, or both left NULL', 16, 1);
        RETURN;
    END;

    SELECT 
        MainCourse.SubjectCode,
        MainCourse.CourseNumber,
        MainCourse.Title AS CourseTitle,
        prereq.SubjectCode AS PrereqSubjectCode,
        prereq.CourseNumber AS PrereqCourseNumber,
        prereq.Title AS PrerequisiteTitle,
        cp.MinGrade AS MinimumGrade
    FROM CoursePrereq cp
    INNER JOIN Course MainCourse ON cp.CourseID = MainCourse.CourseID
    INNER JOIN Course prereq ON cp.PrereqID = prereq.CourseID
    WHERE MainCourse.SubjectCode = ISNULL(@SubjectCode, MainCourse.SubjectCode)
      AND MainCourse.CourseNumber = ISNULL(@CourseNumber, MainCourse.CourseNumber)
    ORDER BY MainCourse.SubjectCode, MainCourse.CourseNumber, prereq.SubjectCode, prereq.CourseNumber;
END;
GO

-- ============================================
-- Query 3: Has a specific student completed the prerequisites for a specific course?
-- Encapsulate logic inside a stored procedure
-- ============================================

CREATE OR ALTER PROCEDURE CheckStudentPrerequisites
    @StudentID INT,
    @SubjectCode nvarchar(10),
    @CourseNumber nvarchar(10)
AS
BEGIN
    -- Get the course ID
    DECLARE @CourseID INT;
    SELECT @CourseID = CourseID 
    FROM Course 
    WHERE SubjectCode = @SubjectCode AND CourseNumber = @CourseNumber;

    IF @CourseID IS NULL
    BEGIN
        RAISERROR('Course not found', 16, 1);
        RETURN;
    END;

    -- Check each prerequisite
    SELECT 
        @SubjectCode + ' ' + @CourseNumber AS CourseChecking,
        prereq.SubjectCode + ' ' + prereq.CourseNumber AS PrerequisiteCourse,
        prereq.Title AS PrerequisiteTitle,
        cp.MinGrade AS MinGradeRequired,
        CASE 
            WHEN EXISTS (
                SELECT 1 
                FROM Registration r
                INNER JOIN Section s ON r.SectionID = s.SectionID
                WHERE r.StudentID = @StudentID 
                  AND s.CourseID = prereq.CourseID
            ) THEN 'Completed'
            ELSE 'Not Completed'
        END AS Status
    FROM CoursePrereq cp
    INNER JOIN Course prereq ON cp.PrereqID = prereq.CourseID
    WHERE cp.CourseID = @CourseID
    ORDER BY prereq.SubjectCode, prereq.CourseNumber;

    -- Overall eligibility check
    SELECT 
        @SubjectCode + ' ' + @CourseNumber AS Course,
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
            ) THEN 'Yes - All prerequisites completed'
            ELSE 'No - Missing prerequisites'
        END AS CanRegister;
END;
GO

-- ============================================
-- Test the scalar function
-- ============================================

-- Test the semester function
SELECT dbo.GetSemesterFromMonth(1) AS January;    -- Should return 'Spring'
SELECT dbo.GetSemesterFromMonth(6) AS June;       -- Should return 'Summer'
SELECT dbo.GetSemesterFromMonth(9) AS September;  -- Should return 'Fall'
GO

-- ============================================
-- Test the stored procedures
-- ============================================

-- Test Query 1: Get sections for MIST 460
EXEC GetCourseSectionsForSpecifiedCourse @SubjectCode = 'MIST', @CourseNumber = '460';

-- Test Query 2: Get prerequisites for MIST 460
EXEC GetCoursePrerequisites @SubjectCode = 'MIST', @CourseNumber = '460';

-- Test Query 3: Check if Student 1 has completed prerequisites for MIST 460
EXEC CheckStudentPrerequisites @StudentID = 1, @SubjectCode = 'MIST', @CourseNumber = '460';
GO