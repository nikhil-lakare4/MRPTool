from django.shortcuts import render,redirect
from . models import company_detail,admin_detail,worker_detail,product_detail,attribute_product,history_sales_data,job_detail,all_jobs,job_assign,worker_data
from datetime import datetime
from django.contrib import messages
import pickle
import numpy as n
import math
import pytz
from django.http import JsonResponse

# Create your views here.
def company_login_func(request):
    uname = None
    if request.method == 'POST':
        print("Number of arguments : ",request.POST.keys())
        uname = request.POST['company_username']
        password = request.POST['company_password']
        print(uname,password)
        user1 = company_detail()
        if company_detail.objects.filter(company_username = uname , company_password= password).count() > 0:
            request.session['companyuser'] = uname.strip()
            cname = company_detail.objects.get(company_username = uname)
            request.session['companyrealname'] = cname.company_realname
            print(cname.company_realname)
            return render(request,'roleswitch.html',{'msg':cname.company_realname.upper()})
        return render(request,'company_login.html')

    if 'companyuser' in request.session:
        if request.session['companyuser'] != None:
            # uname = request.session['companyuser']
            # cname = company_detail.objects.get(company_username = uname)
            # print(cname.company_realname)
            s = request.session['companyrealname']
            return render(request,'roleswitch.html',{'msg':s.upper()})
    else:
        return render(request,'company_login.html')

def company_register_func(request):
    message = ""
    if request.method == 'POST':
        uname = request.POST['company_username']
        fname = request.POST['company_fullname']
        password1 = request.POST['ps1']
        password2 = request.POST['ps2']
        c = company_detail()
        if company_detail.objects.filter(company_username = uname) :
            print("exist")
            message = "Exist"
            messages.error(request,"Company Already Registered")
            return render(request,'company_register.html',{'msg':message})
        elif password1 != password2 or (password1=="" and password2==""):
            message = "Wrong password"
            messages.error(request,"Password Dont match!")
            return render(request,'company_register.html',{'msg':message})
        else:
            c.company_username = uname
            c.company_realname = fname
            c.company_password = password1
            c.save()
            message = "Data Saved --"+password1+'-----'+password2
            messages.success(request,'Company Registered Successfully')
            return render(request,'company_register.html',{'msg':message})

    else:
        return render(request,'company_register.html')

def admin_login_func(request):
    uname = None
    if request.method == 'POST':

        uname = request.POST['admin_username']
        password = request.POST['admin_password']
        print(uname,password)
        compname = request.session['companyuser']
        if admin_detail.objects.filter(admin_username = uname , admin_password= password,company_username=compname).count() > 0:
            request.session['adminuser'] = uname.strip()
            cname = admin_detail.objects.get(admin_username = uname,company_username=compname)
            request.session['adminrealname'] = cname.admin_realname.upper()
            print(cname.admin_realname)
            return product_selection_func(request)
        return render(request,'admin_login.html',{'msg':request.session['companyrealname'].upper()})

    if 'companyuser' in request.session:
        # uname = request.session['companyuser']
        # cname = company_detail.objects.get(company_username = uname)
        # print(cname.company_realname)
        s = request.session['companyrealname']
        return render(request,'admin_login.html',{'msg':s.upper()})
    else:
        return render(request,'company_login.html')

def admin_register_func(request):
    message = ""
    if request.method == 'POST':
        uname = request.POST['admin_username']
        fname = request.POST['admin_fullname']
        password1 = request.POST['ps1']
        password2 = request.POST['ps2']
        c = admin_detail()
        if admin_detail.objects.filter(admin_username = uname,company_username= request.session['companyuser']) :
            print("exist")
            message = "Exist"
            messages.error(request,"Admin Already Registered")
            return render(request,'admin_register.html',{'msg':message})
        elif password1 != password2 or (password1=="" and password2==""):
            message = "Wrong password"
            messages.error(request,"Password Dont match!")
            return render(request,'admin_register.html',{'msg':message})
        else:
            c.company_username = request.session['companyuser']
            c.admin_username = uname
            c.admin_realname = fname
            c.admin_password = password1
            c.save()
            message = "Data Saved --"+password1+'-----'+password2
            messages.success(request,'Company Registered Successfully')
            return render(request,'admin_register.html',{'msg':message})
    else:
        return render(request,'admin_register.html')

