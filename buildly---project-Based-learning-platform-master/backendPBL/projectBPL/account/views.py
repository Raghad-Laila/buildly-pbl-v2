from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from .serializers import (
    RegisterLearnerSerializer, 
    RegisterAdminSerializer, 
    LoginSerializer, 
    ProfileSerializer,
    ChangePasswordSerializer,
)
from .models import CustomUser


def build_user_response(user, request=None):
    serializer = ProfileSerializer(user, context={'request': request})
    return serializer.data

class RegisterLearnerView(generics.CreateAPIView):
    """إنشاء حساب متعلم"""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterLearnerSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        user_data = build_user_response(user, request)
        
        return Response({
            'message': _('تم إنشاء حساب المتعلم بنجاح'),
            'user': user_data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class RegisterAdminView(generics.CreateAPIView):
    """إنشاء حساب مشرف"""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterAdminSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': _('تم إنشاء حساب المشرف بنجاح'),
            'user': build_user_response(user, request),
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """تسجيل الدخول"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': _('تم تسجيل الدخول بنجاح'),
            'user': build_user_response(user, request),
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

class LogoutView(APIView):
    """تسجيل الخروج"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            
            if not refresh_token:
                return Response({
                    'error': _('refresh_token مطلوب')
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # إضافة التوكن للقائمة السوداء
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # تسجيل خروج Django
            logout(request)
            
            return Response({
                'message': _('تم تسجيل الخروج بنجاح')
            }, status=status.HTTP_205_RESET_CONTENT)
            
        except Exception as e:
            return Response({
                'error': _('حدث خطأ أثناء تسجيل الخروج'),
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    """عرض وتعديل الملف الشخصي"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        response_data = {
            'message': _('تم جلب بيانات الملف الشخصي'),
            'user': serializer.data,
            'quiz_info': {
                'is_rated': instance.is_rated,
                'level': instance.level
            }
        }
        
        if instance.is_learner:
            response_data['enrollment_info'] = {
                'enrolled_courses_count': instance.get_enrolled_courses_count(),
                'enrolled_courses_titles': instance.get_enrolled_courses_list(),
                'note': _('المسارات التعليمية المنضم لها')
            }
        
        return Response(response_data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': _('تم تحديث الملف الشخصي بنجاح'),
            'user': serializer.data
        })


class ProfileAvatarDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user

        if user.profile_picture:
            user.profile_picture.delete(save=False)
            user.profile_picture = None
            user.save()

        serializer = ProfileSerializer(user, context={'request': request})

        return Response({
            'message': _('تم حذف الصورة الشخصية بنجاح'),
            'user': serializer.data,
        })


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': _('تم تغيير كلمة المرور بنجاح'),
        })
    

class SubmitQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if not user.is_learner:
            return Response({
                'error': 'only learner can take a quiz'
            }, status=403)

        level = request.data.get('level')

        if level not in ['beginner', 'intermediate', 'advanced']:
            return Response({
                'error': 'Unknown level'
            }, status=400)

        user.level = level
        user.is_rated = True
        user.save()

        return Response({
            'message': 'Quiz saved',
            'level': user.level
        })