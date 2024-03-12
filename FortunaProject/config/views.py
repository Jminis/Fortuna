from django.shortcuts import render, redirect
from .models import Config
from .forms import ConfigForm

# Create your views here.
def config_view(request):
    #config 입력
    if request.method == "POST":
        form = ConfigForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('config')  # 성공적으로 저장 후 같은 뷰로 리디렉션
    else:
        form = ConfigForm()  # GET 요청 시 빈 폼 생성    
    
    #config 가져오기
    try:
        config = Config.objects.latest('created_at')
        context = {'config': config, 'form': form}
    except Config.DoesNotExist:
        context = {'form': form}  # Config 데이터가 없을 경우 form만 컨텍스트에 추가

    return render(request, 'config/config.html', context)

def not_in_progess_view(request):
    return render(request, 'config/not_in_progress.html')


