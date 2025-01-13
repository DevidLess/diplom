from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Lawyer, Review
from .forms import ReviewForm
from django.db.models import Avg, Count


# @login_required
# def lawyer_list(request):
#     lawyers = Lawyer.objects.all()
#     return render(request, 'lawyers/lawyer_list.html', {'lawyers': lawyers})

@login_required
def lawyer_list(request):
    # Получаем параметры сортировки из запроса
    sort_by = request.GET.get('sort', None)  # По умолчанию сортировка не применяется

    # Аннотируем юристов средним рейтингом и количеством отзывов
    lawyers = Lawyer.objects.annotate(
        avg_rating=Avg('reviews__score'),
        review_count=Count('reviews')
    )

    # Применяем сортировку в зависимости от параметра
    if sort_by == 'rating_asc':
        lawyers = lawyers.order_by('avg_rating')
    elif sort_by == 'rating_desc':
        lawyers = lawyers.order_by('-avg_rating')
    elif sort_by == 'reviews_asc':
        lawyers = lawyers.order_by('review_count')
    elif sort_by == 'reviews_desc':
        lawyers = lawyers.order_by('-review_count')

    return render(request, 'lawyers/lawyer_list.html', {'lawyers': lawyers})


@login_required
def lawyer_detail(request, lawyer_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)

    # Проверяем, оставлял ли текущий пользователь отзыв на этого юриста
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(lawyer=lawyer, user=request.user).exists()

    # Получаем параметр сортировки из запроса
    sort_by = request.GET.get('sort', '-created_at')  # По умолчанию сортируем по дате (новые сначала)

    # Получаем параметр фильтрации из запроса
    filter_by = request.GET.get('filter', None)  # По умолчанию фильтрация отключена

    # Фильтруем отзывы
    reviews = lawyer.reviews.all()
    if filter_by == 'my_reviews' and request.user.is_authenticated:
        reviews = reviews.filter(user=request.user)  # Фильтруем только отзывы текущего пользователя

    # Сортируем отзывы
    if sort_by == 'score_asc':
        reviews = reviews.order_by('score')
    elif sort_by == 'score_desc':
        reviews = reviews.order_by('-score')
    else:
        reviews = reviews.order_by('-created_at')  # По умолчанию

    if request.method == 'POST' and not user_has_reviewed:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.lawyer = lawyer
            review.user = request.user
            review.save()
            return redirect('lawyers:lawyer_detail', lawyer_id=lawyer.id)
    else:
        form = ReviewForm()

    return render(request, 'lawyers/lawyer_detail.html', {
        'lawyer': lawyer,
        'reviews': reviews,
        'form': form,
        'user_has_reviewed': user_has_reviewed,
        'sort_by': sort_by,  # Передаем текущий параметр сортировки в шаблон
        'filter_by': filter_by,  # Передаем текущий параметр фильтрации в шаблон
    })


# @login_required
# def lawyer_detail(request, lawyer_id):
#     lawyer = get_object_or_404(Lawyer, id=lawyer_id)

#     # Проверяем, оставлял ли текущий пользователь отзыв на этого юриста
#     user_has_reviewed = False
#     if request.user.is_authenticated:
#         user_has_reviewed = Review.objects.filter(lawyer=lawyer, user=request.user).exists()

#     # Получаем параметр сортировки из запроса
#     sort_by = request.GET.get('sort', '-created_at')  # По умолчанию сортируем по дате (новые сначала)

#     # Сортируем отзывы
#     if sort_by == 'score_asc':
#         reviews = lawyer.reviews.all().order_by('score')
#     elif sort_by == 'score_desc':
#         reviews = lawyer.reviews.all().order_by('-score')
#     else:
#         reviews = lawyer.reviews.all().order_by('-created_at')  # По умолчанию

#     if request.method == 'POST' and not user_has_reviewed:
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.lawyer = lawyer
#             review.user = request.user
#             review.save()
#             return redirect('lawyers:lawyer_detail', lawyer_id=lawyer.id)
#     else:
#         form = ReviewForm()

#     return render(request, 'lawyers/lawyer_detail.html', {
#         'lawyer': lawyer,
#         'reviews': reviews,
#         'form': form,
#         'user_has_reviewed': user_has_reviewed,
#         'sort_by': sort_by,  # Передаем текущий параметр сортировки в шаблон
#     })


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Только автор может редактировать
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('lawyers:lawyer_detail', lawyer_id=review.lawyer.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'lawyers/edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Только автор может удалить
    lawyer_id = review.lawyer.id
    review.delete()
    return redirect('lawyers:lawyer_detail', lawyer_id=lawyer_id)


@login_required
def confirm_delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Только автор может удалить
    if request.method == 'POST':
        lawyer_id = review.lawyer.id
        review.delete()
        return redirect('lawyers:lawyer_detail', lawyer_id=lawyer_id)
    return render(request, 'lawyers/confirm_delete_review.html', {'review': review})