def worker_login_func(request):
    uname = None
    if request.method == 'POST':
        uname = request.POST['worker_username']
        password = request.POST['worker_password']

        print(uname,password)
        c_name = request.session['companyuser']
        if worker_detail.objects.filter(worker_username = uname , worker_password= password , company_username = c_name).count() > 0:
            request.session['workeruser'] = uname.strip()
            cname = worker_detail.objects.get(worker_username = uname,company_username = c_name)
            request.session['workerrealname'] = cname.worker_realname
            print(cname.worker_realname)
            return worker_main_func(request)
        return render(request,'worker_login.html')
    if 'companyuser' in request.session:
        # uname = request.session['companyuser']
        # cname = company_detail.objects.get(company_username = uname)
        # print(cname.company_realname)
        s = request.session['companyrealname']
        return render(request,'worker_login.html',{'msg':s.upper()})
    else:
        return render(request,'company_login.html')

def worker_register_func(request):
    message = ""
    c_name = request.session['companyuser']
    if request.method == 'POST':
        uname = request.POST['worker_username']
        fname = request.POST['worker_fullname']
        password1 = request.POST['ps1']
        password2 = request.POST['ps2']
        c = worker_detail()
        if worker_detail.objects.filter(worker_username = uname,company_username = c_name) :
            print("exist")
            message = "Exist"
            messages.error(request,"Worker Already Registered")
            return render(request,'worker_register.html',{'msg':message})
        elif password1 != password2 or (password1=="" and password2==""):
            message = "Wrong password"
            messages.error(request,"Password Dont match!")
            return render(request,'worker_register.html',{'msg':message})
        else:
            c.company_username = request.session['companyuser']
            c.worker_username = uname
            c.worker_realname = fname
            c.worker_password = password1
            c.save()
            message = "Data Saved --"+password1+'-----'+password2
            messages.success(request,'Worker Registered Successfully')
            return render(request,'worker_register.html',{'msg':message})
    else:
        return render(request,'worker_register.html')

def product_selection_func(request):
    compname = request.session['companyuser']
    try:
        dat = product_detail.objects.filter(company_username = compname)
    except product_detail.DoesNotExist:
        print("Dow noooooooooooooooooo ")
        return render(request,'productselection.html')
    return render(request,'productselection.html',{'data':dat})


def dashboard_func(request , pname = '***' ):
    request.session['productuname'] = pname
    p = product_detail.objects.get(company_username = request.session['companyuser'],product_username=pname)
    request.session['productrealname'] = p.product_realname
    return render(request ,'dashboard.html',{'msg':p.product_realname})

def create_product_func(request):
    if request.method == "POST":
        l = []
        for k in request.POST.values():
            l.append(k)
        l = l[1:]

        if l[0].strip() == "" or l[1].strip() == "" :
            messages.error(request,"Invalid Input")
            return render(request,'create_product.html')
        for i in range(3,len(l),3):
            if l[i].strip() == "" or l[i+1].strip() =="" or l[i+2].strip() =="":
                messages.error(request,"Invalid Input")
                return render(request,'create_product.html')
            if l[i+1].isdigit() == False or l[i+2] == False:
                messages.error(request,"Invalid Input")
                return render(request,'create_product.html')

        c = product_detail()
        c.company_username = request.session['companyuser']
        c.product_username = l[0].strip()
        c.product_realname = l[1].strip()
        c.product_description = l[2].strip()
        c.save()

        id = 1
        for i in range(3,len(l),3):

            e = attribute_product()
            e.company_username = request.session['companyuser']
            e.product_username = l[0].strip()
            e.attribute_name = l[i].strip()
            e.attribute_required_quantity = int(l[i+1].strip())
            e.attribute_current_quantity = int(l[i+2].strip())
            e.attribute_id = id
            e.save()
            id = id+1

        print("Details Saved!")

        return redirect('product_selection')
    return render(request,'create_product.html')

