from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from member.forms import SignupForm


class SignupView(FormView):
    template_name = 'auth/signup.html'  # 템플릿 설정
    form_class = SignupForm  # 폼 설정
    # success_url = reverse_lazy('signup_done')  # 완료시 url
    # success_url은 클래스가 로딩될 때 설정됩니다.
    # 만약 reverse()를 쓴다면, 클래스가 로딩될 시점에 URLConf가 완전히 로딩되지 않았을 수도 있어
    # ImportError 또는 ImproperlyConfigured 오류가 발생할 수 있습니다.
    # reverse_lazy() → 나중에 실제로 URL이 필요할 때 계산 (지연 평가)

    def form_valid(self,form):
        # form.save()
        # return HttpResponseRedirect(self.get_success_url())

        user = form.save()
        return render(
            self.request,
            template_name= 'auth/signup_done.html',
            context={'user':user}
        )



