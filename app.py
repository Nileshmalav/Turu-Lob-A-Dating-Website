from basicm import *
from sqlm import *



def create():
    db.create_all()


@login.user_loader
def load_user(sno):
    return userpassdb.query.get(sno)


@app.route("/sample")
def sample():
    return render_template("new.html")


# google login
# google login
# google login
oauth = OAuth(app)
app.config['GOOGLE_CLIENT_ID'] = "515628424605-0kptp9hkun9m800ljng4j9sujnonup6o.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"




google = oauth.register(
    name='google',
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

# Google login route


@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    myuser = userInfodb.query.filter_by(email=resp['email']).first()
    if myuser:
        user_object = userpassdb.query.filter_by(
            username=myuser.username).first()
        login_user(user_object)
        noti = notificationdb(username=myuser.username, title="New Login",
                              text="new login for your account", type='login')
        db.session.add(noti)
        db.session.commit()
        return redirect("/")
    elif(not myuser):
        myuserInfo = userInfodb(
            first_name=resp['name'], last_name=" ", email=resp['email'])
        db.session.add(myuserInfo)
        db.session.commit()
        user = userInfodb.query.filter_by(email=resp['email']).first()
        return render_template("LoginSignup/signup2.html", sno=user.sno, message1="Now select username and password!")

    elif(not myuser.username):
        myuser.email = resp['email']
        myuser.first_name = resp['name']
        myuser.last_name = " "
        db.session.commit()
        user = userInfodb.query.filter_by(email=resp['email']).first()
        return render_template("LoginSignup/signup2.html", sno=user.sno, message1="Now select username and password!")

# google login
# google login
# google login


@app.route("/")
def index():
    user_object = load_user(current_user.get_id())
    if user_object:
        username = user_object.username
        return redirect("/home")
    return render_template('LoginSignup/login.html')


# login logout
# login logout
# login logout
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_object = userpassdb.query.filter_by(username=username).first()
        if user_object:
            if user_object.password == password:
                login_user(user_object)
                noti = notificationdb(username=username, title="New Login",
                                      text="new login for your account", type="login")
                db.session.add(noti)
                db.session.commit()
                return redirect("/")
            else:
                return render_template("LoginSignup/login.html", message="password incorrect")
        else:
            return render_template("LoginSignup/login.html", message="username not registered")
    else:
        return render_template('LoginSignup/login.html')


@app.route("/logout")
def logout():
    logout_user()
    return render_template("LoginSignup/login.html", message2="login now")


# login logout
# login logout
# login logout


# signup
# signup
# signup

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        phone = request.form['phone']
        if len(email) <= 1:
            return render_template("LoginSignup/signup.html", message="email cannot be empty")
        if len(first_name) <= 1:
            return render_template("LoginSignup/signup.html", message="first name cannot be empty")
        if len(last_name) <= 1:
            return render_template("LoginSignup/signup.html", message="last name cannot be empty")

        myTodo = userInfodb.query.filter_by(email=email).first()
        if not myTodo:
            myuserInfo = userInfodb(
                first_name=first_name, last_name=last_name, email=email, phone=phone)
            db.session.add(myuserInfo)
            user = userInfodb.query.filter_by(email=email).first()

            # otp code
            # otp code
            otpuser = otpdb.query.filter_by(email=email).first()
            myotp = str(randint(100000, 999999))
            if otpuser:
                otpuser.otp = myotp
                otpuser.time = datetime.now()
            else:
                myuserotp = otpdb(email=email, otp=myotp, time=datetime.now())
                db.session.add(myuserotp)
            db.session.commit()
            try:
                mail.send_message('OTP for forget login and password', sender=email,
                                  recipients=[email],
                                  html=render_template("otpmail2.html", myotp=myotp))
                return render_template("/LoginSignup/otpsu.html", message1="OTP is send to your email", sno=user.sno)
            except:
                return render_template("/LoginSignup/otpsu.html", message=f"OTP is not send to your email. Please don't use any proxy. OTP is {myotp} for testing purpose only", sno=user.sno)

            # otp code
            # otp code
        elif(not myTodo.username):
            myTodo.email = email
            myTodo.first_name = first_name
            myTodo.last_name = last_name
            myTodo.phone = phone

            user = userInfodb.query.filter_by(email=email).first()
            # otp code
            # otp code
            otpuser = otpdb.query.filter_by(email=email).first()
            myotp = str(randint(100000, 999999))
            if otpuser:
                otpuser.otp = myotp
                otpuser.time = datetime.now()
            else:
                myuserotp = otpdb(email=email, otp=myotp, time=datetime.now())
                db.session.add(myuserotp)
            db.session.commit()

            try:
                mail.send_message('OTP for forget login and password', sender=email,
                                  recipients=[email],
                                  html=render_template("otpmail2.html", myotp=myotp))
                return render_template("/LoginSignup/otpsu.html", message1="OTP is send to your email", sno=user.sno)
            except:
                return render_template("/LoginSignup/otpsu.html", message=f"OTP is not send to your email. Please don't use any proxy. OTP is {myotp} for testing purpose only", sno=user.sno)

            # otp code
            # otp code
        else:
            return render_template("LoginSignup/signup.html", message="email is already registered")
    return render_template('LoginSignup/signup.html')


# otp verification
# otp verification
@app.route("/signup/otpverify/<int:sno>", methods=['GET', 'POST'])
def otpsuverification(sno):
    myuser = userInfodb.query.filter_by(sno=sno).first()
    email = myuser.email
    if request.method == "POST":
        myotpuser = otpdb.query.filter_by(email=email).first()
        otp = myotpuser.otp
        fotp = request.form['otp']
        if str(fotp) == str(otp):
            return render_template("LoginSignup/signup2.html", sno=sno, message2="Now select username and password!")

        else:
            return render_template("/LoginSignup/otpsu.html", message="OTP entered is incorrect!", sno=sno)
# otp verification
# otp verification

# otp resend
# otp resend


@app.route("/signup/otpresend/<int:sno>", methods=['GET', 'POST'])
def otpsuresend(sno):
    userinfo = userInfodb.query.filter_by(sno=sno).first()
    email = userinfo.email
    otpuser = otpdb.query.filter_by(email=email).first()
    myotp = str(randint(100000, 999999))
    if otpuser:
        otpuser.otp = myotp
        otpuser.time = datetime.now()
    else:
        myuserotp = otpdb(email=email, otp=myotp, time=datetime.now())
        db.session.add(myuserotp)
    db.session.commit()

    try:
        mail.send_message('OTP for forget login and password', sender=email,
                          recipients=[email],
                          html=render_template("otpmail2.html", myotp=myotp))
        return render_template("/LoginSignup/otpsu.html", message1="OTP is send to your email", sno=sno)
    except:
        return render_template("/LoginSignup/otpsu.html", message=f"OTP is not send to your email. Please don't use any proxy. OTP is {myotp} for testing purpose only", sno=sno)


# otp resend
# otp resend


@app.route("/signup/<int:sno>", methods=['GET', 'POST'])
def signup2(sno):
    username = request.form['username']
    password = request.form['password']
    if len(username) <= 1:
        return render_template("LoginSignup/signup2.html", sno=sno, message="username cannot be empty")
    if len(password) <= 4:
        return render_template("LoginSignup/signup2.html", sno=sno, message="password can not be empty")

    userna = userpassdb.query.filter_by(username=username).all()
    if not userna:
        user = userpassdb(username=username, password=password, sno=sno)
        userinfo = userInfodb.query.filter_by(sno=sno).first()
        userinfo.username = username
        db.session.add(user)
        db.session.commit()
        user_object = userpassdb.query.filter_by(username=username).first()
        login_user(user_object)
        noti = notificationdb(username=username, title="Sign UP Successfull",
                              text="your account was registered successfully😍😍! now enjoy using Turu💖Lob", type="login")
        db.session.add(noti)
        db.session.commit()
        return redirect("/profile/editprofile")
    else:
        return render_template("LoginSignup/signup2.html", sno=sno, message="username already taken, try another username")

# signup
# signup
# signup


# forget password
# forget password
# forget password
@app.route("/forgetpassword", methods=['GET', 'POST'])
def forgetpassword():
    if request.method == "GET":
        return render_template("/LoginSignup/forgetpassword.html")
    elif request.method == 'POST':
        myotp = str(randint(100000, 999999))
        email = request.form['email']
        myuser = userInfodb.query.filter_by(email=email).first()
        if myuser:
            username = myuser.username
            otpuser = otpdb.query.filter_by(username=username).first()
            sno = myuser.sno
            if otpuser:
                otpuser.otp = myotp
                otpuser.email = email
                otpuser.time = datetime.now()
            else:
                myuserotp = otpdb(username=username, otp=myotp,
                                  email=email, time=datetime.now())
                db.session.add(myuserotp)
            db.session.commit()
            try:
                mail.send_message('OTP for forget login and password', sender=email,
                                  recipients=[email],
                                  html=render_template("otpmail.html", myotp=myotp))
                return render_template("/LoginSignup/otpfp.html", message1="OTP is send to your email", sno=sno)
            except:
                return render_template("/LoginSignup/otpfp.html", message=f"OTP is not send to your email. Please don't use any proxy. OTP is {myotp} for testing purpose only", sno=sno)
        else:
            return render_template("/LoginSignup/forgetpassword.html", message="user not found")


@app.route("/otpfpverification/<string:sno>", methods=['GET', 'POST'])
def otpfpverification(sno):
    myuser = userInfodb.query.filter_by(sno=sno).first()
    username = myuser.username
    if request.method == "POST":
        myotpuser = otpdb.query.filter_by(username=username).first()
        otp = myotpuser.otp
        fotp = request.form['otp']
        if str(fotp) == str(otp):
            userpass = userpassdb.query.filter_by(username=username).first()
            password = userpass.password
            return render_template("/LoginSignup/userlogpass.html", username=username, password=password)
        else:
            return render_template("/LoginSignup/otpfp.html", message="OTP entered is incorrect!", sno=sno)


@app.route("/resetpassword", methods=['GET', 'POST'])
def resetpassword():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        
        newpass=request.form["password1"]
        newpass2=request.form["password2"]
        if newpass!=newpass2:
            return render_template("/LoginSignup/userlogpass.html", username=username, password=password,message="passwords are not same")
        userpass = userpassdb.query.filter_by(username=username).first()
        if password==userpass.password:
            userpass.password=newpass
        db.session.commit()
        user_object = userpassdb.query.filter_by(
            username=username).first()
        login_user(user_object)
        return redirect("/")

# otp resend
# otp resend
@app.route("/forgetpassword/otpresend/<int:sno>", methods=['GET', 'POST'])
def otpfpresend(sno):
    myuser = userInfodb.query.filter_by(sno=sno).first()
    username = myuser.username
    email = myuser.email
    otpuser = otpdb.query.filter_by(username=username).first()
    myotp = str(randint(100000, 999999))

    if otpuser:
        otpuser.otp = myotp
        otpuser.time = datetime.now()
    else:
        myuserotp = otpdb(username=username, otp=myotp, time=datetime.now())
        db.session.add(myuserotp)
    db.session.commit()
    try:
        mail.send_message('OTP for forget login and password', sender=email,
                          recipients=[email],
                          html=render_template("otpmail.html", myotp=myotp))
        return render_template("/LoginSignup/otpfp.html", message1="OTP is send to your email", sno=sno)
    except:
        return render_template("/LoginSignup/otpfp.html", message=f"OTP is not send to your email. Please don't use any proxy. OTP is {myotp} for testing purpose only", sno=sno)


# otp resend
# otp resend

# forget password
# forget password
# forget password


# TODO: profile
# TODO: profile
# TODO: profile

# main profile
# main profile
@app.route('/<string:myusername>/profile')
def profile(myusername):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    user = userInfodb.query.filter_by(username=myusername).first()
    me = userInfodb.query.filter_by(username=username).first()
    images = otherprofileImagesdb.query.filter_by(username=myusername).all()
    posts = postsdb.query.filter_by(username=myusername).order_by(
        postsdb.date_created.desc()).all()
    postlike = postslikedb.query.filter_by(fusername=username).all()
    return render_template("Profile/profile.html", user=user, me=me, images=images, username=username, posts=posts, postlike=postlike)
# main profile
# main profile


# edit details
# edit details
@app.route('/profile/editprofile', methods=['GET', 'POST'])
@login_required
def profileEdit():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    userinfo = userInfodb.query.filter_by(username=username).first()
    userpass=userpassdb.query.filter_by(username=username).first()
    if request.method == 'POST':
        username1 = request.form['username']
        if username != username1:
            user1 = userpassdb.query.filter_by(username=username1).first()
            if user1:
                return render_template("Profile/profileedit.html", user=userinfo, message="username already taken")

        email = request.form['email']
        if email != userinfo.email:
            user1 = userInfodb.query.filter_by(email=email).first()
            if user1:
                return render_template("Profile/profileedit.html", user=userinfo, message="email already registered")

        userinfo.first_name = first_name = request.form['first_name']
        userinfo.last_name = last_name = request.form['last_name']
        userinfo.phone = request.form['phone']
        userinfo.intro = request.form['intro']
        userinfo.gender = request.form['gender']
        userinfo.age = request.form['age']
        userinfo.facebook = request.form['facebook']
        userinfo.instagram = request.form['instagram']
        if request.form['locationCity']:
            userinfo.locationCity = request.form['locationCity']
        if request.form['locationState']:
            userinfo.locationState = request.form['locationState']
        if request.form['locationCountry']:
            userinfo.locationCountry = request.form['locationCountry']
        db.session.commit()
        return redirect(f"/{username1}/profile")
    return render_template("Profile/profileedit.html", user=userinfo)
# edit details
# edit details


# edit profile image
# edit profile image
@app.route('/profile/editprofile/image', methods=['POST', 'GET'])
@login_required
def profileupload():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    if request.method == 'POST':
        pic = request.files['pic']
        user = userInfodb.query.filter_by(username=username).first()
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
        user.img = pic.read()
        user.imgname = filename
        user.imgmimetype = mimetype
        db.session.commit()
        return redirect("/profile/editprofile")
    else:
        return render_template("Profile/profileimageul.html")
# edit profile image
# edit profile image

# show profile image


@app.route('/profile/images/<string:username>')
def RouteImgProfile(username):
    img = userInfodb.query.filter_by(username=username).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.imgmimetype)