def stock_analysis_func(request):
    p_uname = request.session['productuname']
    p_realname = request.session['productrealname']
    c_name = request.session['companyuser']
    if request.method == "POST":
        dvalue = request.POST.get('demand_value',0)
        dvalue = int(dvalue)
        dat = attribute_product.objects.filter(company_username = c_name,product_username = p_uname).order_by('attribute_id')
        r = []
        c = []
        f = []
        for i in dat:
            r.append(i.attribute_required_quantity)
            c.append(i.attribute_current_quantity)
            f.append(0)
        for i in range(0,len(r)):
            f[i] = c[i] - dvalue * r[i]

        d = zip(dat,f)
        return render(request,"stock_analysis.html",{"puname":p_uname,"prname":p_realname,"tdata":d})

    return render(request,"stock_analysis.html",{"puname":p_uname,"prname":p_realname})

def demand_prediction_func(request):
    #import model and print values
    if request.method == "POST":
        month = request.POST['month']
        c = request.session['companyuser']
        p = request.session['productuname']
        if history_sales_data.objects.filter(company_username=c,product_username=p).count() < 12:
            res = "Insufficient Historic Data!"
            return render(request,'demand_prediction.html',{'demand':res})
        reg = pickle.load(open('ML_models/'+c+'_'+p+'_demand.pkl','rb'))

        sample =  int(month)
        example = n.array([sample])
        example = example.reshape(len(example),-1)
        result = reg.predict(example)
        result = int(result)

        dat = history_sales_data.objects.filter(company_username=c,product_username=p).order_by('year')
        year = []
        sales = []
        for a in dat:
            year.append(a.year)
            sales.append(a.unit_sold)
            print(a.year,a.price)

        uniqueyear = []
        [uniqueyear.append(item) for item in year if item not in uniqueyear]

        chartdata = {}

        for i in uniqueyear:
            temp = []
            for j in dat:
                if i == j.year:
                    temp.append(j.unit_sold)
            chartdata[i] = temp

        print(chartdata)

        return render(request,'demand_prediction.html',{'demand':result,'cdata':chartdata})
    return render(request,'demand_prediction.html')

def price_prediction_func(request):
    #import model and print values
    if request.method == "POST":
        sales = request.POST['sales']
        month = request.POST['month']
        cost = request.POST['cost']
        sale = int(sales)
        mont = int(month)
        cos = int(cost)
        # ML Part
        c = request.session['companyuser']
        p = request.session['productuname']

        if history_sales_data.objects.filter(company_username=c,product_username=p).count() < 12:
            res = "Insufficient Historic Data"
            return render(request,'price_prediction.html',{"result":res})
        reg = pickle.load(open('ML_models/'+c+'_'+p+'_price.pkl','rb'))
        sample = []
        sample.append(mont)
        sample.append(sale)
        sample.append(cos)
        example = n.array([sample])
        example = example.reshape(len(example),-1)
        result = reg.predict(example)
        result = int(result)

        #Chart data
        dat = history_sales_data.objects.filter(company_username=c,product_username=p).order_by('year')
        year = []
        price = []
        for a in dat:
            year.append(a.year)
            price.append(a.price)
            print(a.year,a.price)

        uniqueyear = []
        [uniqueyear.append(item) for item in year if item not in uniqueyear]

        chartdata = {}

        for i in uniqueyear:
            temp = []
            for j in dat:
                if i == j.year:
                    temp.append(j.price)
            chartdata[i] = temp

        print(chartdata)
        # color = ['#FF1744','#00E676','#283593','#2979FF','#18FFFF']
        # chartdata = zip(chartdata,color)
        return render(request,'price_prediction.html',{"result":result,"cdata":chartdata})


    return render(request,'price_prediction.html')

def add_sales_data_func(request):
    # Add Historic data
    if request.method == "POST":
        month = request.POST['month']
        year = request.POST['year'].strip()
        u_produced = request.POST['u_produced'].strip()
        u_sold = request.POST['u_sold'].strip()
        cost = request.POST['cost'].strip()
        price = request.POST['price'].strip()
        c = request.session['companyuser'].strip()
        p = request.session['productuname'].strip()

        if len(year) != 4 or year.isdigit() == False:
            messages.error(request,'Invalid data')
            return render(request,'add_sales_data.html')
        try:
            month = int(month)
            u_produced = int(u_produced)
            u_sold = int(u_sold)
            cost = int(cost)
            price = int(price)
        except:
            messages.error(request,'Invalid data')
            return render(request,'add_sales_data.html')


        obj = history_sales_data()
        obj.company_username = c
        obj.product_username = p
        obj.month = month
        obj.year = year
        obj.unit_sold = u_sold
        obj.unit_produced = u_produced
        obj.cost = cost
        obj.price = price
        obj.save()


        messages.success(request,'Data Saved Successfully')
        return render(request,'add_sales_data.html')
    return render(request,'add_sales_data.html')

