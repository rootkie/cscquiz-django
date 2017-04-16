from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_status = models.CharField(max_length=20,default="unanswered")
    question_type = models.CharField(max_length=20,default='CN')
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    answer = models.IntegerField(default=0)

    def __str__(self):
    	 return self.question_text

class Score(models.Model):
	question_number = models.IntegerField()
	answered_correct_by = models.CharField(max_length=100,default="NA")
	def __str__(self):
		return self.answered_correct_by

class ActiveSet(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)