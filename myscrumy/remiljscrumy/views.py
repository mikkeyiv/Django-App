from django.shortcuts import render,redirect,get_object_or_404
from remiljscrumy.models import ScrumyGoals,GoalStatus,ScrumyHistory,User
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .forms import SignupForm,CreateGoalForm,MoveGoalForm,DevMoveGoalForm,AdminChangeGoalForm,QAChangeGoalForm,QAChangegoal
from django.contrib.auth import authenticate,login
from django.contrib.auth.models  import User,Group
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
#from django.core.exceptions import ObjectDoesNotExist 

# Create your views here.

def index(request):
	# scrumygoals = ScrumyGoals.objects.all()
	# return HttpResponse(scrumygoals)
    if request.method == 'POST':
    #this is a method used to send data to the server   
        form = SignupForm(request.POST)
        #creates the form instance and bounds form data to it
        if form .is_valid():#used to validate the form
            #add_goal = form.save(commit=False)#save an object bounds in the form
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # password2 = form.cleaned_data.get('password1')
            # if password2 != raw_password:
            #     raise form.Http404('password must match')
            user = authenticate(username=username, password=raw_password)
            user.is_staff=True
            login(request,user)
            g = Group.objects.get(name='Developer')
            g.user_set.add(request.user)
            user.save()
            return redirect('home')
    else:
        form = SignupForm()#creates an unbound form with an empty data
    return render(request, 'remiljscrumy/index.html', {'form': form})


def filterArg(request):
    output = ScrumyGoals.objects.filter(goal_name='Learn Django')
    return HttpResponse(output)


def move_goal(request, goal_id):
    verifygoal = GoalStatus.objects.get(status_name="Verify Goal")
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    current = request.user
    group = current.groups.all()[0]
    try:
        goal = ScrumyGoals.objects.get(goal_id=goal_id)
    except ObjectDoesNotExist:
        notexist = 'A record with that goal id does not exist'
        context = {'not_exist': notexist}
        return render(request, 'remiljscrumy/exception.html', context)
    if group == Group.objects.get(name='Developer') and current == goal.user:
        form = DevMoveGoalForm()
        if request.method == 'POST':
            form = DevMoveGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goal.goal_status = choice
                goal.save()
                return HttpResponseRedirect(reverse('home'))

        else:
            form = DevMoveGoalForm()
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'current_user': current, 'group': group})
    if group == Group.objects.get(name='Developer') and current != goal.user:
        form = DevMoveGoalForm()

        if request.method == 'GET':
            notexist = 'YOU DO NO NOT HAVE THE PERMISSION TO CHANGE OTHER USERS GOAL'
            context = {'not_exist': notexist}
            return render(request, 'remiljscrumy/exception.html', context)

    if group == Group.objects.get(name='Admin'):
        form = AdminChangeGoalForm()

        if request.method == 'GET':
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
                form = AdminChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    get_status = selected_status.goal_status
                    goal.goal_status = get_status
                    goal.save()
                    return HttpResponseRedirect(reverse('home'))
        else:
            form = AdminChangeGoalForm()
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'current_user': current, 'group': group})
    if group == Group.objects.get(name='Owner') and current == goal.user:
        form = AdminChangeGoalForm()

        if request.method == 'GET':
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
                form = AdminChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    get_status = selected_status.goal_status
                    goal.goal_status = get_status
                    goal.save()
                    return HttpResponseRedirect(reverse('home'))
        else:
            form = AdminChangeGoalForm()
            return render(request, 'remiljscrumy/movegoal.html',{'form': form, 'goal': goal, 'current_user': current,  'group': group})
    # else:
    #     notexist = 'You cannot move other users goals'
    #     context = {'not_exist': notexist}
    #     return render(request, 'maleemmyscrumy/exception.html', context)

    if group == Group.objects.get(name='Quality Assurance') and current == goal.user:
        form = QAChangegoal()

        if request.method == 'GET':
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
            form = QAChangegoal(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goal.goal_status = choice
                goal.save()
                return HttpResponseRedirect(reverse('home'))
        else:
            form = QAChangegoal()
            return render(request, 'remiljscrumy/movegoal.html',{'form': form, 'goal': goal, 'currentuser': current, 'group': group})

    if group == Group.objects.get(name='Quality Assurance') and current != goal.user and goal.goal_status == verifygoal:
        form = QAChangeGoalForm()
        if request.method == 'GET':
                return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
                form = QAChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('home'))
        else:
                form = QAChangeGoalForm()
                return render(request, 'remiljscrumy/movegoal.html',{'form': form, 'goal': goal, 'currentuser': current, 'group': group})
    else: 
        notexist = 'You can only move goal from verify goals to done goals'
        context = {'not_exist': notexist}
        return render(request, 'remiljscrumy/exception.html', context)

# def move_goal(request, goal_id):
#     #response = ScrumyGoals.objects.get(goal_id=goal_id)
#     # try:
#     #goal = ScrumyGoals.objects.get(goal_id=goal_id)
#     # except ScrumyGoals.DoesNotExist:
#     #     raise Http404 ('A record with that goal id does not exist')
#     instance = get_object_or_404(ScrumyGoals,goal_id=goal_id)
#     form = MoveGoalForm(request.POST or None, instance=instance)
#     if form. is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         return redirect('home')
#     context={
#         'goal_id': instance.goal_id,
#         'user': instance.user,
#         'goal_status': instance.goal_status,
#         'form':form,
#         }
#     return render(request, 'remiljscrumy/exception.html', context)
            #move_goal = form.save(commit=False)
            # move_goal = 
            # form.save()
            # # goal_name = form.cleaned_data.get('goal_name')
            # # ScrumyGoals.objects.get(goal_name)
            # return redirect('home')
    # def form_valid(self, form):
    #          form.instance.goal_status = self.request.user
    #          return super(addgoalForm, self).form_valid(form)
    

    # }
    # return render(request, 'remiljscrumy/exception.html', context=gdict)
    #return HttpResponse(response)
    # return HttpResponse('%s is the response at the record of goal_id %s' % (response, goal_id))'''