# show profile image

# add delete other images
# add delete other images


@app.route('/profile/<string:myusername>/otherimages', methods=['POST', 'GET'])
@login_required
def profileotherpictures(myusername):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    if request.method == 'POST':
        pic = request.files['pic']
        user = userInfodb.query.filter_by(username=username).first()
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
        img = otherprofileImagesdb(
            username=username, img=pic.read(), name=filename, mimetype=mimetype)

        db.session.add(img)
        db.session.commit()
        return redirect(f"/profile/{username}/otherimages")

    images = otherprofileImagesdb.query.filter(otherprofileImagesdb.username == myusername).order_by(
        otherprofileImagesdb.date_created.desc()).all()

    return render_template("Profile/otherimage.html", images=images, username=username)
# add delete other images
# add delete other images


# route other profile images
@app.route("/profile/otherprofileimages/<int:id>")
def Routeotherprofileimage(id):
    img = otherprofileImagesdb.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.img, mimetype=img.mimetype)
# route other profile images

# delete other profile images


@app.route("/delete/otherprofileimages/<int:id>", methods=['GET'])
@login_required
def deleteotherprofileimage(id):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    img = otherprofileImagesdb.query.filter_by(id=id).first()
    if img.username == username:
        db.session.delete(img)
        db.session.commit()
    return redirect(f"/profile/{username}/otherimages")
