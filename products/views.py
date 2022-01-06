from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
from products.models import Product, ProductReal
from questions.forms import QuestionForm
from questions.models import Question


def products_list(request: HttpRequest):
    kw = request.GET.get('kw', default='')
    product_list = Product.objects.order_by('-id')
    product_list = product_list.filter(
        Q(display_name__icontains=kw)  # 상품명검색
    ).distinct()

    page = request.GET.get('page', '1')
    paginator = Paginator(product_list, 8)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    return render(request, 'products/product_list.html', {
        'product_list': page_obj,
    })


def _products_detail(request: HttpRequest, product_id):
    product_detail = get_object_or_404(Product, pk=product_id)
    product_reals = product_detail.product_reals.all()
    questions = Question.objects.filter(object_id=product_id)
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.content_type = ContentType.objects.get_for_model(product)
            question.object_id = product.id
            question.user_id = request.user.id
            question.save()
            messages.success(request, "질문이 등록되었습니다.")
            return redirect("products:detail", product_id=product.id)
    else:
        form = QuestionForm()
    return render(request, 'products/product_detail.html', {
        'products': product_detail,
        'product_reals': product_reals,
        'questions': questions,
        "question_form": form,
    })


def products_detail(request: HttpRequest, product_id):
    return _products_detail(request, product_id)


@login_required(login_url='accounts:signin')
def question_create(request: HttpRequest, product_id):
    return _products_detail(request, product_id)


def question_delete(request: HttpRequest, product_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    messages.success(request, "질문이 삭제되었습니다.")

    return redirect("products:detail", product_id=product_id)


def question_modify(request: HttpRequest, product_id, question_id):
    product = get_object_or_404(Product, id=product_id)
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "질문이 수정되었습니다.")
            return redirect("products:detail", product_id=product_id)
        else:
            form = QuestionForm(None, instance=question)

    return render(request, "products/question_modify.html", {
        "products": product,
        "questions": question,
        "question_form": form,
    })
