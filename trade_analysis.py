from flask import Flask, render_template, request, redirect,session
from DBConnection import Db
import pandas as pd
app = Flask(__name__)
app.secret_key="res"

@app.route('/',methods=['get','post'])
def login():
    if request.method=="POST":
        db=Db()
        username=request.form['textfield']
        password=request.form['textfield2']
        res=db.selectOne("select * from login where user_name='"+username+"' and password='"+password+"'")
        if res is not None :
            if res['user_type']=='admin':
                session['login_id']=res['login_id']
                return redirect('/ahome')
            elif res['user_type']=='user':
                 session['login_id']=res['login_id']
                 return redirect('/user_home')

            else:
                return '<script>alert("Invalid");window.location="/"</script>'
        else:
            return '<script>alert("invalid user");window.location="/"</script>'
    return render_template('login.html')

@app.route('/user_home')
def user_home():
    return render_template('user/user_home.html')

@app.route('/view_user')
def view_user():
    db=Db()
    res=db.select("select * from user")
    return render_template('admin/view_user.html',data=res)

@app.route('/ahome')
def ahome():
    import datetime
    d=datetime.datetime.now().strftime("%Y-%b-%d")
    session['s']=d
    return render_template('admin/admin_home.html')

@app.route('/view_complaint')
def view_complaint():
    db=Db()
    res=db.select("select * from complaint_table,user WHERE complaint_table.user_id=user.user_id AND complaint_table.reply='pending'")
    return render_template('admin/view_complaint.html',data=res)


@app.route('/sent_reply/<cid>',methods=['get','post'])
def sent_reply(cid):
    db=Db()
    if request.method=='POST':
        rply=request.form['textarea']
        db.update("update complaint_table set reply='"+rply+"', reply_date=curdate() where complaint_id='"+cid+"' ")
        return redirect('/ahome')

    res=db.selectOne("select * from complaint_table WHERE complaint_id='"+cid+"'")
    return render_template('admin/sent_reply.html')


@app.route('/change_password',methods=['get','post'])
def change_password():
    db=Db()
    if request.method=='POST':
        old_password=request.form['textfield']
        new_password=request.form['textfield2']
        confirm_password=request.form['textfield3']
        db=Db()
        q1=db.selectOne("select * from login WHERE password='"+old_password+"' and login_id='"+str(session['login_id'])+"'")
        if q1 is not None:
            if new_password==confirm_password:
                db.update("update login set password='"+new_password+"' where login_id='"+str(session['login_id'])+"'")
                return redirect('/ahome')
            else:
                return "<script>alert('invalid password');window.location='/change_password'</script>"
        else:
            return "<script>alert('invalid password');window.location='/change_password'</script>"
    return render_template("admin/change_password.html")



@app.route('/user_reg',methods=['get','post'])
def user_reg():
    if request.method=="POST":
        name=request.form['n']
        House_name=request.form['h']
        place=request.form['p']
        Pin=request.form['pi']
        post=request.form['po']
        district=request.form['di']
        state=request.form['st']
        phone_no=request.form['ph']
        email=request.form['em']
        password=request.form['ps']
        db=Db()
        res=db.insert("insert into login VALUES ('','"+email+"','"+password+"','user')")
        db.insert("insert into user VALUES ('"+str(res)+"','"+name+"','"+House_name+"','"+place+"','"+Pin+"','"+post+"','"+district+"','"+state+"','"+email+"','"+phone_no+"')   ")
        return '''<script>alert("done");window.location="/"</script>'''
    else:
        return render_template('user/index.html')

@app.route('/send_complaint',methods=['get','post'])
def send_complaint():
    if request.method=="POST":
        COMPLAINT=request.form['textarea']
        db=Db()
        db.insert("insert into complaint_table VALUES ('','"+str(session['login_id'])+"' ,'"+COMPLAINT+"',curdate(),'pending','pending')")
        return '<script>alert("Done");window.location="/user_home"</script>'
    else:
        return render_template('user/send_complaint.html')

@app.route('/view_reply')
def view_reply():
    db=Db()
    res=db.selectOne("select * from complaint_table ")
    return render_template('user/view_reply.html',data=res)


@app.route('/change_upassword',methods=['get','post'])
def change_upassword():
    db=Db()
    if request.method=='POST':
        old_password=request.form['textfield']
        new_password=request.form['textfield2']
        confirm_password=request.form['textfield3']
        db=Db()
        q1=db.selectOne("select * from login WHERE password='"+old_password+"' and login_id='"+str(session['login_id'])+"'")
        if q1 is not None:
            if new_password==confirm_password:
                db.update("update login set password='"+new_password+"' where login_id='"+str(session['login_id'])+"'")

            else:
                return "<script>alert('invalid password');window.location='/change_upassword'</script>"
            return redirect('/user_home')
        else:
            return "<script>alert('invalid password');window.location='/change_upassword'</script>"
    return render_template("user/change_upassword.html")


@app.route('/add_dataset')
def add_dataset():
    db=Db()
    a=pd.read_csv("C:\\Users\\USER\\Documents\\project\\trade_analysis\\static\\google.csv")
    print(a.values)
    data=a.values
    for i in data:
        res=db.insert("insert into `dataset`(`id`,`date`,`open_price`,`high_price`,`low_price`,`close_price`,`volume`) values ( '','"+str(i[0])+"','"+str(i[1])+"','"+str(i[2])+"','"+str(i[3])+"','"+str(i[4])+"','"+str(i[5])+"');")
    return "ok"

if __name__ == '__main__':
    app.run(port=4000)
