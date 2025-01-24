from django.db import models


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.group_name}'


class AdvancedUserProfile(models.Model):
    profile_id = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    user_status = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.profile_id} {self.email} {self.password} {self.created_at} {self.user_status}'


class Topic(models.Model):
    title = models.CharField(max_length=256, unique=True)
    time_to_pass = models.DurationField(default=0)
    is_open = models.BooleanField(default=False)
    question_in_test = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} {self.time_to_pass} {self.is_open} {self.question_in_test}'


class Question(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=256)
    img_ref = models.ImageField(upload_to='images/question/%Y/%m/%d/')

    def __str__(self):
        return f'{self.topic_id} {self.question_text} {self.img_ref}'


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=256)
    img_ref = models.ImageField(upload_to='images/answer/%Y/%m/%d/')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question_id} {self.answer_text} {self.img_ref} {self.is_correct}'


class Result(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    passed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id} {self.topic_id} {self.score} {self.passed_at}'
