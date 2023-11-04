import sqlite3

###########################################
#users table function section

def AddNewUser(user):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'INSERT INTO users(name, surname, email, password) VALUES(?,?,?,?)'
    cursor = conn.cursor()   

    success=False
    try:
        cursor.execute(sql, (user['name'], user['surname'], user['email'], user['password']))
        conn.commit()
        success=True
    except Exception as error:
        print('Errore inserimento nel database', str(error))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def GetUserByID(id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM users WHERE id = ?'
    cursor = conn.cursor()   
    cursor.execute(sql, (id,))

    user=cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def GetUserByEmail(email):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM users WHERE email = ?'
    cursor = conn.cursor()   
    cursor.execute(sql, (email,))

    user=cursor.fetchone()

    cursor.close()
    conn.close()

    return user

###########################################
#albums table function section

def AddNewAlbum(album):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'INSERT INTO albums(title, author) VALUES(?,?)'
    cursor = conn.cursor()   

    success=False
    try:
        cursor.execute(sql, (album['title'], album['author']))
        conn.commit()
        success=True
    except Exception as error:
        print('Errore inserimento album nel database', str(error))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def GetAlbums():
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM albums ORDER BY title COLLATE NOCASE ASC'
    cursor = conn.cursor()   
    cursor.execute(sql)

    albums=cursor.fetchall()

    cursor.close()
    conn.close()

    return albums

def GetAlbums_Public():
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM albums ORDER BY title COLLATE NOCASE ASC'
    cursor = conn.cursor()   
    cursor.execute(sql)

    albums=cursor.fetchall()

    public_albums=[]

    #new query to find for each album if there is at least one public photo inside
    for album in albums:
        public_photos=GetPhotosByAlbumID_Public(album['id'])

        if public_photos:
            public_albums.append(album)

    cursor.close()
    conn.close()

    return public_albums

def GetAlbumsByAuthor(author):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM albums WHERE author=? ORDER BY title COLLATE NOCASE ASC'
    cursor = conn.cursor()   
    cursor.execute(sql, (author,))

    albums=cursor.fetchall()

    cursor.close()
    conn.close()

    return albums

def GetAlbumByID(id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM albums WHERE id=?'
    cursor = conn.cursor()   
    cursor.execute(sql, (id,))

    album=cursor.fetchone()

    cursor.close()
    conn.close()

    return album

def GetAlbumTotDownloadsByID(album_id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT SUM(downloads) FROM photos WHERE album_id=?'
    cursor = conn.cursor()   
    cursor.execute(sql, (album_id,))

    tot_downloads=cursor.fetchone()

    cursor.close()
    conn.close()

    return tot_downloads

###########################################
#photos table functions section

def AddNewPhoto(photo):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'INSERT INTO photos(album_id, title, description, date, position, author, private, downloads) VALUES(?,?,?,?,?,?,?,?)'
    cursor = conn.cursor()   

    success=False
    try:
        cursor.execute(sql, (photo['album_id'], photo['title'], 
            photo['description'], photo['date'], photo['position'], 
            photo['author'], photo['private'], photo['downloads']))
        conn.commit()
        success=True
    except Exception as error:
        print('Errore inserimento foto nel database', str(error))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def GetPhotosByAlbumID(album_id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM photos WHERE album_id=? ORDER BY date ASC'
    cursor = conn.cursor()   
    cursor.execute(sql, (album_id,))

    photos=cursor.fetchall()

    cursor.close()
    conn.close()

    return photos

def GetPhotosByAlbumID_Public(album_id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM photos WHERE album_id=? AND private=0 ORDER BY date ASC'
    cursor = conn.cursor()   
    cursor.execute(sql, (album_id,))

    photos=cursor.fetchall()

    cursor.close()
    conn.close()

    return photos

def GetFirstPhotoByAlbumID_Public(album_id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM photos WHERE album_id=? AND private=0 ORDER BY date ASC'
    cursor = conn.cursor()   
    cursor.execute(sql, (album_id,))

    photo=cursor.fetchone()

    cursor.close()
    conn.close()

    return photo

def GetPhotoByID(id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT * FROM photos WHERE id=?'
    cursor = conn.cursor()   
    cursor.execute(sql, (id,))

    photo=cursor.fetchone()

    cursor.close()
    conn.close()

    return photo

def GetLatestAddedPhoto():
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'SELECT id FROM photos ORDER BY id DESC LIMIT 1'
    cursor = conn.cursor()   
    cursor.execute(sql)

    photo=cursor.fetchone()

    cursor.close()
    conn.close()

    return photo

def AssignPhotoFilename(filename, id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'UPDATE photos SET filename=? WHERE id=?'
    cursor = conn.cursor()      

    success=False
    try:
        cursor.execute(sql, (filename, id,))
        conn.commit()
        success=True
    except Exception as error:
        print('Errore modifica foto filename nel database', str(error))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def UpdatePhotoDownloads(downloads, id):
    conn = sqlite3.connect('database/picturist.db') 
    conn.row_factory = sqlite3.Row

    sql = 'UPDATE photos SET downloads=? WHERE id=?'
    cursor = conn.cursor()      

    success=False
    try:
        cursor.execute(sql, (downloads, id,))
        conn.commit()
        success=True
    except Exception as error:
        print('Errore modifica foto filename nel database', str(error))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

###########################################