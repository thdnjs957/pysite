from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Subquery, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User


def list(request):

    PAGE_ROW_COUNT = 5
    PAGE_DISPLAY_COUNT = 5

    board_all_list = Board.objects.all().order_by('-id')  # 전체 리스트 가져오기

    paginator = Paginator(board_all_list, PAGE_ROW_COUNT)

    page_num = request.GET.get('pageNum')  # list에서 넘긴 pageNum

    totalPageCount = paginator.num_pages  # 전체 페이지 갯수

    try:
        board_list = paginator.page(page_num)
    except PageNotAnInteger:
        board_list = paginator.page(1)
        page_num = 1
    except EmptyPage:
        board_list = paginator.page(paginator.num_pages)
        page_num = paginator.num_pages

    page_num = int(page_num)

    startpage_num = 1 + ((page_num - 1) / PAGE_DISPLAY_COUNT) * PAGE_DISPLAY_COUNT
    endpage_num = startpage_num + PAGE_DISPLAY_COUNT - 1

    if totalPageCount < endpage_num:
        endpage_num = totalPageCount

    bottomPages = range(int(startpage_num), endpage_num + 1)

    data = {
            'board_list': board_list,
            'page_num': page_num,
            'bottomPages': bottomPages,
            'totalPageCount': totalPageCount,
            'startpage_num': startpage_num,
            'endpage_num': endpage_num
        }

    return render(request, 'board/list.html', data)

def writeform(request):
    if request.method == 'GET' and 'id' in request.GET:
        id = request.GET['id']
    else:
        id = 0

    data = {
        'id': id
    }
    # data = {'boardlist': board}
    return render(request, 'board/write.html', data)


def write(request):
    board_id = request.POST['id']
    if board_id == '0':  # 그냥 글쓰기이면
        board = Board()
        board.title = request.POST['title']
        board.content = request.POST['content']

        value = Board.objects.aggregate(max_groupno=Max('groupno'))['max_groupno'] or 0

        if board.groupno == 0:
            board.groupno = value + 1

        user = User.objects.get(id=request.session['authuser']['id'])
        board.user = user
        board.save()

    else:  # 답글이면

        # 해당 board_id에 해당하는 객체 가져오기
        board = Board.objects.get(id=board_id)
        print(board.groupno)

        # updateOrderNo
        # 여러행 업데이트
        Board.objects.filter(groupno=board.groupno).filter(orderno__gte=board.orderno).update(orderno=F('orderno')+1)

        # insertReply
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.groupno = board.groupno
        board.orderno = board.orderno + 1
        board.depth = board.depth + 1
        user = User.objects.get(id=request.session['authuser']['id'])
        board.user = user

        board.save()

    return HttpResponseRedirect('/board')

def view(request, id=0):
    # user = User.objects.get(id=request.session['authuser']['id'])  # 쿼리가 들어간거임 db에서 가져옴 dictionary
    # data = {
    #     'user': user
    # }
    board = Board.objects.get(id=id)

    Board.objects.filter(id=board.id).update(hit=board.hit + 1)

    print(board.hit, type(board.hit))
    data = {'board': board}

    return render(request, 'board/view.html', data)

def modifyform(request, id=0):
    board = Board.objects.get(id=id)
    data = {
        'board': board
    }
    return render(request, 'board/modify.html', data)

def modify(request, id=0):
    board = Board.objects.get(id=id)
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.save()  # update 해줌
    print(board.id, type(board.id))  # board.id는 int임
    return HttpResponseRedirect('/board/view/' + str(board.id) + '?result=success')

def delete(request, id=0):
    board = Board.objects.filter(id=id)
    board.delete()
    return HttpResponseRedirect('/board')



