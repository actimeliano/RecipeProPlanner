import streamlit as st
import pandas as pd
from database import RecipeDatabase
from planner import DinnerPlanner
from utils import recipe_to_dict, dict_to_recipe

# Initialize the database and planner
db = RecipeDatabase()
planner = DinnerPlanner()

def main():
    st.title("Recipe Database and Dinner Planner")

    menu = ["View Recipes", "Add Recipe", "Plan Dinners", "Generate Shopping List", "Export Calendar"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View Recipes":
        view_recipes()
    elif choice == "Add Recipe":
        add_recipe()
    elif choice == "Plan Dinners":
        plan_dinners()
    elif choice == "Generate Shopping List":
        generate_shopping_list()
    elif choice == "Export Calendar":
        export_calendar()

def view_recipes():
    st.header("Recipe Database")
    
    # Search functionality
    search_term = st.text_input("Search recipes:")
    category = st.selectbox("Filter by category:", ["All", "Main Dish", "Dessert", "Drink", "Side Dish"])
    
    recipes = db.search_recipes(search_term, category)
    
    if recipes:
        for recipe in recipes:
            st.subheader(recipe.name)
            st.write(f"Category: {recipe.category}")
            st.write(f"Ingredients: {', '.join(recipe.ingredients)}")
            st.write(f"Instructions: {recipe.instructions}")
            st.write("---")
    else:
        st.write("No recipes found.")

def add_recipe():
    st.header("Add New Recipe")
    
    name = st.text_input("Recipe Name:")
    category = st.selectbox("Category:", ["Main Dish", "Dessert", "Drink", "Side Dish"])
    ingredients = st.text_area("Ingredients (one per line):")
    instructions = st.text_area("Instructions:")
    
    if st.button("Add Recipe"):
        ingredients_list = [ing.strip() for ing in ingredients.split("\n") if ing.strip()]
        new_recipe = dict_to_recipe({
            "name": name,
            "category": category,
            "ingredients": ingredients_list,
            "instructions": instructions
        })
        db.add_recipe(new_recipe)
        st.success("Recipe added successfully!")

def plan_dinners():
    st.header("Plan Your Dinners")
    
    # Get all recipes for the dropdown
    all_recipes = db.get_all_recipes()
    recipe_names = [recipe.name for recipe in all_recipes]
    
    # Create a date range for the next 7 days
    dates = pd.date_range(start=pd.Timestamp.now().date(), periods=7)
    
    # Create a dictionary to store the dinner plan
    dinner_plan = {}
    
    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        selected_recipe = st.selectbox(f"Dinner for {date_str}", [""] + recipe_names, key=date_str)
        if selected_recipe:
            dinner_plan[date_str] = selected_recipe
    
    if st.button("Save Dinner Plan"):
        planner.save_dinner_plan(dinner_plan)
        st.success("Dinner plan saved successfully!")

def generate_shopping_list():
    st.header("Generate Shopping List")
    
    # Get the current dinner plan
    dinner_plan = planner.get_dinner_plan()
    
    if dinner_plan.empty:
        st.warning("No dinner plan found. Please plan your dinners first.")
        return
    
    # Get all recipes
    all_recipes = db.get_all_recipes()
    recipe_dict = {recipe.name: recipe for recipe in all_recipes}
    
    # Generate shopping list
    shopping_list = {}
    for _, row in dinner_plan.iterrows():
        recipe = recipe_dict.get(row['recipe'])
        if recipe:
            for ingredient in recipe.ingredients:
                if ingredient in shopping_list:
                    shopping_list[ingredient] += 1
                else:
                    shopping_list[ingredient] = 1
    
    # Display shopping list
    st.subheader("Your Shopping List:")
    for item, count in shopping_list.items():
        st.write(f"- {item} (x{count})")
    
    # Option to download as text file
    if st.button("Download Shopping List"):
        shopping_list_text = "\n".join([f"{item} (x{count})" for item, count in shopping_list.items()])
        st.download_button(
            label="Download as Text",
            data=shopping_list_text,
            file_name="shopping_list.txt",
            mime="text/plain"
        )

def export_calendar():
    st.header("Export Dinner Plan to Calendar")
    
    if st.button("Generate Calendar File"):
        calendar_file = planner.export_to_calendar()
        st.download_button(
            label="Download Calendar File",
            data=calendar_file,
            file_name="dinner_plan.ics",
            mime="text/calendar"
        )

if __name__ == "__main__":
    main()