def inventory_status_func(request):
    p_uname = request.session['productuname']
    p_realname = request.session['productrealname']
    c_name = request.session['companyuser']
    # get data
    dat = attribute_product.objects.filter(company_username = c_name,product_username = p_uname).order_by('attribute_id')

    r = []
    c = []
    maximumid = 0
    for i in dat:
        r.append(i.attribute_required_quantity)
        c.append(i.attribute_current_quantity)
        maximumid += 1

    ans = 2147483647
    for i in range(0,len(r)):
        temp = c[i] / r[i]
        if temp < 1.0 :
            ans = 0
            break
        else:
            temp = math.floor(temp)
            if temp<ans :
                ans = temp

    if request.method == "POST":
        #Get new values from POST
        new_values = []
        for i in range(1,maximumid+1):
            a = str(i)
            j =  request.POST.get(a,0).strip()
            if j == "" :
                j = 0
            else:
                j = int(j)
                if j<0:
                    j = 0
            new_values.append(j)
        print(new_values)

        for i in range(1,maximumid+1):
            if new_values[i-1] != 0 :
                tempdata = attribute_product.objects.get(company_username = c_name,product_username = p_uname,attribute_id = i)
                print("Old ",tempdata.attribute_current_quantity," new ",tempdata.attribute_current_quantity+new_values[i-1])
                n  = tempdata.attribute_current_quantity + new_values[i-1]
                tempdata.attribute_current_quantity = n
                tempdata.save()
        #NORMAL Method
        # get data
        dat = attribute_product.objects.filter(company_username = c_name,product_username = p_uname).order_by('attribute_id')

        r = []
        c = []
        for i in dat:
            r.append(i.attribute_required_quantity)
            c.append(i.attribute_current_quantity)

        ans = 2147483647
        for i in range(0,len(r)):
            temp = c[i] / r[i]
            if temp < 1.0 :
                ans = 0
                break
            else:
                temp = math.floor(temp)
                if temp<ans :
                    ans = temp

        return render(request,'inventory_status.html',{"max_quantity":ans,"tdata":dat})
    return render(request,'inventory_status.html',{"max_quantity":ans,"tdata":dat})

def create_job_func(request):
    p_uname = request.session['productuname']
    c_name = request.session['companyuser']
    dat = all_jobs.objects.filter(company_username = c_name,product_username = p_uname).order_by('job_id')
    return render(request,'create_job.html',{"tdata":dat})

def actual_create_job_func(request):
    p_uname = request.session['productuname']
    c_name = request.session['companyuser']
    dat = attribute_product.objects.filter(company_username = c_name,product_username = p_uname).order_by('attribute_id')
    if request.method == "POST":
        last = dat.last()
        last_id = last.attribute_id

        #Get DATA from post
        jobid = request.POST['jid'].strip()
        jdesc = request.POST['jd'].strip()
        l = []
        for i in range(1,last_id+1):
            index = str(i)
            a = request.POST.get(index,0)
            if a != 0 :
                l.append(int(a))

        #error checking
        if not jobid:
            messages.error(request,"Provide valid jobid")
            return render(request,'actual_create_job.html',{"tdata":dat})
        if not l:
            messages.error(request,"Atleast select 1 attribute")
            return render(request,'actual_create_job.html',{"tdata":dat})

        #save to database
        if all_jobs.objects.filter(job_id = jobid,product_username = p_uname):
            messages.error(request,"Job ID already Exists")
            return render(request,'actual_create_job.html',{"tdata":dat})

        #SAVE IN ALL_JOBS TABLE
        c = all_jobs()
        c.company_username = c_name
        c.product_username = p_uname
        c.job_id = jobid
        c.job_desc = jdesc
        c.save()

        #Save attributes in job_detail
        for i in l:
            o = job_detail()
            o.company_username = c_name
            o.product_username = p_uname
            o.job_id = jobid
            o.attribute_id = i
            aname = dat.get(attribute_id = i)
            o.attribute_name = aname.attribute_name
            o.attribute_required_quantity = aname.attribute_required_quantity
            o.save()

        messages.success(request,"Job Created Successfully")
        return render(request,'actual_create_job.html',{"tdata":dat})
    return render(request,'actual_create_job.html',{"tdata":dat})

