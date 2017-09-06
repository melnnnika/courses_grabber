from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, Instructor


def index(request):
    categories = ''
    providers = ''
    sources = ''
    language = ''
    duration = ''
    if request.GET.get('c'):
        categories = request.GET.get('c')
    if request.GET.get('p'):
        providers = request.GET.get('p')
    if request.GET.get('s'):
        sources = request.GET.get('s')
    if request.GET.get('l'):
        language = request.GET.get('l')
    if request.GET.get('d'):
        duration = request.GET.get('d')

    courses_list = Course.objects.all()
    if categories:
        courses_list = courses_list.filter(category__in=categories.split('_'))
    if providers:
        courses_list = courses_list.filter(provider__in=providers.split('_'))
    if sources:
        courses_list = courses_list.filter(source__in=sources.split('_'))
    if language:
        courses_list = courses_list.filter(language__in=language.split('_'))
    if duration:
        courses_list = courses_list.filter(duration_filter__in=duration.split('_'))

    filter_category = Course.objects.order_by('category').values_list('category', flat=True).distinct()
    filter_provider = Course.objects.order_by('provider').values_list('provider', flat=True).distinct()
    filter_source = Course.objects.order_by('source').values_list('source', flat=True).distinct()
    filter_lang = Course.objects.order_by('language').values_list('language', flat=True).distinct()
    filter_duration = Course.objects.exclude(duration_filter__isnull=True).order_by('duration_filter').values_list('duration_filter', flat=True).distinct()

    paginator = Paginator(courses_list, 10)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    index = courses.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 10 if index >= 10 else 0
    end_index = index + 10 if index <= max_index - 10 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'courses_list': courses,
        'filter_category': filter_category,
        'filter_provider': filter_provider,
        'filter_source': filter_source,
        'filter_lang': filter_lang,
        'filter_duration': filter_duration,
        'page_range': page_range
    }
    return render(request, 'index.html', context)


def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    video = ''
    if course.video:
        video = course.video.replace("watch?v=", "embed/")
    instructors = Instructor.objects.filter(course=course_id)
    return render(request, 'detail.html', {'course': course, 'instructors': instructors, 'video': video})
