from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count

from .models import Answer, Choice, Question, Survey, SurveyCompletion

SESSION_KEY = 'survey_progress'  

def _get_identity(request):
    if request.user.is_authenticated:
        return request.user, None
    if not request.session.session_key:
        request.session.create()
    return None, request.session.session_key


def _already_completed(survey, user, session_key):
    qs = SurveyCompletion.objects.filter(survey=survey)
    if user:
        return qs.filter(user=user).exists()
    return qs.filter(session_key=session_key).exists()


def survey_list(request):
    surveys = Survey.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'surveys/list.html', {'surveys': surveys})


def start_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, is_active=True)
    user, session_key = _get_identity(request)

    if _already_completed(survey, user, session_key):
        if not survey.allow_retake:
            return render(request, 'surveys/already_passed.html', {'survey': survey})
        answer_filter = {'question__survey': survey}
        answer_filter.update({'user': user} if user else {'session_key': session_key})
        Answer.objects.filter(**answer_filter).delete()
        SurveyCompletion.objects.filter(survey=survey).filter(
            user=user if user else None, session_key=session_key if not user else None
        ).delete()

    request.session[SESSION_KEY] = {'survey_id': survey.id, 'current': 0, 'answers': {}}
    request.session.modified = True
    return redirect('surveys:question', survey_id=survey.id)


def question_view(request, survey_id):
    progress = request.session.get(SESSION_KEY)
    if not progress or progress['survey_id'] != survey_id:
        return redirect('surveys:start', survey_id=survey_id)

    survey = get_object_or_404(Survey, pk=survey_id)
    questions = list(survey.questions.all())
    idx = progress['current']

    if idx >= len(questions):
        return _finish_survey(request, survey)

    question = questions[idx]

    if request.method == 'POST':
        if question.question_type == Question.TEXT:
            progress['answers'][str(question.id)] = request.POST.get('text_answer', '')
        else:
            choice_ids = request.POST.getlist('choice')
            progress['answers'][str(question.id)] = choice_ids

        progress['current'] += 1
        request.session[SESSION_KEY] = progress
        request.session.modified = True
        return redirect('surveys:question', survey_id=survey.id)

    return render(request, 'surveys/question.html', {
        'survey': survey,
        'question': question,
        'step': idx + 1,
        'total': len(questions),
    })


def _finish_survey(request, survey):
    progress = request.session.get(SESSION_KEY)
    user, session_key = _get_identity(request)

    for question_id, value in progress['answers'].items():
        question = Question.objects.get(pk=question_id)
        answer = Answer.objects.create(
            question=question,
            user=user,
            session_key=session_key,
            text_answer=value if question.question_type == Question.TEXT else None,
        )
        if question.question_type != Question.TEXT:
            answer.selected_choices.set(Choice.objects.filter(id__in=value))

    SurveyCompletion.objects.create(survey=survey, user=user, session_key=session_key)

    del request.session[SESSION_KEY]
    request.session.modified = True
    return redirect('surveys:thanks', survey_id=survey.id)


def thanks_view(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    return render(request, 'surveys/thanks.html', {'survey': survey})


@staff_member_required
def results_view(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    questions = survey.questions.prefetch_related('choices', 'answers')

    report = []
    for question in questions:
        item = {'question': question, 'type': question.question_type}
        if question.question_type == Question.TEXT:
            item['text_answers'] = list(
                question.answers.exclude(text_answer='').values_list('text_answer', flat=True)
            )
        else:
            item['choice_stats'] = (
                question.choices
                .annotate(votes=Count('answers'))
                .order_by('-votes')
            )
            item['total_respondents'] = question.answers.count()
        report.append(item)

    return render(request, 'surveys/results.html', {
        'survey': survey,
        'report': report,
        'total_completions': survey.completions.count(),
    })