def show_job_func(request , _jid):
    p_uname = request.session['productuname']
    c_name = request.session['companyuser']
    dat = job_detail.objects.filter(company_username = c_name,product_username = p_uname,job_id=_jid).order_by('attribute_id')
    dat1 = all_jobs.objects.get(company_username = c_name,product_username = p_uname,job_id=_jid)
    jdesc = dat1.job_desc
    return render(request,"show_job.html",{"tdata":dat,"jid":_jid,"jdesc":jdesc})

def assign_job_func(request):
    p_uname = request.session['productuname']
    c_name = request.session['companyuser']
    dat = all_jobs.objects.filter(company_username = c_name,product_username = p_uname).order_by('job_id')
    return render(request,'assign_job.html',{"tdata":dat})

def actual_assign_job_func(request, _jid):
    p_uname = request.session['productuname']
    c_name = request.session['companyuser']
    dat1 = all_jobs.objects.get(company_username = c_name,product_username = p_uname,job_id=_jid)
    jdesc = dat1.job_desc
    #Get worker
    awdata = job_assign.objects.filter(company_username = c_name).only('worker_username')
    #wdata = worker_detail.objects.filter(company_username = c_name).order_by('worker_realname').only("worker_username","worker_realname")
    aw = []
    for i in awdata:
        aw.append(i.worker_username)
        print(i.worker_username)
    wdata = worker_detail.objects.exclude(worker_username__in = aw).only("worker_username","worker_realname","company_username")
    wdata = wdata.filter(company_username = c_name)
    nworker = wdata.count()
    l = []
    for i in range(1,nworker+1):
        l.append(i)

    wdata1 = zip(wdata,l)
    wdata2 = wdata1

    if request.method == "POST":
        numberofjobs = request.POST['njobs'].strip()
        if numberofjobs == "" or numberofjobs.isdigit() == False:
            messages.error(request,"Invalid Number of jobs")
            return render(request,'actual_assign_job.html',{"jid":_jid,"jdesc":jdesc,"wdata":wdata1})
        numberofjobs = int(numberofjobs)
        if numberofjobs <=0 :
            messages.error(request,"Invalid Number of jobs")
            return render(request,'actual_assign_job.html',{"jid":_jid,"jdesc":jdesc,"wdata":wdata1})
        instruction = request.POST['instruction'].strip()
        itime = request.POST['se_time'].strip()
        a = itime.split("-")
        sdates = a[0].strip()
        edates = a[1].strip()
        sdate = datetime.strptime(sdates,'%d/%m/%Y %I:%M %p')
        edate = datetime.strptime(edates,'%d/%m/%Y %I:%M %p')

        workerslist = []
        arb = zip(wdata,l)
        for i,j in arb:
            k = str(j)
            temp =request.POST.get(k,0)
            if k == temp:
                workerslist.append(i.worker_username)
        print(workerslist)

        for i in workerslist:
            o = job_assign()
            o.company_username = c_name
            o.product_username = p_uname
            o.job_id = _jid
            o.worker_username = i
            o.e_start_time = sdate
            o.e_end_time = edate
            o.a_start_time = sdate
            o.a_end_time = edate
            o.number_jobs = numberofjobs
            o.numer_jobs_done = numberofjobs
            o.missed_jobs = 0
            o.instruction = instruction
            o.save()


        messages.success(request,"Job Assigned Successfully")
        return render(request,'actual_assign_job.html',{"jid":_jid,"jdesc":jdesc,"wdata":wdata1})

    return render(request,'actual_assign_job.html',{"jid":_jid,"jdesc":jdesc,"wdata":wdata1})

