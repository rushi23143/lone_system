from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from .forms import RegisterForm, LoanForm, LoginForm
from.models import MyUser, InternalTeam
from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta


# Create your views here.


def index(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            dob = form.cleaned_data['date_of_birth']
            mobile = form.cleaned_data['mobile']
            pan = form.cleaned_data['pan']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            password = request.POST['password']
            current_date = date.today()

            birth_year = dob.year
            birth_month = dob.month
            birth_day = dob.day

            current_year = current_date.year
            current_month = current_date.month
            current_day = current_date.day

            age = current_year-birth_year-((current_month, current_day) < (birth_month, birth_day))
            mob = str(mobile)
            print(type(mobile))

            if len(mob) == 10 and type(mobile) == int and age > 18:
                if MyUser.objects.filter(email=email).exists():
                    messages.info(request, 'email already exist, try login!')
                    redirect('register')
                else:
                    query = MyUser.objects.create(fullname=name, email=email, date_of_birth=dob, mobile=mob, pan=pan,
                                                  address=address, city=city, state=state, password=password,
                                                  date_of_issue=timezone.now())
                    query.save()
                    return redirect('detail_form')
            else:
                if age < 18:
                    messages.error(request, 'your age is below 18!')
                else:
                    messages.error(request, "Sorry, you can't register! please check your mobile no.")
    else:
        form = RegisterForm()
    return render(request, 'index.html', {'form': form})


def detail_form(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            print('valid')
            email = form.cleaned_data['email']
            amount = form.cleaned_data['loan_amount']
            year = form.cleaned_data['tenure_year']
            month = form.cleaned_data['tenure_month']
            rate = form.cleaned_data['rate_of_interest']

            rate1 = float(rate)
            rate_percent = rate1/100

            compounded = int(year)*12+int(month)
            due_date = date.today() + relativedelta(months=+compounded)

            final_rate = round(rate_percent/12, 3)

            if amount <= 100000:
                messages.error(request, 'Done')
                A = int(amount)*((1+final_rate)**compounded)
                final_amount = round(A)
                interest_amount = round(final_amount - amount)
                user = MyUser.objects.get(email=email)
                name = user.fullname
                query = InternalTeam.objects.create(name=name, email=email, loan_amount=amount,
                                                    tenure_period=compounded, rate_of_interest=rate,
                                                    interest_amount=interest_amount, amount_to_be_paid=final_amount,
                                                    final_rate=final_rate, due_date=due_date)
                query.save()
                print(final_amount, interest_amount)

                return redirect('thank_you')
            else:
                messages.error(request, 'Amount exceeds!')
                return redirect('detail_form')
    else:
        print('not valid')
        form = LoanForm()
    return render(request, 'detail_form.html', {'form': form})


def dashboard(request):
    queries = InternalTeam.objects.all()
    return render(request, 'dashboard.html', {'queries': queries})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if MyUser.objects.filter(email=email).exists():
                user = MyUser.objects.get(email=email)
                user_pass = user.password
                if password == user_pass:
                    return redirect('detail_form')
                else:
                    messages.error(request, 'Login failed!')
                    return redirect('login')
            elif not MyUser.objects.filter(email=email).exists():
                messages.error(request, 'Register First!')
                return redirect('login')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def view_query(request, pk):
    query = get_object_or_404(InternalTeam, pk=pk)
    return render(request, 'view_details.html', {'query': query})


def thank_you(request):
    return render(request, 'thank_you.html')


def team_login(request):
    if request.method == "POST":
        uname = request.POST['un1']
        pwd = request.POST['pswd1']
        user = auth.authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                auth.login(request, user)
                messages.info(request, 'Successfully Logged In')
                return redirect('dashboard')
        except:
            messages.info(request, "invalid credentials!")
            return redirect('team_login')
    else:
        return render(request, 'team_login.html')


def team_logout(request):
    auth.logout(request)
    return redirect('team_login')