# delete other profile images

# TODO: profile
# TODO: profile
# TODO: profile


# TODO: chats
# TODO: chats
# TODO: chats

# socketio code
# socketio code
@socketio.on('message')
@login_required
def message(data):
    user_object = load_user(current_user.get_id())
    username = user_object.username  # data['username']
    time = datetime.now()
    time1 = time.strftime("%m/%d/%Y, %H:%M:%S")

    msg = {'chat': data['chat'], 'fromuser': username,
           'touser': data['touser'], 'sendtime': time1,'url':0}
    touser = (data['touser'])
    chat = data['chat']
    chats = chatsdb(touser=touser, fromuser=username, chatmessage=chat)

    chatsuser1 = chatsuserdb.query.filter_by(
        fromuser=username, touser=touser).first()

    chatsuser2 = chatsuserdb.query.filter_by(
        fromuser=touser, touser=username).first()
    chatsuser = chatsuser = chatsuserdb.query.filter(
        (chatsuserdb.fromuser == username), (chatsuserdb.touser == touser)).first()
    if chatsuser1 != None:
        chatsuser = chatsuser1
    elif chatsuser2 != None:
        chatsuser = chatsuser2

    if chatsuser:
        chatsuser.lastmessage = chat
        chatsuser.chatusertime = time1
        chatsuser.date_created = time
    else:
        chatsuser = chatsuserdb(touser=touser, fromuser=username,
                                lastmessage=chat, chatusertime=time1, date_created=time)
        db.session.add(chatsuser)
    db.session.add(chats)
    db.session.commit()
    send(msg, broadcast=True)
    




