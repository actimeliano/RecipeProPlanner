from database import Recipe

def recipe_to_dict(recipe: Recipe) -> dict:
    return {
        "id": recipe.id,
        "name": recipe.name,
        "category": recipe.category,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions
    }

def dict_to_recipe(recipe_dict: dict) -> Recipe:
    return Recipe(
        id=recipe_dict.get("id"),
        name=recipe_dict["name"],
        category=recipe_dict["category"],
        ingredients=recipe_dict["ingredients"],
        instructions=recipe_dict["instructions"]
    )
