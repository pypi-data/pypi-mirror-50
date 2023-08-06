import psycopg2

class pglogger(object):

    connection = None

    def connect(self):

            try:
                print('connecting to PostgreSQL database...')
                
                conn_string = "host="+ self.PGHOST +" port="+ self.PGPORT +" dbname="+ self.PGDATABASE +" user=" + self.PGUSER \
                +" password="+ self.PGPASSWORD
                self.connection = psycopg2.connect(conn_string,connect_timeout=3)                
                
                cursor = self.connection.cursor()
                result = cursor.execute('SELECT VERSION()')
                self.connection.commit()
                print cursor.statusmessage                 
                
                data = cursor.fetchone()

            except Exception as error:
                print('Error: connection not established {}'.format(error))

            else:
                print('connection established\n{}'.format(data[0]))

        #return connection

    def __init__(self,creds):
        self.PGHOST = creds.PGHOST  
        self.PGPORT = creds.PGPORT      
        self.PGDATABASE = creds.PGDATABASE      
        self.PGUSER = creds.PGUSER      
        self.PGPASSWORD = creds.PGPASSWORD      
        self.connect()       
        
    def query(self, query):
        try:
            cursor = self.connection.cursor()
            result = cursor.execute(query)
            self.connection.commit()
            print cursor.statusmessage 
            
            #data = cursor.fetchall()
            return 1
        except Exception as error:
            print('error execting query "{}", error: {}'.format(query, error))
            print('trying to reconnect and execute one more time')
            
            try:      
                self.connect()
                    
                cursor = self.connection.cursor()
                result = cursor.execute(query)
                self.connection.commit()
                print cursor.statusmessage 
                    
                #data = cursor.fetchall() 
                return 1
                    
            except Exception as error:
                print('failed to reconnect; give up')
                return 0               

    def log(self,table,data,time=0):
        import numpy as np
        data_string = np.array2string(data,separator=',')
        data_string = data_string[1:-1] # remove brackets
        
        if not time:
            time = "NOW() AT TIME ZONE 'America/New_York'"

        myquery = "INSERT INTO "+table+" (time,channels) VALUES ("+time+",'{"+data_string+"}')"
        print myquery
        status = self.query(myquery)  
        return status
        
    def close (self): #__del__
        self.connection.close()
        print('connection closed')
        #self.cursor.close()