@socketio.on('imageroom')
@login_required
def messageimage(data):
    user_object = load_user(current_user.get_id())
    username = user_object.username  # data['username']
    time = datetime.now()
    time1 = time.strftime("%m/%d/%Y, %H:%M:%S")
    touser = (data['touser'])

    if data['image']!=0:
        mytouser = touser
        filename = secure_filename(data['filename'])
        mimetype = data['mimetype']
        img = chatsdb.query.filter_by(fromuser=username,touser=touser).order_by(chatsdb.date_created.desc()).first()

        


        image = {'image':data['image'],'url': f'/chats/images/{img.id+1}', 'fromuser': username,
            'touser': data['touser'], 'sendtime': time1}
    else:
        image={'url': data['url'], 'fromuser': username,
            'touser': data['touser'], 'sendtime': time1}
    send(image, broadcast=True)
# socketio code
# socketio code


@app.route("/chats")
@login_required
def chats():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    chatsusers = chatsuserdb.query.filter(
        (chatsuserdb.fromuser == username) | (chatsuserdb.touser == username)).order_by(chatsuserdb.date_created.desc()).all()

    return render_template("Chats/chatusers.html", username=username, chatusers=chatsusers)


# chat screen to user
# chat screen to user
@app.route("/chats/<string:touser>")
@login_required
def userchats(touser):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    chatsusers = chatsuserdb.query.filter(
        (chatsuserdb.fromuser == username) | (chatsuserdb.touser == username)).order_by(chatsuserdb.date_created.desc()).all()
    mtouser = userInfodb.query.filter_by(username=touser).first()
    mychats = chatsdb.query.filter(
        (chatsdb.fromuser == username) | (chatsdb.touser == username)).all()
    return render_template("Chats/chatscreen.html", username=username, mtouser=mtouser, chatusers=chatsusers, touser=touser, chats=mychats)
