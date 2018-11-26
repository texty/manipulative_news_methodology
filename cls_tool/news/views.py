from django.shortcuts import render
from . import models, forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict


@login_required
def classify(request):
    if request.method == 'POST':
        form = forms.NewClassify(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/classifier/')

    else:
        explanations = ';;'.join([t.description for t in models.FakeType.objects.all()])
        classified_new = models.Article.objects.filter(bee=request.user
                                                       ).exclude(html_id__in=models.Classified.objects.all(
                                                       ).values('article')
                                                       ).order_by('?'
                                                       ).first()
        form = forms.NewClassify(initial={'article': classified_new})
        feedback = forms.FeedbackForm(initial={'article': classified_new})
        done_counter = models.Classified.objects.filter(article__bee=request.user).count()

        return render(request, 'classifier.html', {'cls_new': classified_new,
                                                   'form': form,
                                                   'type_explanations': explanations,
                                                   'feedback': feedback,
                                                   'done_counter': done_counter,
                                                   })


@login_required
def edit(request):
    selected_type = request.GET.get('type')

    print(request.GET.get('types'))
    types = models.FakeType.objects.all()
    if not selected_type or selected_type == 'all':
        classified_before = models.Classified.objects.filter(article__bee=request.user
                                                             ).order_by('-classified_at')
    else:
        classified_before = models.Classified.objects.filter(article__bee=request.user
                                                             ).filter(types__label=selected_type
                                                             ).order_by('-classified_at')
    paginator = Paginator(classified_before, 15)

    page = request.GET.get('page')
    try:
        done = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        done = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        done = paginator.page(paginator.num_pages)

    return render(request, 'list_done.html', {'done': done,
                                              'types': types,
                                              'selected_type': selected_type})


@login_required
def edit_done(request, pk):
    article = models.Classified.objects.get(article__html_id=pk)
    if request.method == 'POST':
        form = forms.NewClassify(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/classifier/done/')
    else:
        explanations = ';;'.join([t.description for t in models.FakeType.objects.all()])

        feedback = forms.FeedbackForm(initial={'article': article.article})
        form = forms.NewClassify(instance=article, data=model_to_dict(article))

        return render(request, 'edit_done.html', {'form': form,
                                                  'cls_article': article,
                                                  'type_explanations': explanations,
                                                  'feedback': feedback,
                                                  })


@login_required
def feedback(request):
    if request.method == 'POST':
        feedback = forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
            return JsonResponse({'ok': True})
