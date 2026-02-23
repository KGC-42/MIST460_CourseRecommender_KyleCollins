-- Query 1: Find courses a specific student has registered for
-- Shows courses offered Spring 2026
-- MIST 460 In-Class Assignment
-- Student: Kyle Collins

USE Mist460_RDB_Collins;
GO

-- Change @StudentID to test different students
DECLARE @StudentID INT = 1;
DECLARE @Semester NVARCHAR(12) = 'Spring';
DECLARE @Year INT = 2026;

SELECT 
    r.RegistrationID,
    r.RegistrationDate,
    a.Firstname + ' ' + a.Lastname AS StudentName,
    c.SubjectCode + ' ' + c.CourseNumber AS Course,
    c.Title AS CourseTitle,
    c.Credits,
    sec.SectionNumber,
    i.FirstName + ' ' + i.LastName AS Instructor,
    sec.SectionSemester,
    sec.SectionYear,
    sec.CRN,
    sec.RemainingOpenings,
    sec.SectionAverageRating
FROM Registration r
INNER JOIN Student st ON r.StudentID = st.StudentID
INNER JOIN AppUser a ON st.StudentID = a.AppUserID
INNER JOIN Section sec ON r.SectionID = sec.SectionID
INNER JOIN Course c ON sec.CourseID = c.CourseID
INNER JOIN Instructor i ON sec.InstructorID = i.InstructorID
WHERE r.StudentID = @StudentID
  AND sec.SectionSemester = @Semester
  AND sec.SectionYear = @Year
ORDER BY c.SubjectCode, c.CourseNumber;
GO