# chat screen to user
# chat screen to user

# chat image
# chat image
@app.route("/chats/images/<int:id>")
@login_required
def chatimages(id):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    chatsimg = chatsdb.query.filter(chatsdb.id == id).first()

    if chatsimg.fromuser == username or chatsimg.touser == username:
        if not chatsimg:
            return 'Img Not Found!', 404

        return Response(chatsimg.chatimg, mimetype=chatsimg.imagemimetype)
    else:
        return "Nothing here"
# chat image
# chat image


# chat image send
# chat image send
@app.route("/chats/<string:touser>/imageupload", methods=["POST", "GET"])
@login_required
def chatimageupload(touser):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    if request.method == "POST":
        pic = request.files['pic']
        mytouser = touser
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = chatsdb(chatimg=pic.read(), fromuser=username,
                      touser=mytouser, imagename=filename, imagemimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        return redirect(f"/chats/{touser}")
    else:
        return render_template("Chats/chatimgul.html", touser=touser)
# chat image send
# chat image send


# chat stickers
# chat stickers
# chat stickers
# chat stickers
@app.route("/chats/<string:touser>/stickers")
@login_required
def chatsStickers(touser):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    stickers = stickersdb.query.order_by(stickersdb.date_created.desc()).all()
    return render_template("Chats/stickers.html", stickers=stickers, touser=touser)


# send stickers
# send stickers
@app.route("/chats/sticker/<string:touser>/<int:id>/send", methods=['POST', 'GET'])
@login_required
def chatStickerSend(touser, id):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    sticker = stickersdb.query.filter_by(id=id).first()
    pic = sticker.img
    if request.method == "GET":
        img = chatsdb(chatimg=pic, fromuser=username,
                      touser=touser, imagename=sticker.name, imagemimetype=sticker.mimetype)
        db.session.add(img)
        db.session.commit()
        return redirect(f"/chats/{touser}")

    return redirect(f"/chats/{touser}")
# send stickers
# send stickers


# chat stickers
# chat stickers
# chat stickers
# chat stickers

# TODO: chats
# TODO: chats
# TODO: chats


# TODO: Main
# TODO: Main

# location
# location
@app.route("/location", methods=['POST'])
@login_required
def location():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        user = userInfodb.query.filter_by(username=username).first()
        user.latitude = latitude
        user.longitude = longitude
        db.session.commit()
        return "success"

# location
# location


# home posts
# home posts
# home posts
# home posts
@app.route("/home")
@login_required
def home():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    user = userInfodb.query.filter_by(username=username).first()
    me = userInfodb.query.filter_by(username=username).first()

    posts1 = postsdb.query.filter_by(City=user.locationCity).order_by(postsdb.date_created.desc()).all()
    posts2 = postsdb.query.filter_by(State=user.locationState).order_by(postsdb.date_created.desc()).all()
    posts3 = postsdb.query.filter_by(Country=user.locationCountry).order_by(postsdb.date_created.desc()).all()
    posts4 = postsdb.query.order_by(postsdb.date_created.desc()).all()
    if posts1:
        shuffle(posts1)
    if posts2:
        shuffle(posts2)
    if posts3:
        shuffle(posts3)
    if posts4:
        shuffle(posts4)
    posts=posts1+posts2+posts3+posts4

    postlike = postslikedb.query.filter_by(fusername=username).all()
    return render_template('home.html', username=username, posts=posts , postlike=postlike, me=me)


@app.route("/posts/images", methods=['GET', 'POST'])
@login_required
def postImageul():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    user = userInfodb.query.filter_by(username=username).first()
    if request.method == 'POST':
        pic = request.files['pic']
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
        post = postsdb(username=username, name=f"{user.first_name} {user.last_name}", age=user.age,
                       latitude=user.latitude, longitude=user.longitude, City=user.locationCity, State=user.locationState, Country=user.locationCountry, img=pic.read(), imagename=filename, imagemimetype=mimetype)
        db.session.add(post)
        db.session.commit()
        return redirect("/")
    else:
        return render_template('addpost.html')


@app.route("/posts/images/<string:sno>", methods=['GET', 'POST'])
@login_required
def postImage(sno):
    img = postsdb.query.filter_by(id=sno).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.imagemimetype)