from random import randint 
def add_goal(request):
    # existing_id = ScrumyGoals.objects.order_by('goal_id')
    # while True:
    #     goal_id = randint(1000, 10000)  #returns a random number between 1000 and 9999           
    #     if goal_id not in existing_id:        
    #         pr = ScrumyGoals.objects.create(goal_name='Keep Learning Django', goal_id=goal_id, created_by='Louis', moved_by="Louis", goal_status=GoalStatus.objects.get(pk=1), user=User.objects.get(pk=6))
    #         break
    #  form = CreateGoalForm
    # if request.method == 'POST':
    #     form = CreateGoalForm(request.POST)
    #     if form .is_valid():
    #         add_goals = form.save(commit=False)
    #         add_goals = form.save()
    #         #form.save()
    #         return redirect('home')
    # else:
    #     form = CreateGoalForm()
    return render(request, 'remiljscrumy/addgoal.html', {'form': form})

def home(request):
    '''# all=','.join([eachgoal.goal_name for eachgoal in ScrumyGoals.objects.all()])  
    # home = ScrumyGoals.objects.filter(goal_name='keep learning django')
    # return HttpResponse(all)
    #homedict = {'goal_name':ScrumyGoals.objects.get(pk=3).goal_name,'goal_id':ScrumyGoals.objects.get(pk=3).goal_id, 'user': ScrumyGoals.objects.get(pk=3).user,}
    user = User.objects.get(email="louisoma@linuxjobber.com")
    name = user.scrumygoal.all()
    homedict={'goal_name':ScrumyGoals.objects.get(pk=1).goal_name,'goal_id':ScrumyGoals.objects.get(pk=1).goal_id,'user':ScrumyGoals.objects.get(pk=1).user,
             'goal_name1':ScrumyGoals.objects.get(pk=2).goal_name,'goal_id1':ScrumyGoals.objects.get(pk=2).goal_id,'user':ScrumyGoals.objects.get(pk=2).user,
             'goal_name2':ScrumyGoals.objects.get(pk=3).goal_name,'goal_id2':ScrumyGoals.objects.get(pk=3).goal_id,'user2':ScrumyGoals.objects.get(pk=3).user}'''
   
    # form = CreateGoalForm
    # if request.method == 'POST':
    #     form = CreateGoalForm(request.POST)
    #     if form .is_valid():
    #         add_goal = form.save(commit=True)
    #         add_goal = form.save()
    # #         #form.save()
    #         return redirect('home')

    current = request.user
    week = GoalStatus.objects.get(pk=1)
    day = GoalStatus.objects.get(pk=2)
    verify = GoalStatus.objects.get(pk=3)
    done = GoalStatus.objects.get(pk=4)
    user = User.objects.all()
    weeklygoal = ScrumyGoals.objects.filter(goal_status=week)
    dailygoal = ScrumyGoals.objects.filter(goal_status=day)
    verifygoal = ScrumyGoals.objects.filter(goal_status=verify)
    donegoal = ScrumyGoals.objects.filter(goal_status=done)
    groups = current.groups.all()
    dev = Group.objects.get(name='Developer')
    owner = Group.objects.get(name='Owner')
    admin = Group.objects.get(name='Admin')
    qa = Group.objects.get(name='Quality Assurance')

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if current.is_authenticated:
        if dev in groups or qa in groups or owner in groups:
            # if request.method == 'GET':
            #     return render(request, 'remiljscrumy/home.html', context)
            form = CreateGoalForm()
            context = {'user': user, 'weeklygoal': weeklygoal, 'dailygoal': dailygoal, 'verifygoal': verifygoal,
                       'donegoal': donegoal, 'form': form, 'current': current, 'groups': groups,'dev': dev,'owner':owner,'admin':admin,'qa':qa}
        if request.method == 'POST':
            form = CreateGoalForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                status_name = GoalStatus(id=1)
                post.goal_status = status_name
                post.user = current
                post = form.save()
        elif admin in groups:
             context = {'user': user, 'weeklygoal': weeklygoal, 'dailygoal': dailygoal, 'verifygoal': verifygoal,
                       'donegoal': donegoal,'current': current, 'groups': groups,'dev': dev,'owner':owner,'admin':admin,'qa':qa}
        return render(request, 'remiljscrumy/home.html', context)

    #     else:
        #         form = WeekOnlyAddGoalForm()
        #     return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
        # if group == 'Admin':
        #     context ={
        #     'user':User.objects.all(),
        #     'weeklygoal':ScrumyGoals.objects.filter(goal_status=week),
        #     'dailygoal':ScrumyGoals.objects.filter(goal_status=day),
        #     'verifiedgoals':ScrumyGoals.objects.filter(goal_status=verify),
        #     'donegoal':ScrumyGoals.objects.filter(goal_status=done),   
        #     'current':request.user,
        #     'groups':request.user.groups.all(),
        #     'admin': Group.objects.get(name="Admin"),
        #     'owner': Group.objects.get(name='Owner'),
        #     'dev': Group.objects.get(name='Developer'),
        #     'qa': Group.objects.get(name='Quality Assurance'),}
        #     return render(request,'remiljscrumy/home.html',context=homedict)
            
        #     if request.method == 'GET':
        #         return render(request, 'remiljscrumy/home.html', context)




   
    #         