#Agentstvo KLINIKA_REGISTRATURA
import pyodbc
cn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};SERVER=VEDROID;DATABASE=Agentstvo;UID=User;PWD=12345")
cursor = cn.cursor()
#ad=input("Ввод: ")
#cursor.execute("UPDATE KARTA_PACIENTA SET ID_pacienta='1', Data_zapisy='2020-12-27', Zapis_vracha='Боль в спине',"
                       # " Problema='erf', Lechenie='refe', Kod_zapisy_na_uslugu='1' WHERE ID_pacienta=1")
#cursor.commit()
cursor.execute("IF IS_MEMBER ('db_owner') = 1 SELECT 'TRUE' "
               "ELSE SELECT 'FALSE'")
#ЧЕРЕЗ FETCHALL зАПОЛНИТЬ ВСЮ СТРОКУ

row = cursor.fetchone()
print(row[0])

#while row:
   # print(row[0])
    #row = cursor.fetchone()
#cursor.execute("UPDATE КЛИЕНТ_ПОКУПАТЕЛЬ SET Код_клиента_покупателя='15', Фамилия='Жмышенко', Имя='Валерий', Отчество='Альбертович', Серия_Паспорта='3217', Номер_Паспорта='800555', Номер_агента='4') WHERE Код_клиента_покупателя=15")
#cursor.commit()