@app.route("/posts/like", methods=['GET', 'POST'])
@login_required
def postLike():
    if request.method == 'POST':
        user_object = load_user(current_user.get_id())
        username = user_object.username
        sno = request.form['sno']
        myuser = userInfodb.query.filter_by(username=username).first()
        post = postsdb.query.filter_by(id=sno).first()
        user = postslikedb.query.filter_by(fusername=username).first()
        if user:
            db.session.delete(user)
            like = int(post.like)-1
            if like < 0:
                like = 0
            post.like = like

        else:
            user = postslikedb(fusername=username, postid=sno)
            like = int(post.like)+1
            if like < 0:
                like = 0
            post.like = like
            noti = notificationdb(username=username,
                                  text=f"New like to your post from {myuser.first_name} {myuser.last_name}😍", type='post', link=f'/{username}/profile', title="❤️New Like")
            db.session.add(user)
            db.session.add(noti)
        db.session.commit()
        return "success"
# home posts
# home posts
# home posts
# home posts


# swipe and match
# swipe and match
@app.route("/swipematch")
@login_required
def swipematch():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    myuser = userInfodb.query.filter_by(username=username).first()
    mygender = myuser.gender
    gender = ""
    if mygender == "Female":
        gender = "Male"
    elif mygender == "Male":
        gender = "Female"
    else:
        message1 = "set gender first"
    usershow1 = userInfodb.query.filter(
        userInfodb.locationCity == myuser.locationCity, userInfodb.gender == gender).all()
    usershow2 = userInfodb.query.filter(
        userInfodb.locationState == myuser.locationState, userInfodb.gender == gender).all()
    usershow3 = userInfodb.query.filter(
        userInfodb.locationCountry == myuser.locationCountry, userInfodb.gender == gender).all()
    usershow4 = userInfodb.query.filter_by(gender=gender).all()
    if usershow1:
        shuffle(usershow1)
    if usershow2:
        shuffle(usershow2)
    if usershow3:
        shuffle(usershow3)
    if usershow4:
        shuffle(usershow4)
    mylike = likedb.query.filter_by(fromuser=username).all()
    mysuperlike = superLikedb.query.filter_by(fromuser=username).all()
    mysave = savedb.query.filter_by(fromuser=username).all()

    return render_template("swipematch.html", me=myuser, usershow1=usershow1, usershow2=usershow2, usershow3=usershow3, usershow4=usershow4, mylike=mylike, mysuperlike=mysuperlike, mysave=mysave)
