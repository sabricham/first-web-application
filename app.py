from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import dao

##################################################
#flask init section
app=Flask('__name__')
app.config['SECRET_KEY'] = 'd5XZNPfspVvf6Z7ys5OuU8GgQ8PIPNDW'

##################################################
#login management section
class User(UserMixin):
    def __init__(self, id, name, surname, email, password):
        self.id=id
        self.name=name
        self.surname=surname
        self.email=email
        self.password=password

login_manager = LoginManager()
login_manager.init_app(app)

##################################################
#homepage
@app.route('/')
def entrance():
    #redirect to home
    return redirect(url_for('home'))

@app.route('/home')
def home():
    #get all the public albums in database
    albums=dao.GetAlbums_Public()
    
    #create a pack to contain already the i's album cover image filename
    packs=[]
    for album in albums:   
        #get also the filename of the album cover which is the first public photo in album
        photo=dao.GetFirstPhotoByAlbumID_Public(album['id'])

        #count the total album number of downloads
        tot_downloads=dao.GetAlbumTotDownloadsByID(album['id'])[0]
        
        if photo:
            pack={"album_title":album['title'], "album_id":album['id'], "album_author":album['author'],
                "album_cover_filename":photo['filename'], "album_tot_downloads":tot_downloads}
        else:
            pack={"album_title":album['title'], "album_id":album['id'], "album_author":album['author'],
                 "album_tot_downloads":tot_downloads}

        packs.append(pack)

    return render_template('home.html', packs=packs)

#homepage view album
@app.route('/home/view-album', methods=['GET'])
def home_view_album():
    #get clicked album and all the photos inside that album
    album_id=request.args.get('album_id')

    photos=dao.GetPhotosByAlbumID_Public(album_id)
    album=dao.GetAlbumByID(album_id)
    return render_template('home-view-album.html', photos=photos, album=album)

#homepage view photo
@app.route('/home/view-album/view-photo', methods=['GET'])
def home_view_photo():
    #get clicked photo and also send the album for further infos
    photo_id=request.args.get('photo_id')
    album_id=request.args.get('album_id')

    photo=dao.GetPhotoByID(photo_id)
    album=dao.GetAlbumByID(album_id)
    return render_template('home-view-photo.html', photo=photo, album=album)

##################################################
#personal area
@app.route('/personal-area')
@login_required
def personal():
    #get all the albums made by the logged in user using its id
    user_id=current_user.get_id()
    user=dao.GetUserByID(user_id)
    user_name=user['name']
    user_surname=user['surname']

    albums=dao.GetAlbumsByAuthor(user_name+' '+user_surname)

    #create a pack to contain already the i's album cover image filename
    packs=[]
    for album in albums:   
        #get also the filename of the album cover which is the first public photo in album
        photo=dao.GetFirstPhotoByAlbumID_Public(album['id'])

        #count the total album number of downloads
        tot_downloads=dao.GetAlbumTotDownloadsByID(album['id'])[0]
        
        if photo:
            pack={"album_title":album['title'], "album_id":album['id'], "album_author":album['author'],
                "album_cover_filename":photo['filename'], "album_tot_downloads":tot_downloads}
        else:
            pack={"album_title":album['title'], "album_id":album['id'], "album_author":album['author'],
                 "album_tot_downloads":tot_downloads}

        packs.append(pack)

    return render_template('personal.html', packs=packs)

@app.route('/personal-area', methods=['POST'])
@login_required
def personal_post():
    title = request.form.get('title')

    #get logged in user name and surname
    user_id=current_user.get_id()
    user=dao.GetUserByID(user_id)
    user_name=user['name']
    user_surname=user['surname']

    #new album
    new_album={"title":title, "author":user_name+' '+user_surname}
    success=dao.AddNewAlbum(new_album)

    if success:
        flash('Nuovo album creato con successo!', 'success')
        return redirect(url_for('personal'))
    else:            
        flash('Errore nel server', 'error')
        return redirect(url_for('personal'))

#personal area view-album
@app.route('/personal-area/view-album', methods=['GET'])
@login_required
def personal_view_album():
    #get clicked album and all the photos inside that album
    album_id=request.args.get('album_id')

    photos=dao.GetPhotosByAlbumID(album_id)
    album=dao.GetAlbumByID(album_id)
    return render_template('personal-view-album.html', photos=photos, album=album)

