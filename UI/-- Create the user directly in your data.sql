-- Create the user directly in your database (contained user)
CREATE USER APIUser WITH PASSWORD = 'MI$T460Instructor';
GO

GRANT EXECUTE TO APIUser;
GO

GRANT SELECT TO APIUser;
GO