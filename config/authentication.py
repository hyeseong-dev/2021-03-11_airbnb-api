import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.response import Response
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication): # DRF의 Token방식과 JWT의 차이 DB저장 유무(JWT는 저장하지 않음)
    def authenticate(self, request):                        # 서버 측면에서 더 효율적임 2만명이 로그인을 해도 디비에서 저장하는 것은 아무것도 없음
        try:                                                # 리프레쉬 토큰이 현재 구현 되지 않은 부분이 있음
            token = request.META.get("HTTP_AUTHORIZATION") # 헤더에 관한 정보는 MEATA속성에 있음
            if token is None:
                return None
            xjwt, jwt_token = token.split(" ") #관습적으로 
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            pk = decoded.get("pk")
            user = User.objects.get(pk=pk)
            return (user,None) # tuple, list로 안넘기면 오류남 cannot unpack non-iterable User object
        except ValueError:
            return None
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(detail="JWT Format Invalid")
            # return Response(status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
