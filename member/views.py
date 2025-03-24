from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from member.forms import SignupForm
from utils.email import send_email

User = get_user_model()


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

        # 이메일 발송
        signer = TimestampSigner()  # 특정 정보를 암호화해서 보냄
        # 1. 이메일에 서명
        signed_user_email = signer.sign(user.email)
        # 2. 서명된 이메일을 직렬화
        signer_dump = signing.dumps(signed_user_email)
        # print(signer_dump)
        # # 3. 직렬화된 데이터를 역직렬화
        # decoded_user_email = signing.loads(signer_dump)
        # print(decoded_user_email)
        # # 4. 타임스탬프 유효성 검사 포함하여 복호화
        # email = signer.unsign(decoded_user_email, max_age = 60 * 30)  # 30분 설정
        # print(email)


        # http://localhost:8000/verify/?code=asdfasd
        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}'
        # print(url)
        if settings.DEBUG:
            print(url)
        else:
            subject = '[Pystagram]이메일 인증을 완료해주세요'
            message = f'다음 링크를 클릭해주세요. <br><a href="{url}">{url}</a>'

            send_email(subject, message, user.email)

        return render(
            self.request,
            template_name= 'auth/signup_done.html',
            context={'user':user}
        )


def verify_email(request):
    code = request.GET.get('code', '')  # code가 없으면 공백으로 처리
    signer = TimestampSigner()
    try:
        # 3. 직렬화된 데이터를 역직렬화
        decoded_user_email = signing.loads(code)
        # 4. 타임스탬프 유효성 검사 포함하여 복호화
        email = signer.unsign(decoded_user_email, max_age = 60 * 5)  # 5분 설정
    # except Exception as e:  # 이렇게 처리 많이 하지만 에러를 지정해서 하는게 제일 좋음.
    except (TypeError, SignatureExpired):  # 시간 지나서 오류발생하면 오류처리
        return render(request, 'auth/not_verified.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()

    # TODO: 나중에 Redirect 시키기
    # return redirect(reverse('login'))  # 원래 해야하는 동작
    return render(request, 'auth/email_verified_done.html', {'user':user})
#
