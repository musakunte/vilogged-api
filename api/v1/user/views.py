from rest_framework import serializers, generics, mixins, views, status, permissions
from django.core import serializers as dj_serializer
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from utility.utility import Utility, PaginationBuilder
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from vilogged.config_manager import ConfigManager
from vilogged.ldap import LDAPManager
from vilogged.department.models import Department
from vilogged.users.models import UserProfile
from api.v1.department.views import DepartmentSerializer

model = UserProfile

FILTER_FIELDS = [
    '_id',
    '_rev',
    'username',
    'email',
    'phone',
    'work_phone',
    'home_phone',
    'image',
    'department__name',
    'department',
    'gender',
    'first_name',
    'last_name',
    'is_active',
    'is_staff',
    'date_joined'
]
SEARCH_FIELDS = [
    'username',
    'email',
    'phone',
    'work_phone',
    'home_phone',
    'image',
    'department__name',
    'gender',
    'first_name',
    'last_name',
]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = (
            '_id',
            '_rev',
            'username',
            'email',
            'phone',
            'work_phone',
            'home_phone',
            'image',
            'department',
            'gender',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'designation',
            'image',
            'last_login',
            'date_joined',
            'password'
        )

        write_only_fields = ('password',)

model_serializer = UserSerializer


class UserList(views.APIView):

    def get(self, request, **kwargs):
        model_data = PaginationBuilder().get_paged_data(model, request, FILTER_FIELDS, SEARCH_FIELDS, '-date_joined')

        row_list = []
        for obj in model_data['model_list']:
            row_list.append(obj.to_json())
        return Response({
            'count': model_data['count'],
            'results': row_list,
            'next': model_data['next'],
            'prev': model_data['prev']
        })


class UserDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = '_id'

    def post_or_put(self, request, *args, **kwargs):
        request.data['_id'] = self.kwargs['_id']
        request.data['department'] = Utility.return_id(Department, request.data.get('department'), 'name')
        try:
            user_instance = UserProfile.objects.get(_id=self.kwargs['_id'])
            if request.data.get('password', None) is None or request.data.get('password', None) != '':
                request.data['password'] = user_instance.password
            elif request.data.get('password', None) is not None and request.data.get('password', None) != '':
                request.data['password'] = make_password(request.data['password'])
            return self.update(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            if request.data.get('password', None) is not None and request.data.get('password', None) != '':
                request.data['password'] = make_password(request.data['password'])
            return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = Utility.get_data_or_none(UserProfile, request, **kwargs)
        if user is None:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(user.to_json())

    def put(self, request, *args, **kwargs):
        return self.post_or_put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.post_or_put(request, *args, **kwargs)


class AuthUser(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        config = ConfigManager().get_config()
        user = None
        print ('here')
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if config.get('authType', 'api') == 'api':
            user = authenticate(username=username, password=password)

        if config.get('authType', 'api') == 'ldap':
            user = LDAPManager().ldap_login(username, password)

        if user is not None:
            if user.is_active:
                token = Token.objects.get(user=user)
                data = user.to_json(True)
                del data['password']
                return Response({'user': data, 'token': token.key})
            else:
                return Response({'detail': 'User not active'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'invalid credentials provided'}, status=status.HTTP_401_UNAUTHORIZED)

