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