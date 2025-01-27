"""Views for the recipe APIs."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing Recipe APIs."""

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # We need to retrieve the Recipes only for the current user.
    def get_queryset(self):
        """Retrieve recipes for authenticated users."""
        return self.queryset.filter(user=self.request.user).order_by("-id")
