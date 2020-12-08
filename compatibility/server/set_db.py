import sqlite3
import os

db = sqlite3.connect('./blog.db')
cursor = db.cursor()

cursor.execute(
    """create table if not exists `notice`(
        id integer primary key autoincrement,
        `title` varchar(100) not null,
        `content` varchar(1000) not null,
        `author` varchar(20) not null,
        `time` varchar(10) not null
    )""")

cursor.execute(
    """create table if not exists `free`(
        id integer primary key autoincrement,
        `title` varchar(100) not null,
        `content` varchar(1000) not null,
        `author` varchar(20) not null,
        `time` varchar(10) not null
    )""")

cursor.execute(
    "insert into `notice` (`title`, `content`, `author`, `time`) "
    "values ('이곳은 공지게시판입니다.', 'notice0.html', '김현수', '2020/12/05')")
cursor.execute(
    "insert into `notice` (`title`, `content`, `author`, `time`) "
    "values ('1. https server를 구현한 방법', 'notice1.html', '김현수', '2020/12/05')")
cursor.execute(
    "insert into `notice` (`title`, `content`, `author`, `time`) "
    "values ('2. 게시판을 구현한 방법', 'notice2.html', '김현수', '2020/12/05')")
cursor.execute(
    "insert into `free` (`title`, `content`, `author`, `time`) "
    "values ('이곳은 자유게시판입니다.', 'free0.html', '김현수', '2020/12/05')")
db.commit()