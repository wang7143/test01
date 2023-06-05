from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
NAME_SEARCH=''

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif','flv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getLoginDetails():
    #with is called a context management statement
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'], ))
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)

@app.route("/", methods=["POST", "GET"]) #Home page
def root():
    loggedIn, firstName, noOfItems = getLoginDetails()
    name=''
    global NAME_SEARCH
    name=NAME_SEARCH
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        #Order of goods
        cur.execute('SELECT productId, name, price, description, image, stock FROM products order by productId desc')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
        cur.execute(("SELECT lastName FROM users WHERE firstName = ?") , (firstName,))
        lastName1 = cur.fetchone()
        itemData = parse(itemData)
        cur.execute(
            "SELECT products.productId, products.name, products.price, products.image,categories.name FROM products,categories WHERE products.categoryId = categories.categoryId AND products.name like ? ",(name,))
        data = cur.fetchall()
    conn.close()
    data = parse(data)
    if lastName1==('1',) and lastName1!=None:
        return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData,data1=data)
    else:
        return render_template('home1.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData,data1=data)

@app.route("/add")  #Add goods
def admin():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    return render_template('add.html', categories=categories)

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        categoryId = int(request.form['category'])

        #Uploading image procedure
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO products (name, price, description, image, stock, categoryId) VALUES (?, ?, ?, ?, ?, ?)''', (name, price, description, imagename, stock, categoryId))
                conn.commit()
                msg="added successfully"
            except:
                msg="error occured"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect(url_for('root'))

@app.route("/remove")
def remove():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        # Order of goods
        cur.execute('SELECT productId, name, price, description, image, stock FROM products order by productId desc')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
        cur.execute(("SELECT lastName FROM users WHERE firstName = ?"), (firstName,))
        # lastName1 = cur.fetchone()
    itemData = parse(itemData)
    conn.close()
    return render_template('remove.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData)

@app.route("/removeItem", methods=["GET", "POST"])
def removeItem():
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM products WHERE productId = ?', (productId,))
            conn.commit()
            msg = "Deleted successsfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    # print(msg)
    # print(productId)
    return redirect(url_for('remove'))

@app.route("/displayCategory")
def displayCategory():
        loggedIn, firstName, noOfItems = getLoginDetails()
        categoryId = request.args.get("categoryId") #Gets the id value passed from the front-end page form
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = ?", (categoryId, ))
            data = cur.fetchall()
        conn.close()
        categoryName = data[0][4]
        data = parse(data)
        return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryName=categoryName)

@app.route("/searchQuery",methods=["GET", "POST"])  # GET contains the parameters in the URL, and POST passes the parameters through the request body
def searchQuery():
        name = str(request.args.get('name'))
        loggedIn, firstName, noOfItems = getLoginDetails()
        # name1 = str('%'+request.args.get("name")+'%')
        C=''
        for i in name:
            print(i)
            C=C+str(i)+'%'
        # print('%'+C)
        name1=str('%'+C)
        global NAME_SEARCH
        NAME_SEARCH=name1

        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT products.productId, products.name, products.price, products.image,categories.name FROM products,categories WHERE products.categoryId = categories.categoryId AND products.name like ? ", (name1,))
            data = cur.fetchall()
        conn.close()
        data = parse(data)
        print("search-date:")
        print(data)
        return render_template('search.html', data=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems,name=name)

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect('database.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'The user name or password is incorrect！'
            return render_template('login.html', error=error)



@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ?', (productId, ))
        productData = cur.fetchone()
    conn.close()
    return render_template("productDescription.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)

@app.route("/ordersDescription")
def ordersDescription():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    orderId = request.args.get('orderId')
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email,))
        userId = cur.fetchone()[0]
        # cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ?', (productId, ))
        # productData = cur.fetchone()
        cur.execute("SELECT products.productId, products.name, products.price, products.image, orderNO,ispay,isfh,orders.time,users.address1,firstName,phone,time1,kd_number FROM products, orders ,users WHERE"
                    " users.userId=orders.userId AND products.productId = orders.productId AND orders.orderNO = ? ",(orderId,))
        orderDescription = cur.fetchall()
    conn.close()
    # print(firstName)
    # print(orderDescription[0][9])
    return render_template("ordersDescription.html", data=orderDescription, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)

@app.route("/ordersQR")
def ordersQR():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    # orderId = request.args.get('orderId')
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email,))
        userId = cur.fetchone()[0]
        cur.execute("select orderNO from orders where userId=userId and productId=productId order by orderNO desc")
        orderId = str(cur.fetchone()[0])
        # cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ?', (productId, ))
        # productData = cur.fetchone()
        cur.execute("SELECT products.productId, products.name, products.price, products.image, orderNO,ispay,isfh,orders.time,users.address1,firstName,phone,time1 FROM products, orders ,users WHERE"
                    " users.userId=orders.userId AND products.productId = orders.productId AND orders.orderNO = ?",(orderId,))
        orderDescription = cur.fetchall()
    conn.close()
    # print(firstName)
    # print(orderDescription[0][9])
    return render_template("ordersQR.html", data=orderDescription, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)

@app.route("/addToOrders")
def addToOrders():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'], ))
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO orders(userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"

        conn.close()
        # print(orderId)
        return redirect(url_for('ordersQR'))

@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'], ))
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('root'))

@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ? order by products.productId desc", (userId, ))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]

    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/checkout")
def checkout():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    # loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ?", (userId, ))
        products = cur.fetchall()
    conn.close()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template('checkout.html',totalPrice=totalPrice)
@app.route("/checkout1")
def checkout_xqy():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image, orderNO,ispay,isfh,orders.time "
                    "FROM products, orders WHERE products.productId = orders.productId AND orders.userId = ?",(userId,))
        products = cur.fetchall()
    conn.close()
    price = 0
    for row in products:
        price = row[2]
    return render_template('checkout_xqy.html',totalPrice=price)
#shipments
@app.route("/fh")
def fh():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    order_no = request.args.get('orderno')
    email = session['email']
    return render_template('fh.html',order_number=order_no)
#Add the tracking number to the database   Tomorrow write
@app.route("/add_kd_number", methods = ['GET', 'POST'])
def add_kd_number():
    order_number,kd_number=None,None
    if request.method == 'POST':
        kd_number = request.form['kd_number']
        order_number = request.args.get('order_number')
        # print(order_number,kd_number)
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute("UPDATE orders SET kd_number = ?,isfh= ? WHERE orderNO = ?", (kd_number, 'shipped',order_number))
                con.commit()
                msg = "Successfully shipped！"
            except Exception as e:
                con.rollback()
                msg = "Database operation failed, error cause：%s" % e
        con.close()

    return render_template('kd_sj.html',order_number=order_number,kd_number=kd_number,msg=msg)







@app.route("/payCZ")
def payCZ():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image, orderNO,ispay,isfh,orders.time "
                    "FROM products, orders WHERE products.productId = orders.productId AND orders.userId = ?",(userId,))
        products = cur.fetchall()
        for row in products:
            orderNO1 = row[4]
        #     To complete the fake payment here, click Paid in checkout to modify the database ispay field
        try:
            cur.execute("UPDATE orders SET ispay = '已付款' where orderNO =?",(orderNO1,))
            conn.commit()
            msg = "pay successfully"
        except:
            conn.rollback()
            msg = "pay occured"
    conn.close()
    price = 0
    for row in products:
        price = row[2]
        ispay=row[6]

    return render_template('checkout_xqy.html',totalPrice=price,ispay=ispay)

@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    productId = int(request.args.get('productId'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM kart WHERE userId = ? AND productId = ?", (userId, productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('cart'))
@app.route("/removeFromOrders")
def removeFromOrders():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    # productId = int(request.args.get('productId'))
    orderNO =int(request.args.get('orderNO'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        # cur.execute("SELECT orderNO FROM orders WHERE userId = userId")
        try:
            cur.execute("DELETE FROM orders WHERE userId = ? AND orderNO=?", (userId,orderNO))
            # cur.execute("DELETE FROM orders WHERE orderNO=?", (orderNO))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('order'))

@app.route("/account/orders")  #All of the information for the order is stored in the database orders table
def order():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image, orderNO,ispay,isfh,orders.time FROM products, orders WHERE products.productId = orders.productId AND orders.userId = ? order by time desc", (userId, ))
        products = cur.fetchall()
        # Delete orders unpaid 1 day ago
        try:
            cur.execute(("DELETE FROM orders WHERE date('now', '-1 day') >= date(time) and ispay=?"), ('non-payment',))
            conn.commit()
            msg = "Deleted successsfully"
        except:
            conn.rollback()
            msg = "Error occured"
    totalPrice = 0
    for row in products:
        totalPrice += row[2]

    return render_template("order.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)


@app.route("/account/orderSJ")  #All of the information for the order is stored in the database orders table
def orderSJ():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        # userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image, orderNO,ispay,isfh,orders.time FROM products, orders WHERE products.productId = orders.productId order by time desc")
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]

    return render_template("order_SJ.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/logout/")
def logout():
    session.pop('email')
    return redirect(url_for('root'))

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/register", methods = ['GET', 'POST'])   #user registration
def register():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                # address1, address2, zipcode, city, state, country, phone=''
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)
@app.route("/movie")
def movie():
    return render_template("movie.html")

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


if __name__ == '__main__':
    app.run(debug=True)
