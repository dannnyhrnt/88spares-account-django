from rest_framework import permissions

class HasAccess(permissions.BasePermission):
	def has_permission(self, request, view):
		return view.action == 'retrieve' or request.user.is_staff

	def has_object_permission(self, request, view, obj):
		return request.user.is_staff