from schemas import SubstituteRequest, SubstituteOption, SubstituteAttributes
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Mock substitution database
SUBSTITUTION_DB = {
    "butter": {
        "vegan": [
            {
                "name": "Coconut Oil",
                "reason": "Vegan alternative that provides similar fat content and moisture.",
                "attributes": {
                    "flavor_profile": "mild coconut flavor",
                    "texture": "solid at room temperature",
                    "nutritional_info": {"calories": "120 kcal", "fat": "14g"},
                },
            },
            {
                "name": "Olive Oil",
                "reason": "Vegan substitute that adds healthy fats and a subtle flavor.",
                "attributes": {
                    "flavor_profile": "fruity and robust",
                    "texture": "liquid at room temperature",
                    "nutritional_info": {"calories": "119 kcal", "fat": "13.5g"},
                },
            },
        ],
        "standard": [
            {
                "name": "Margarine",
                "reason": "Non-vegan alternative with similar fat content.",
                "attributes": {
                    "flavor_profile": "buttery",
                    "texture": "solid at room temperature",
                    "nutritional_info": {"calories": "100 kcal", "fat": "11g"},
                },
            },
            {
                "name": "Applesauce",
                "reason": "Adds moisture and reduces fat content.",
                "attributes": {
                    "flavor_profile": "mild sweetness",
                    "texture": "moisture-enhancing",
                    "nutritional_info": {"calories": "50 kcal", "fat": "0g"},
                },
            },
        ],
    },
    "eggs": {
        "vegan": [
            {
                "name": "Flaxseed Meal",
                "reason": "Vegan substitute that binds ingredients similarly to eggs.",
                "attributes": {
                    "flavor_profile": "nutty",
                    "texture": "gel-like when mixed with water",
                    "nutritional_info": {
                        "calories": "55 kcal per 1 tablespoon",
                        "fat": "4g",
                    },
                },
            },
            {
                "name": "Chia Seeds",
                "reason": "Vegan alternative that provides binding properties.",
                "attributes": {
                    "flavor_profile": "mild",
                    "texture": "gel-like when mixed with water",
                    "nutritional_info": {
                        "calories": "60 kcal per 1 tablespoon",
                        "fat": "4g",
                    },
                },
            },
        ],
        "standard": [
            {
                "name": "Applesauce",
                "reason": "Adds moisture and acts as a binding agent.",
                "attributes": {
                    "flavor_profile": "mild sweetness",
                    "texture": "moisture-enhancing",
                    "nutritional_info": {
                        "calories": "50 kcal per 1/4 cup",
                        "fat": "0g",
                    },
                },
            },
            {
                "name": "Silken Tofu",
                "reason": "Provides moisture and structure similar to eggs.",
                "attributes": {
                    "flavor_profile": "neutral",
                    "texture": "smooth and creamy",
                    "nutritional_info": {
                        "calories": "55 kcal per 1/4 cup",
                        "fat": "3g",
                    },
                },
            },
        ],
    },
    # Add more ingredients as needed
}


def get_substitutions(request: SubstituteRequest) -> List[SubstituteOption]:
    original = request.original_ingredient.lower()
    substitutions = []

    # Determine dietary context
    dietary = (
        [diet.lower() for diet in request.dietary_restrictions]
        if request.dietary_restrictions
        else []
    )

    # Fetch substitution options based on dietary restrictions
    if original in SUBSTITUTION_DB:
        if dietary:
            for diet in dietary:
                if diet in SUBSTITUTION_DB[original]:
                    for option in SUBSTITUTION_DB[original][diet]:
                        substitution = SubstituteOption(
                            name=option["name"],
                            reason=option["reason"],
                            attributes=SubstituteAttributes(**option["attributes"]),
                        )
                        substitutions.append(substitution)
        # Add standard substitutions
        if "standard" in SUBSTITUTION_DB[original]:
            for option in SUBSTITUTION_DB[original]["standard"]:
                substitution = SubstituteOption(
                    name=option["name"],
                    reason=option["reason"],
                    attributes=SubstituteAttributes(**option["attributes"]),
                )
                substitutions.append(substitution)

        # Prioritize available ingredients
        if request.available_ingredients:
            available = [ing.lower() for ing in request.available_ingredients]
            substitutions = sorted(
                substitutions, key=lambda x: 0 if x.name.lower() in available else 1
            )
    else:
        logger.warning(f"No substitution data found for ingredient: {original}")

    return substitutions
