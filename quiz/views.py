from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from quiz.models import Question, Score, ActiveSet
import random
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your views here.
def index(request):
	#Ordered Score
	l=[]
	for i in range(30):
		score = Score.objects.filter(question_number=(i+1))
		if score:
			l.append(score[0])
		else:
			l.append('')

	message = request.session.pop('message', "no message")

	if message != "no message":
		return render(request,'index.html',{'scores':l,'message':message})
	else:
		return render(request,'index.html',{'scores':l})

@login_required
def detail(request,question_id):
	#Randomly show questions that are unanswered
	active_questions = ActiveSet.objects.filter(question__question_status="unanswered")
	if not active_questions:
		return redirect('gen active')


	question_active = random.choice(active_questions).question
	#The moment the question is shown, it's attempted, and shall not be shown again
	question = Question.objects.get(id=question_active.id)
	question.question_status="attempted"
	question.save()
	return render(request,'question.html',{
		'qn':question,
		'qn_id':question_id
	})

@login_required
def reset_questions(request):
	questions = Question.objects.exclude(question_status='unanswered')

	# for question in questions:
	# 	question.question_status="unanswered"
	# 	question.save()
	questions.update(question_status="unanswered")
	request.session['message'] = "Question reset"
	return redirect('index')

@login_required
def reset_scores(request):
	Score.objects.all().delete()

	#passing message through sessions
	request.session['message'] = "Score reset"
	return redirect('index')

@login_required
def answer(request,question_id):
	
	real_question_id = request.POST.get('id')
	apparent_question_id= question_id
	choice = request.POST.get('choice')

	question_answer = Question.objects.get(id=real_question_id).answer
	result = "wrong"
	if str(question_answer) == choice:
		result = "correct"

	return JsonResponse({'result': result})

@login_required
def scoring(request,question_id):
	schools = [static('image/hci.png'),static('image/dhs.png'),static('image/jjc.jpg'),static('image/rv.png'),static('image/ejc.jpg')]
	choice = int(request.POST.get('choice'))
	#score = Score(question_number=question_id,answered_correct_by= (choice-1))
	score = Score(question_number=question_id,answered_correct_by=schools[choice-1])
	score.save()

	return redirect('index')

@login_required
def createSet(request):
	#clear the active sets first
	ActiveSet.objects.all().delete()

	#grab by ratio
	question_ens = Question.objects.filter(question_status="unanswered",question_type='EN')
	question_cns = Question.objects.filter(question_status="unanswered",question_type='CN')
	question_enr = list(question_ens)
	question_cnr = list(question_cns)
	random.shuffle(question_enr)
	random.shuffle(question_cnr)
	question_en=question_enr[:10]
	question_cn=question_cnr[:20]
	#check if enough qn
	if not question_en or not question_cn:
		request.session['message'] = "Not enough questions"
		return redirect('index')

	#push questions into active set
	for question in question_en:
		a = ActiveSet(question=question)
		a.save()
	for question in question_cn:
		a = ActiveSet(question=question)
		a.save()

	request.session['message'] = "Active set created"
	return redirect('index')
