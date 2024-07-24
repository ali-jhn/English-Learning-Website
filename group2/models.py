from django.db import models


class Person(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    exercises = models.ManyToManyField('Exercise', related_name='lessons')

    def get_lesson_details(self):
        return {'title': self.title, 'content': self.content, 'exercises': self.exercises.all()}

    def load_lesson(self):
        return self.get_lesson_details()

    def __str__(self):
        return self.title

class Exercise(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def evaluate_answers(self, user_answer):
        return self.answer.strip().lower() == user_answer.strip().lower()

    def get_feedback(self, user_answer):
        if self.evaluate_answers(user_answer):
            return "Correct!"
        else:
            return f"Incorrect. The correct answer is: {self.answer}"

    def present_exercise(self):
        return self.question

    def submit_answer(self, user_answer):
        return self.evaluate_answers(user_answer)

    def __str__(self):
        return self.question

class Search(models.Model):
    keywords = models.CharField(max_length=200)
    results = models.ManyToManyField(Lesson)

    def display_search_results(self):
        return self.results.all()

    def execute_search(self, keyword):
        self.results.set(Lesson.objects.filter(title__icontains=keyword))
        self.save()

    def __str__(self):
        return self.keywords

class Answer(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='answers')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='answers')
    user_answer = models.TextField()
    is_correct = models.BooleanField()

    def save(self, *args, **kwargs):
        self.is_correct = self.exercise.evaluate_answers(self.user_answer)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.exercise.question[:20]} - {"Correct" if self.is_correct else "Incorrect"}'

