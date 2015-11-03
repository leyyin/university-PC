CREATE TABLE Users (
  userID   INT PRIMARY KEY,
  name     VARCHAR(50),
  email    VARCHAR(100),
  password VARCHAR(20),
  roleID   INT,
  FOREIGN KEY (roleID) REFERENCES Roles (roleID)
);

CREATE TABLE Roles (
  roleID INT PRIMARY KEY,
  title  VARCHAR(20)
);

CREATE TABLE Courses (
  courseID  INT PRIMARY KEY,
  name      VARCHAR(50),
  subjectID INT,
  FOREIGN KEY (subjectID) REFERENCES Subjects (subjectID),
  userID    INT,
  FOREIGN KEY (userID) REFERENCES Users (UserID),
  startDate DATE,
  endDate   DATE
);


CREATE TABLE Subjects (
  subjectID INT PRIMARY KEY,
  name      VARCHAR(20)
);

CREATE TABLE Enrollment (
  userID     INT,
  FOREIGN KEY (userID) REFERENCES Users (userID),
  courseID   INT,
  FOREIGN KEY (courseID) REFERENCES Courses (courseID),
  PRIMARY KEY (userID, courseID),
  enrollDate DATE
);

CREATE TABLE Resources (
  resourceID INT PRIMARY KEY,
  name       VARCHAR(40),
  path       VARCHAR(200)
);

CREATE TABLE Lectures (
  lectureID    INT PRIMARY KEY,
  name         VARCHAR(50),
  courseID     INT,
  FOREIGN KEY (courseID) REFERENCES Courses (courseID),
  lectureDate  DATE,
  lectureIndex INT,
  resourceID   INT,
  FOREIGN KEY (resourceID) REFERENCES Resources (resourceID)
);

CREATE TABLE Assignments (
  assignmentID INT PRIMARY KEY,
  name         VARCHAR(20),
  description  VARCHAR(1000),
  deadline     DATE
);

CREATE TABLE Delivery (
  deliveryID INT PRIMARY KEY,
  type       VARCHAR(100)
);

CREATE TABLE UserAssignment (
  assignmentID INT,
  FOREIGN KEY (assignmentID) REFERENCES Assignments (assignmentID),
  userID       INT,
  FOREIGN KEY (userID) REFERENCES Users (userID),
  PRIMARY KEY (userID, assignmentID),
  deliveryID   INT,
  FOREIGN KEY (deliveryID) REFERENCES Delivery (deliveryID)
);

CREATE TABLE Tests (
  testID      INT PRIMARY KEY,
  name        VARCHAR(200),
  description VARCHAR(1000),
  deadline    DATE,
  questionID  INT,
  FOREIGN KEY (questionID) REFERENCES Questions (questionID)
);

CREATE TABLE Questions (
  questionID    INT PRIMARY KEY,
  questionIndex INT,
  type          VARCHAR(200)
);

CREATE TABLE UserTest (
  userID    INT,
  FOREIGN KEY (userID) REFERENCES Users (userID),
  testID    INT,
  FOREIGN KEY (testID) REFERENCES Tests (testID),
  PRIMARY KEY (userID, testID),
  dateTaken DATE
);

CREATE TABLE Groups (
  groupID   INT PRIMARY KEY,
  groupName VARCHAR(200)
);

CREATE TABLE UserGroup (
  userID  INT,
  FOREIGN KEY (userID) REFERENCES Users (userID),
  groupID INT,
  FOREIGN KEY (groupID) REFERENCES Groups (groupID),
  PRIMARY KEY (userID, groupID)
);

CREATE TABLE Thread (
  threadID   INT PRIMARY KEY,
  title      VARCHAR(200),
  userID     INT,
  FOREIGN KEY (userID) REFERENCES Users (userID),
  threadDate DATE,
  priorityID INT,
  FOREIGN KEY (priorityID) REFERENCES Priority (priorityID)
);

CREATE TABLE Priority (
  priorityID INT PRIMARY KEY,
  name       VARCHAR(100)
);

CREATE TABLE Post (
  postID   INT PRIMARY KEY,
  threadID INT,
  FOREIGN KEY (threadID) REFERENCES Thread (threadID),
  userID   INT,
  FOREIGN KEY (userID) REFERENCES Users (userID),
  postDate DATE,
  comment  VARCHAR(100)
);

CREATE TABLE Rating (
  userID INT,
  FOREIGN KEY (userID) REFERENCES Users (userID),
  postID INT,
  FOREIGN KEY (postID) REFERENCES Post (postID),
  PRIMARY KEY (userID, postID),
  value  INT
);
