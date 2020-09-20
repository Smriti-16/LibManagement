TABLE BOOKS:

CREATE TABLE Books (
ISBN INT NOT NULL ,
book_name VARCHAR( 100 ) NOT NULL ,
book_status CHAR(1) NOT NULL,
num_of_copies INT NOT NULL ,
book_genre INT NOT NULL,
book_edition INT NOT NULL ,
book_publisher_id INT NOT NULL ,
PRIMARY KEY ( ISBN )
);

TABLE GENRE:

CREATE TABLE Genre (
book_genre_id INT NOT NULL ,
book_genre_name VARCHAR( 50 ) NOT NULL,
PRIMARY KEY ( book_genre_id )
);


TABLE AUTHOR:

CREATE TABLE Author (
author_id INT NOT NULL,
author_name VARCHAR ( 100 ) NOT NULL ,
PRIMARY KEY ( author_id )
);

TABLE PUBLISHER:

CREATE TABLE Publisher (
publisher_id INT NOT NULL,
publisher_name VARCHAR (100) NOT NULL,
PRIMARY KEY ( publisher_id )
);

TABLE BOOK_AUTHOR:

CREATE TABLE Book_Author (
book_id INT NOT NULL ,
author_id INT NOT NULL
);

RELATION BW THE ABOVE CREATED TABLES:

ALTER TABLE Books ADD FOREIGN KEY (book_genre) REFERENCES Genre (book_genre_id) ;
ALTER TABLE Books ADD FOREIGN KEY ( `book_publisher_id` ) REFERENCES Publisher( publisher_id ) ;
ALTER TABLE Book_Author ADD FOREIGN KEY ( book_id ) REFERENCES Books( ISBN ) ;
ALTER TABLE Book _ Author ADD FOREIGN KEY ( author_id ) REFERENCES Author( author_id ) ;


TABLE STUDENT:

CREATE TABLE Student (
student_id VARCHAR(100) NOT NULL ,
student_name VARCHAR( 50 ) NOT NULL ,
student_email VARCHAR( 100 ) NOT NULL ,
PRIMARY KEY (student_id )
);

TABLE LIBRARIAN:

CREATE TABLE Librarian (
librarian_id INT NOT NULL ,
librarian_name VARCHAR( 50 ) NOT NULL ,
librarian_email VARCHAR( 100 ) ,
PRIMARY KEY ( `librarian_id` )
);

TABLE BORROW:

CREATE TABLE Borrow (
borrow_id INT NOT NULL ,
student_id INT NOT NULL ,
ISBN INT NOT NULL ,
librarian_id INT NOT NULL ,
borrow_date DATE NOT NULL ,
return_date DATE ,
expected_return_date DATE NOT NULL ,
PRIMARY KEY (borrow_id )
);

TABLE FINE:

CREATE TABLE Fine (
fine_id INT NOT NULL ,
borrow_id INT NOT NULL ,
librarian_id INT NOT NULL ,
fine_amount FLOAT NOT NULL ,
fine_paid CHAR( 1 ) NULL ,
PRIMARY KEY ( `fine_id` )
);


RELATION BW THE ABOVE CREATED TABLES:

ALTER TABLE Borrow ADD FOREIGN KEY ( student_id ) REFERENCES Student( student_id ) ;
ALTER TABLE Borrow ADD FOREIGN KEY ( ISBN ) REFERENCES books(ISBN) ;
ALTER TABLE Borrow ADD FOREIGN KEY ( librarian_id) REFERENCES Librarian( librarian_id );
ALTER TABLE fine ADD FOREIGN KEY ( borrow_id) REFERENCES Borrow( borrow_id );
ALTER TABLE fine ADD FOREIGN KEY ( librarian_id ) REFERENCES Librarian( librarian_id );



create table login (
username varchar(100) NOT NULL,
password varchar(100) not null,
user_type varchar(100) not null
);









