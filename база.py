import sqlite3

db = sqlite3.connect("ддд.db")


#создали курсор
c = db.cursor()


#выполняет команду которая в скобках
#c.execute(""" create table indi (
   # title text,
  #  ful_text text,
   # views integer,
    #avtor text
#)            """)
#обновляет базу данных
#c.execute("INSERT INTO indi VALUES ('gogl', 'ggg', '2', 'artem')")


# выводит все что находится в аблице данных можно и выборочно если назвать нужную ячейку
c.execute("SELECT rowid, * FROM indi  WHERE rowid = 2")
items = c.fetchall()

for el in items:
    print(el [1] + "\n" + el[3])
db.commit()

db.close()
