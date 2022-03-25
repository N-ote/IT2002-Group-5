from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def index(request):
	return render(request, 'moviesharing/index.html')

# Create your views here.
def logout(request):
	try:
		del request.session['email']
	except KeyError:
		pass
	result_dict = {}
	result_dict['logout_success'] = 'See you next time! You have sucessfully logged out'
	return render(request, 'app/index.html', result_dict)

def signup(request):
	return render(request,'app/signup.html')

def login(request): #After users sign up, they will be redirected back to login page
	displayname = request.POST.get('Name','')
	email = request.POST.get('Email','')
	age = request.POST.get('Age','')
	phone_number = request.POST.get('Phone Number','')
	gender = request.POST.get('Gender','')
	vaccination_status = request.POST.get('Vaccination Status','')
	pw = request.POST.get('pw','')
	if displayname != '' and email!= '' and age!=''  and gender!= '' and vaccination_status!= '' and pw!= '' and phone_number!= '':
		email_check =  "SELECT * FROM users WHERE email = '" + email + "';"
		c = connection.cursor()
		c.execute(email_check)
		emails_exist = c.fetchall() #container
		results_dict = {}
		if len(displayname)>128:
			results_dict['name_warning'] = 'Your name cannot be more than 128 characters'
		if len(email) > 128:
			results_dict['email_verifier'] = ' Your email cannot be more than 128 characters'
		elif emails_exist:
			results_dict['email_verifier']='There is already an account with email ' + email
		if len(pw) < 6:
			results_dict['pw_warning'] = 'Your password cannot be less than 6 characters'
		elif len(pw) >64:
			results_dict['pw_warning'] = 'Your password cannot be more than 64 characters'
		if  gender != 'Male' or gender != 'Female' or gender != 'Prefer not to say':
			results_dict['gender_warning'] = 'You must select an option'
		if vaccination_status != 'Fully Vaccinated' or vaccination_status != 'Not Vaccinated' :
			results_dict['vaccination_status_warning'] = 'Your vaccination history is not clear, must select an option'
		if len(phone_number) == 8:
			results_dict['phone_number_warning'] = 'Your phone number must be equals to 8 characters'
		if results_dict:
			return render(request,'app/signup.html',results_dict)
		insert_query = "INSERT INTO users (display_name, email, age, phone_number, gender, vaccination_status, password, count_rate) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s');" % (displayname,email,age,phone_number,gender,vaccination_status,pw,0)
		c = connection.cursor()
		c.execute(insert_query)
	return render(request,'app/login.html')

'''def result(request): #need to change!!! especially the query
	val = 0
	if  request.GET.get('name',''):
		search_string = request.GET.get('name','')
		val = 1
	elif request.GET.get('hourly rate',''):
		search_string = request.GET.get('hourly rate','')
		val = 2
	elif request.GET.get('preference',''):
		search_string = request.GET.get('preference','')
		val = 3
	if val == 1:
		query = "SELECT i.id, i.name, i.genre, i.price, u.country, u.email, CASE WHEN i.id IN  (SELECT item FROM loan_logs WHERE return_date > CURRENT_DATE ) THEN 'Unavailable' ELSE 'Available' END AS availability FROM items AS i, own AS o, users AS u WHERE u.email = o.owner AND o.item = i.id AND i.name ~ \'%s\' ORDER BY i.name ASC" %(search_string).title()
	elif val == 2:
		query = "SELECT i.id, i.name, i.genre, i.price, u.country, u.email, CASE WHEN i.id IN  (SELECT item FROM loan_logs WHERE return_date > CURRENT_DATE ) THEN 'Unavailable' ELSE 'Available' END AS availability FROM items AS i, own AS o, users AS u WHERE u.email = o.owner AND o.item = i.id AND i.price <= \'%s\' ORDER BY i.price ASC" %(float(search_string))
	elif val == 3:
		query = "SELECT i.id, i.name, i.genre, i.price, u.country, u.email, CASE WHEN i.id IN  (SELECT item FROM loan_logs WHERE return_date > CURRENT_DATE ) THEN 'Unavailable' ELSE 'Available' END AS availability FROM items AS i, own AS o, users AS u WHERE u.email = o.owner AND o.item = i.id AND i.genre ~ \'%s\' ORDER BY i.genre ASC" %(search_string).title()
	c = connection.cursor()
	c.execute(query)
	result = c.fetchall()
	result_dict = {'records' : result}
	return render(request, 'app/result.html', result_dict)

def setting(request): 
	return render(request, 'app/settings.html')

def setting_success(request): #need to change
	height = request.POST.get('name','')
	preference = request.POST.get('preference','')
	rate_per_hour = float(request.POST.get('rate_per_hour',''))
	education = request.POST.get('education','')
	query = "SELECT MAX(id) FROM items" # idk what this is for
	c = connection.cursor()
	c.execute(query)
	movieid = c.fetchall()[0][0] + 1
	insert = "INSERT INTO items VALUES ('%s', '%s', '%s', '%s')" %(movieid, moviename, moviegenre, movieprice)
	c.execute(insert)
	insert2 = "INSERT INTO own VALUES ('%s', '%s')" %(request.session['email'],movieid)
	c.execute(insert2)
	return render(request, 'moviesharing/lend_success.html')



def rate(request):  #need to change
	rated = request.POST.get('email','')
	rating = request.POST.get('rating','')
	query1 = "SELECT COALESCE(rating,0) FROM users WHERE email = '" + rated + "';"
	query2 = "SELECT count_rate FROM users WHERE email = '" + rated + "';"
	check = "SELECT * FROM users WHERE email = '" + rated + "';"
	results_dict = {}
	if not check:
		results_dict['email'] = ' Please enter a valid email'
	if float(rating) <0 or float(rating) >5:
		results_dict['rate'] = 'Please enter a valid rating range (from 0 to 5 inclusive)'
	c = connection.cursor()
	c.execute(query2)
	count = c.fetchall()[0][0]
	#results_dict ['err'] = count
	#return render(request, 'moviesharing/home.html', results_dict)
	if count == 0:
		query3 = "UPDATE users SET rating = '%s' WHERE email = '%s'" % (rating,rated)
	else:
		c.execute(query1)
		curr_rate = c.fetchall()[0][0]
		query3 = "UPDATE users SET rating = '%s' WHERE email = '%s' " %((float(curr_rate)*float(count)+float(rating))/(float(count)+1),rated)
	c.execute(query3)
	query4 = "UPDATE users SET count_rate = count_rate + 1 WHERE email = '" + rated + "';"
	c.execute(query4)
	results_dict['rate'] = 'You have successfully rated!'
	return render(request, 'moviesharing/rate.html', results_dict)'''

