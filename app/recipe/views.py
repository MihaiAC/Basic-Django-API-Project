"""Views for the recipe APIs."""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing Recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # We need to retrieve the Recipes only for the current user.
    def get_queryset(self):
        """Retrieve recipes for authenticated users."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    # If the action is list, return RecipeSerializer.
    def get_serializer_class(self):
        """Return the serializer class based on the type of request."""
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """When creating a new recipe, assign the request user."""
        serializer.save(user=self.request.user)


class TagViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """View for managing tags."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve only the tags corresponding to the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for managing ingredients."""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve only the ingredients corresponding to the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")