#personal area add photo to album
@app.route('/personal-area/view-album/add-photo', methods=['GET'])
@login_required
def personal_add_photo_redirector():
    #get the album_id passed by method get and redirect to a route using album_id as variable
    album_id=request.args.get('album_id')
    return redirect(url_for('personal_add_photo_get', album_id=album_id))

@app.route('/personal-area/view-album-n<album_id>/add-photo')
@login_required
def personal_add_photo_get(album_id):
    #get the album in which you want to add a photo
    album=dao.GetAlbumByID(album_id)   
    return render_template('personal-add-photo.html', album=album)

@app.route('/personal-area/view-album/add-photo', methods=['POST'])
@login_required
def personal_add_photo_post():
    #get album id from the form
    album_id=request.form.get('album_id')
    album=dao.GetAlbumByID(album_id)

    #get logged in user name and surname as author for the photo
    user_id=current_user.get_id()
    user=dao.GetUserByID(user_id)
    author=user['name']+' '+user['surname']

    #create a new photo in database to add at the album
    title=request.form.get('title')
    description=request.form.get('description')
    date=request.form.get('date')
    position=request.form.get('position')

    private=request.form.get('private')
    if private:
        private=1
    else:
        private=0

    downloads=0

    #step 1: create database record for the photo using the available data    
    new_photo={"album_id":album_id, "title":title, "description":description, "date":date, "position":position,
     "author":author, "private":private, "downloads":downloads}
    success=dao.AddNewPhoto(new_photo)

    if not success:
        flash('Errore nel server step 1', 'error')

    #step 2: get photo id just assigned by the database to create the photo's file in database with a unique filename
    new_photo=dao.GetLatestAddedPhoto()

    #step 3: assign a unique filename to the photo just added using its id
    filename='uploaded-photo-'+str(new_photo["id"])+'.jpg'
    success=dao.AssignPhotoFilename(filename, new_photo["id"])

    if not success:
        flash('Errore nel server step 3', 'error')

    #step 4: save the actual file photo on the server in static folder
    save_url='static/'+filename
    file=request.files['image']
    file.save(save_url)
          
    flash('Nuova foto aggiunta con successo!', 'success')

    return redirect(url_for('personal_add_photo_get', album_id=album_id))

#personal area view photo
@app.route('/personal-area/view-album/view-photo', methods=['GET'])
@login_required
def personal_view_photo():
    #get clicked photo and also send the album  for further infos
    photo_id=request.args.get('photo_id')
    album_id=request.args.get('album_id')

    photo=dao.GetPhotoByID(photo_id)
    album=dao.GetAlbumByID(album_id)
    return render_template('personal-view-photo.html', photo=photo, album=album)

##################################################
#login page section
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user_in_db=dao.GetUserByEmail(email)

    if not user_in_db or not check_password_hash(user_in_db['password'], password):
        flash('Email e/o password errati', 'error')
        return redirect(url_for('login'))
    else:
        user=User(id=user_in_db['id'], name=user_in_db['name'], surname=user_in_db['surname'], email=user_in_db['email'], password=user_in_db['password'])

        login_user(user)
        session["user"]=user_in_db['id']
        return redirect(url_for('home')) 
    
@login_manager.user_loader
def load_user(user_id):
    db_user = dao.GetUserByID(user_id)

    user = User(id=db_user['id'], name=db_user['name'], surname=db_user['surname'], email=db_user['email'], password=db_user['password'])
    return user

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))    
    
##################################################
#register page section
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    password = request.form.get('password')

    user_in_db=dao.GetUserByEmail(email)

    if user_in_db:
        flash('Account già esistente', 'error')
        return redirect(url_for('register'))
    else:
        new_user={"name": name, "surname": surname, "email": email, "password": generate_password_hash(password, method='sha256')}
        success=dao.AddNewUser(new_user)

        if success:
            flash('Account creato con successo!', 'success')
            return redirect(url_for('login'))
        else:            
            flash('Errore nel server', 'error')
            return redirect(url_for('register'))
        
##################################################
#download image file

@app.route('/download-<filename>-<id>')
def download_photo(filename, id):
    #get and update photo infos, download times, only if it's public
    photo=dao.GetPhotoByID(id)
    downloads=photo['downloads']
    downloads=downloads+1
    dao.UpdatePhotoDownloads(downloads, id)

    #download as attachment - without changing url
    return send_file("./static/"+filename, as_attachment=True)