# swipe and match
# swipe and match


# like
# like
@app.route("/user/like", methods=['post'])
@login_required
def likeuser():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    message = request.form['message']
    sno = request.form['tousersno']
    myuser = userInfodb.query.filter_by(sno=sno).first()
    noti = notificationdb(username=myuser.username,
                          text=f"New like from {myuser.first_name} {myuser.last_name}😍", type='like', link=f'/{username}/profile', title="❤️New Like")
    db.session.add(noti)
    likeuser = likedb.query.filter(
        likedb.fromuser == username, likedb.touser == myuser.username).first()
    if likeuser:
        db.session.delete(likeuser)
    else:
        mylike = likedb(fromuser=username, touser=myuser.username)
        db.session.add(mylike)
    db.session.commit()
    return "success"
# like
# like

# superLike
# superLike


@app.route("/user/superlike", methods=['post'])
@login_required
def lsuperlikeuser():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    message = request.form['message']
    sno = request.form['tousersno']

    myuser = userInfodb.query.filter_by(sno=sno).first()
    noti = notificationdb(username=myuser.username,
                          text=f"New Super like 💖 from {myuser.first_name} {myuser.last_name}😍", type='superlike', link=f'/{username}/profile', title="❤️New Super Like")
    db.session.add(noti)
    slikeuser = superLikedb.query.filter(
        likedb.fromuser == username, likedb.touser == myuser.username).first()
    if slikeuser:
        db.session.delete(slikeuser)
    else:
        myslike = superLikedb(fromuser=username, touser=myuser.username)
        db.session.add(myslike)
    db.session.commit()
    return "success"
# superLike
# superLike


# save
# save
@app.route("/user/save", methods=['post'])
@login_required
def saveuser():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    message = request.form['message']
    sno = request.form['tousersno']

    myuser = userInfodb.query.filter_by(sno=sno).first()
    saveduser = savedb.query.filter(
        likedb.fromuser == username, likedb.touser == myuser.username).first()
    if saveduser:
        db.session.delete(saveduser)
    else:
        mysave = savedb(fromuser=username, touser=myuser.username,first_name=myuser.first_name,last_name=myuser.last_name,city=myuser.locationCity,state=myuser.locationState,age=myuser.age)
        db.session.add(mysave)
    db.session.commit()
    return "success"
# save
# save

