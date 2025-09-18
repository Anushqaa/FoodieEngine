from shared_functions import *

def calorie_checker():]
    print("🔥 FOOD CALORIE BUDGET CHECKER")
    print("=" * 35)
    
    food_items = load_food_data('FoodDataSet.json')
    collection = create_similarity_search_collection("calorie_checker")
    populate_similarity_collection(collection, food_items)
    print("✅ Food database loaded!")
    
    while True:
        try:
            budget = int(input("\n💪 What's your calorie budget per meal? "))
            if budget > 0:
                break
            else:
                print("Please enter a positive number!")
        except ValueError:
            print("Please enter a valid number!")
    
    print(f"\n🎯 Your calorie budget: {budget} calories")
    print("Now search for foods to see if they fit your budget!")
    

    while True:
        print("\n" + "-" * 40)
        search_term = input("🔍 Search for a food (or 'quit' to exit): ").strip()
        
        if search_term.lower() == 'quit':
            print("👋 Thanks for using the Calorie Checker!")
            break
        
        if not search_term:
            print("Please enter a food to search for!")
            continue
        
        budget_results = perform_filtered_similarity_search(
            collection, search_term, max_calories=budget, n_results=5
        )
        
        all_results = perform_similarity_search(collection, search_term, 5)
        
        print(f"\n📋 Results for '{search_term}':")
        
        if budget_results:
            print(f"✅ FITS YOUR BUDGET ({budget} cal limit):")
            for i, result in enumerate(budget_results, 1):
                calories = result['food_calories_per_serving']
                remaining = budget - calories
                print(f"  {i}. {result['food_name']}")
                print(f"     Calories: {calories} (🟢 {remaining} cal remaining)")
                print(f"     Cuisine: {result['cuisine_type']}")
        else:
            print(f"❌ No foods found within your {budget} calorie budget!")
        
        over_budget = []
        for result in all_results:
            if result['food_calories_per_serving'] > budget:
                over_budget.append(result)
        
        if over_budget:
            print(f"\n🚫 OVER BUDGET (but similar to your search):")
            for i, result in enumerate(over_budget[:3], 1):
                calories = result['food_calories_per_serving']
                excess = calories - budget
                print(f"  {i}. {result['food_name']}")
                print(f"     Calories: {calories} (🔴 {excess} cal over budget)")
        
        if budget_results:
            avg_calories = sum(r['food_calories_per_serving'] for r in budget_results) / len(budget_results)
            print(f"\n📊 Budget-friendly options average: {avg_calories:.0f} calories")


if __name__ == "__main__":
    calorie_checker()