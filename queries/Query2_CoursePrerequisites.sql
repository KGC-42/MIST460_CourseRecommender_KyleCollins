-- Query 2: What are the prerequisites for a specific course?
-- Shows all required courses and minimum grades
-- MIST 460 In-Class Assignment
-- Student: Kyle Collins

USE Mist460_RDB_Collins;
GO

-- Change these to test different courses
DECLARE @SubjectCode NVARCHAR(10) = 'MIST';   -- e.g., 'MIST', 'CS', 'MATH'
DECLARE @CourseNumber NVARCHAR(10) = '460';    -- e.g., '460', '201', '101'

SELECT 
    c1.SubjectCode + ' ' + c1.CourseNumber AS Course,
    c1.Title AS CourseTitle,
    c2.SubjectCode + ' ' + c2.CourseNumber AS PrerequisiteCourse,
    c2.Title AS PrerequisiteTitle,
    cp.MinGrade AS MinimumGrade,
    c2.Credits AS PrerequisiteCredits
FROM Course c1
INNER JOIN CoursePrereq cp ON c1.CourseID = cp.CourseID
INNER JOIN Course c2 ON cp.PrereqID = c2.CourseID
WHERE c1.SubjectCode = @SubjectCode 
  AND c1.CourseNumber = @CourseNumber
ORDER BY c2.SubjectCode, c2.CourseNumber;
GO

-- Alternative: Show message if no prerequisites exist
IF NOT EXISTS (
    SELECT 1 
    FROM Course c1
    INNER JOIN CoursePrereq cp ON c1.CourseID = cp.CourseID
    WHERE c1.SubjectCode = @SubjectCode 
      AND c1.CourseNumber = @CourseNumber
)
BEGIN
    SELECT 
        @SubjectCode + ' ' + @CourseNumber AS Course,
        'No prerequisites required' AS Message;
END
GO