def worker_main_func(request):
    c = request.session['companyuser']
    w_realname = request.session['workerrealname']
    w_username = request.session['workeruser']

    if request.session['workeruser'] == None:
        return worker_login_func(request)
    try:
        jobiddata = job_assign.objects.get(company_username = c,worker_username = w_username)
        jobid = jobiddata.job_id
        p = jobiddata.product_username
        n = jobiddata.numer_jobs_done
        inst = jobiddata.instruction
        request.session['productusername'] = p
        request.session['jobid'] = jobid
    except job_assign.DoesNotExist:
        jobid = -1

    #get attribute Details
    if(jobid == -1):
        messages.error(request,"No Jobs Assigned")
        return render(request,"worker_main.html",{"rname":w_realname})
    else:
        tdata = job_detail.objects.filter(company_username = c , job_id = jobid , product_username = p).order_by('attribute_id')
        return render(request,"worker_main.html",{"rname":w_realname,"tdata":tdata,"n":n,"inst":inst})
    return render(request,"worker_main.html",{"rname":w_realname})

def worker_main_save_job_api(request):
    utc = pytz.UTC
    value = request.GET.get('val', 1)
    c = request.session['companyuser']
    w = request.session['workeruser']
    p = request.session['productusername']
    j = request.session['jobid']

    try:
        jobiddata = job_assign.objects.get(company_username = c,worker_username = w,product_username = p,job_id = j);
    except:
        messages.error(request,"No Jobs Assigned")
        return render(request,'worker_main.html')
    n = jobiddata.numer_jobs_done
    exceed_flag = 0
    if(n>0):
        jobiddata.numer_jobs_done = n - 1
        #Update inventory
        jobdetail = job_detail.objects.filter(company_username = c,product_username = p , job_id = j).only('attribute_id','attribute_required_quantity')
        for i in jobdetail:
            aobj = attribute_product.objects.get(company_username = c, product_username = p ,attribute_id= i.attribute_id)
            quantity = aobj.attribute_current_quantity - i.attribute_required_quantity
            if quantity <= 0 :

                data = {
                'val' : n,
                'emsg' : "Inventory Empty!"
                }
                return JsonResponse(data)

            aobj.attribute_current_quantity = quantity
            aobj.save()
        #check date exceeds
        t = datetime.now()
        t = utc.localize(t)

        if t > jobiddata.e_end_time:
            exceed_flag = 1
            temp = jobiddata.missed_jobs
            jobiddata.missed_jobs = temp + 1
        if (jobiddata.number_jobs) == n :
            #Start time
            st = datetime.now().replace(second=0,microsecond=0)
            st = utc.localize(st)
            jobiddata.a_start_time = st
            print("Time ",st)
        elif (n-1) == 0:
            #Calculate eff
            #End time
            et = datetime.now().replace(second=0,microsecond=0)
            et = utc.localize(et)
            print("End Time ",et)
            jobiddata.a_end_time = et

            done_jobs = jobiddata.missed_jobs
            done_jobs = jobiddata.number_jobs - jobiddata.missed_jobs
            #Calc normal efficiency
            if exceed_flag == 0:
                nlabor = 0.0
                nproduction = 0.0
                noverall = 0.0
                nproduction = done_jobs / jobiddata.number_jobs
                print("NPRod",nproduction)
                e_diff = jobiddata.e_end_time - jobiddata.e_start_time
                e_sec = e_diff.total_seconds()/60
                print("Expected slice: ",e_sec)
                a_diff = et - jobiddata.a_start_time
                a_sec = a_diff.total_seconds()/60
                print("Actual Slice: ",a_sec)
                if a_sec == e_sec:
                    nlabor = 0.1
                else:
                    nlabor = 1 - (a_sec/e_sec)
                print("Nlabor",nlabor)
                noverall = nproduction * nlabor
                print(noverall)
                #Check if record in worker data
                try:
                    wdata = worker_data.objects.get(worker_username = w,company_username = c)
                    wdata.jobs_done = wdata.jobs_done +done_jobs
                    wdata.jobs_assigned = wdata.jobs_assigned + jobiddata.number_jobs
                    old_eff = wdata.efficiency
                    old_eff = old_eff * wdata.tasks_assigned
                    wdata.efficiency = (old_eff + noverall)/(wdata.tasks_assigned + 1)
                    wdata.tasks_assigned = wdata.tasks_assigned + 1
                    wdata.tasks_done = wdata.tasks_done + 1
                    wdata.worker_realname = request.session['workerrealname']
                    wdata.save()
                    print("Updated Record")

                except worker_data.DoesNotExist:
                    wobj = worker_data()
                    wobj.worker_username = w
                    wobj.company_username = c
                    wobj.jobs_done = done_jobs
                    wobj.jobs_assigned = jobiddata.number_jobs
                    wobj.tasks_done = 1
                    wobj.tasks_assigned = 1
                    wobj.efficiency = noverall
                    wdata.worker_realname = request.session['workerrealname']
                    wobj.save()
                    print("New Record Saved")

            #Missed job efficiency
            if exceed_flag == 1:
                #Missed some jobs
                try:
                    wdata = worker_data.objects.get(worker_username = w,company_username = c)
                    wdata.jobs_done = wdata.jobs_done + done_jobs
                    wdata.jobs_assigned = wdata.jobs_assigned + jobiddata.number_jobs
                    old_eff = wdata.efficiency
                    old_eff = old_eff * wdata.tasks_assigned
                    wdata.efficiency = (old_eff - 1.0)/(wdata.tasks_assigned + 1)
                    wdata.tasks_assigned = wdata.tasks_assigned + 1
                    wdata.worker_realname = request.session['workerrealname']
                    wdata.save()
                    print("Updated Record Missed")

                except worker_data.DoesNotExist:
                    wobj = worker_data()
                    wobj.worker_username = w
                    wobj.company_username = c
                    wobj.jobs_done = done_jobs
                    wobj.jobs_assigned = jobiddata.number_jobs
                    wobj.tasks_done = 0
                    wobj.tasks_assigned = 1
                    wobj.efficiency = -1.0
                    wdata.worker_realname = request.session['workerrealname']
                    wobj.save()
                    print("New Record Saved Missed")
        jobiddata.save()

    elif n == 0 :
        print("Task Done")
        n= 1
        #Delete record
        jobiddata.delete()

    data = {
    'val' : n-1,
    'emsg' : ""
    }
    return JsonResponse(data)

