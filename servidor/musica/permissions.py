from rest_framework import permissions


# Adaptdado de la doc (https://www.django-rest-framework.org/api-guide/permissions/#examples)
class IsOwnerOrIsAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has a `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        #Tambien lo permitimos si es el admin
        print(obj.user, request.user) # TODO: borrar
        return obj.user.pk == request.user.pk or request.user.is_staff