# find your love
# find your love


@app.route("/search")
@login_required
def findyourlove():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    users = userInfodb.query.all()
    shuffle(users)
    mylike = likedb.query.filter_by(fromuser=username).all()
    mysuperlike = superLikedb.query.filter_by(fromuser=username).all()
    mysave = savedb.query.filter_by(fromuser=username).all()
    me = userInfodb.query.filter_by(username=username).first()

    return render_template('search/search.html', users=users, me=me, mylike=mylike, mysuperlike=mysuperlike, mysave=mysave)
# find your love
# find your love

#  shedule
#  shedule


@app.route("/schedule")
@login_required
def shedule():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    return render_template('schedule.html')
#  shedule
#  shedule


#  shedule
#  shedule
@app.route("/saved")
@login_required
def saved():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    users=savedb.query.filter_by(fromuser=username).all()
    return render_template('saved.html',users=users)
#  shedule
#  shedule


# membership
# membership
@app.route("/membership")
@login_required
def membership():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    return render_template('membership.html')
# membership
# membership


# notifications
# notifications
@app.route("/notifications")
@login_required
def notifications():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    notification = notificationdb.query.filter(
        notificationdb.username == username).order_by(notificationdb.date_created.desc())
    return render_template('notification.html', username=username, notification=notification)
# notifications
# notifications


# socketio code
# socketio code
@socketio.on('notification')
@login_required
def notification(data):
    user_object = load_user(current_user.get_id())
    username = user_object.username
    
# socketio code
# socketio code


# notifications
# notifications




@app.route("/<string:any>")
def anyurl(any):
    return redirect('/')
# TODO: Main
# TODO: Main









# TODO: Admin
# TODO: Admin


@app.route("/admin")
@login_required
def admin():
    user_object = load_user(current_user.get_id())
    username = user_object.username
    if username=='nilesh':
        userpassm=userpassdb.query.all()
        userinfom=userInfodb.query.all()
        return render_template('Admin/admin.html', userpass=userpassm,userinfo=userinfom)
    else:
        return "Not allowed"




# adding database   
# adding database   
# adding database   
@app.route("/admin/addData",methods=[ "POST","GET"])
def adduserinfo():
    if request.method=="POST":
        username=request.form['username']
        first_name=request.form['firstname']
        lastname=request.form['lastname']
        phone=request.form['phone']
        email=request.form['email']
        intro=request.form['intro']
        gender=request.form['gender']
        age=request.form['age']
        dob=request.form['dob']
 
        userinfo = userInfodb(username=username,first_name=first_name,last_name=lastname,phone=phone,email=email,intro=intro,gender=gender,age=age,dob=dob)
        db.session.add(userinfo)
        db.session.commit()
        return "Added successfully"
    return render_template('Admin/databaseadd.html')

# adding database   
# adding database   
# adding database   




# admin stickers upload
# admin stickers upload


# show stickers
@app.route('/stickers/<int:id>')
def chatStickersImage(id):
    img = stickersdb.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)
# show stickers



@app.route('/admin/stickersul', methods=['POST', 'GET'])
def chatStickerUpload():
    if request.method == 'POST':
        pic = request.files['pic']
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = stickersdb(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        return 'Img Uploaded!', 200
    else:
        return render_template("Admin/stickersul.html")
# admin stickers upload
# admin stickers upload



#deleting database
#deleting database
#deleting database
@app.route("/admin/delete/userpass/<int:sno>")
def adminDeleteUserpass(sno):
    myTodo=userpassdb.query.filter_by(sno=sno).first()
    db.session.delete(myTodo)
    db.session.commit()
    return redirect("/admin")


@app.route("/admin/delete/userinfo/<int:sno>")
def adminDeleteUserinfo(sno):
    myTodo=userInfodb.query.filter_by(sno=sno).first()
    db.session.delete(myTodo)
    db.session.commit()
    return redirect("/admin")


#deleting database
#deleting database
#deleting database



# TODO: Admin
# TODO: Admin
if __name__ == "__main__":
    create()
    addingmydata()
    socketio.run(app, debug=True)
