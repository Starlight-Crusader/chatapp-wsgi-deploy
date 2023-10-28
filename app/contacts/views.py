from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters, generics, response, status

from users.models import User
from users.serializers import UserSerializer
from .serializers import AddRemoveContactSerializer


class GetContactsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        return user.contacts.all()


class SearchContactsListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nickname']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_contact(request):
    serializer = AddRemoveContactSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.get(id=request.user.id)
    contact_user = None

    try:
        contact_user = User.objects.get(nickname=serializer.data['contact_nickname'])
    except:
        return response.Response(
            {'message': 'User to add not found!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.contacts.add(contact_user)
    
    return response.Response(
        {'message': 'Contact successfully added!'},
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_contact(request):
    serializer = AddRemoveContactSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.get(id=request.user.id)
    contact_user = None

    try:
        contact_user = User.objects.get(nickname=serializer.data['contact_nickname'])
    except:
        return response.Response(
            {'message': 'Contact not found!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.contacts.remove(contact_user)

    return response.Response(
        {'message': 'Contact succsessfully removed!'},
        status=status.HTTP_200_OK
    )
