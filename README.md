# HistoriScrape FastAPI Project
# SubstituteChef API

SubstituteChef is an API designed to provide intelligent ingredient substitution suggestions based on recipe context and dietary restrictions. It assists developers and businesses in building cooking applications, recipe websites, and personal assistants by offering smart, context-aware alternatives to unavailable or restricted ingredients.

## Features

- **Contextual Substitutions:** Suggests substitutes that fit seamlessly into your recipe based on existing ingredients.
- **Dietary Customization:** Supports various dietary restrictions such as vegan, gluten-free, and more.
- **Pantry Integration:** Offers substitutions based on the ingredients you already have at home.
- **Multiple Suggestions:** Provides a ranked list of alternatives to choose from.
- **Developer-Friendly:** Single, lightweight endpoint for easy integration.

## Getting Started

### Prerequisites

- Python 3.8+
- Redis Server (optional, for caching and rate limiting)


API Name & Tagline
Name: SubstituteChef API
Tagline: "Smart Ingredient Substitutions for Every Kitchen"
2. Target Problem
Identified Problem:
Cooking enthusiasts, home cooks, and professional chefs often encounter situations where specific ingredients required by a recipe are unavailable. Additionally, dietary restrictions such as allergies, veganism, or gluten intolerance necessitate suitable ingredient substitutions without compromising the dish's flavor, texture, or nutritional value.

Why Existing Solutions Fall Short:
Generic Substitutions: Most available substitution lists are generic and do not consider the specific context of a recipe, leading to suboptimal results.
Lack of Context Awareness: Existing tools fail to analyze the recipe's overall composition, which is crucial for maintaining the dish's integrity when substituting ingredients.
Limited Dietary Integration: Few solutions offer comprehensive support for various dietary restrictions, making it challenging for users with specific needs to find appropriate substitutes.
Developer Accessibility: There is a scarcity of developer-friendly APIs that can be easily integrated into cooking apps, websites, or personal assistants to provide real-time substitution suggestions.
3. Innovation Potential
SubstituteChef API stands out by offering intelligent, context-aware ingredient substitutions tailored to individual recipes and dietary requirements. Unlike generic substitution tools, SubstituteChef leverages machine learning to understand the nuances of each recipe, ensuring that substitutes maintain the dish's desired flavor profile, texture, and nutritional content.

Unique and Powerful Aspects:
Contextual Analysis: Considers other ingredients in the recipe to suggest the most compatible substitutes.
Dietary Customization: Supports various dietary restrictions, providing alternatives that align with user-specific needs (e.g., vegan, gluten-free, nut-free).
Pantry Integration: Allows users to input available ingredients, enabling the API to suggest substitutions based on what they already have.
Multiple Suggestions: Provides a ranked list of substitution options, offering users flexibility in their choices.
Developer-Friendly: Single, lightweight endpoint designed for easy integration into diverse applications.
4. API Endpoint
Single Endpoint Design
/substitute

Method: POST
Description: Provides intelligent ingredient substitution suggestions based on the recipe context and dietary requirements.
Input:

json
Copy code
{
    "original_ingredient": "butter",
    "recipe_context": ["flour", "sugar", "eggs", "milk"],
    "dietary_restrictions": ["vegan"],
    "available_ingredients": ["coconut oil", "applesauce"]
}
Output:

json
Copy code
{
    "status": "success",
    "substitutions": [
        {
            "name": "Coconut Oil",
            "reason": "Vegan alternative that provides similar fat content and moisture.",
            "attributes": {
                "flavor_profile": "mild coconut flavor",
                "texture": "solid at room temperature",
                "nutritional_info": {
                    "calories": 120,
                    "fat": "14g"
                }
            }
        },
        {
            "name": "Applesauce",
            "reason": "Vegan substitute that adds moisture and reduces fat.",
            "attributes": {
                "flavor_profile": "mild sweetness",
                "texture": "moisture-enhancing",
                "nutritional_info": {
                    "calories": 50,
                    "fat": "0g"
                }
            }
        }
    ]
}
Error Handling:

400 Bad Request: Missing required fields or invalid input formats.
404 Not Found: No suitable substitutions found for the given ingredient and context.
500 Internal Server Error: Unexpected server-side errors.
5. Code Logic
Below is a complete Python implementation of the SubstituteChef API using FastAPI. This implementation includes intelligent substitution logic, dietary restriction handling, and robust error handling.

Prerequisites
Python 3.8+
FastAPI
Uvicorn
Pydantic
Numpy (for potential future enhancements)
Redis (optional, for caching)
Directory Structure
css
Copy code
substitutechef/
├── main.py
├── models.py
├── schemas.py
├── services/
│   └── substitution_service.py
├── utils/
│   ├── cache.py
│   └── rate_limiter.py
├── requirements.txt
└── README.md
main.py


### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/substitutechef.git
   cd substitutechef