def worker_main_logout_api(request):
    request.session['workeruser'] = None
    print("ansdnk")
    data = {
    'status':1,
    }
    return JsonResponse(data)

def worker_main_quit_api(request):
    c = request.session['companyuser']
    w = request.session['workeruser']
    p = request.session['productusername']
    j = request.session['jobid']

    try:
        jobiddata = job_assign.objects.get(company_username = c,worker_username = w,product_username = p,job_id = j);
    except job_assign.DoesNotExist:
        messages.error(request,"No Jobs Assigned")
        return render(request,'worker_main.html')

    done_jobs = jobiddata.number_jobs - jobiddata.numer_jobs_done
    try:
        wdata = worker_data.objects.get(worker_username = w,company_username = c)
        wdata.jobs_done = wdata.jobs_done + done_jobs
        wdata.jobs_assigned = wdata.jobs_assigned + jobiddata.number_jobs
        old_eff = wdata.efficiency
        old_eff = old_eff * wdata.tasks_assigned
        wdata.efficiency = (old_eff - 1.0)/(wdata.tasks_assigned + 1)
        wdata.tasks_assigned = wdata.tasks_assigned + 1
        wdata.worker_realname = request.session['workerrealname']
        wdata.save()
        print("Updated Record Missed ")
    except worker_data.DoesNotExist:
        wobj = worker_data()
        wobj.worker_username = w
        wobj.company_username = c
        wobj.jobs_done = done_jobs
        wobj.jobs_assigned = jobiddata.number_jobs
        wobj.tasks_done = 0
        wobj.tasks_assigned = 1
        wobj.efficiency = -1.0
        wdata.worker_realname = request.session['workerrealname']
        wobj.save()
        print("New Record Saved Missed")
    jobiddata.delete()
    print("Zala")
    data = {
        'val' : 0,
        'emsg' : "Task Aborted"
    }
    return JsonResponse(data)

def workers_analysis_func(request):
    c = request.session['companyuser']
    tdata = worker_data.objects.filter(company_username = c).order_by("-efficiency")
    return render(request,"worker_analysis.html",{"tdata":tdata})
