from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Lesson, Exercise, Search, Person, Answer


def select_topic(request):
    lessons = Lesson.objects.all()
    return render(request, 'select_topic.html', {'lessons': lessons})

def view_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'view_lesson.html', {'lesson': lesson})

def search_lesson(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        search = Search.objects.create(keywords=keyword)
        search.execute_search(keyword)
        return render(request, 'search_results.html', {'results': search.display_search_results()})
    return render(request, 'search.html')

@login_required
def submit_answer_view(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.method == 'POST':
        user_answer = request.POST.get('user_answer')
        person = Person.objects.get(username=request.user.username)
        if Answer.objects.filter(user=person, exercise=exercise).exists():
            feedback = "You have already answered this exercise."
        else:
            Answer.objects.create(
                user=person,
                exercise=exercise,
                user_answer=user_answer
            )

            feedback = exercise.get_feedback(user_answer)

        return render(request, 'submit_answer.html', {'exercise': exercise, 'feedback': feedback})

    return render(request, 'submit_answer.html', {'exercise': exercise})

@login_required
def progress_view(request, user_id):
    user_answers = Answer.objects.filter(user__id=user_id).select_related('exercise')

    total_answers = user_answers.count()
    correct_answers = user_answers.filter(is_correct=True).count()
    progress = (correct_answers / total_answers) * 100 if total_answers > 0 else 0

    return render(request, 'user_progress.html', {
        'user_answers': user_answers,
        'progress': progress,
        'total_answers': total_answers,
        'correct_answers': correct_answers,
    })