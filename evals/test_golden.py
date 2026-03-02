from conftest import get_review, judge_with_golden

GOLDEN_EXAMPLES = [
    {"q": "What does Haley love?", "ref": "Haley loves Coconuts, Fruit Salad, Pink Cake, and Sunflowers."},
    {"q": "What does Penny hate?", "ref": "Penny hates Rabbit's Foot, Algae Soup, Pale Broth, and all Alcoholic beverages."},
    {"q": "How many points is one heart?", "ref": "One heart represents 250 friendship points."},
    {"q": "What happens at 8 hearts with a marriage candidate?", "ref": "Their friendship meter stops decaying and you can give them a Bouquet to date them."},
    {"q": "How many points do you get for talking to a villager daily?", "ref": "Talking to a villager gives +20 friendship points per day."},
    {"q": "What is the universal love?", "ref": "Prismatic Shard, Rabbit's Foot, Pearl, Magic Rock Candy, and Golden Pumpkin are universal loves (with rare exceptions like Penny hating Rabbit's Foot)."},
    {"q": "Can I give more than two gifts a week?", "ref": "No, the limit is two gifts per week per villager, except for their birthday, which allows a third gift."},
    {"q": "What happens if I give a hated gift?", "ref": "A hated gift deducts 40 friendship points."},
    {"q": "Where does Sebastian's 2-heart event take place?", "ref": "It takes place in Sebastian's room when he is there."},
    {"q": "Do festivals give friendship points?", "ref": "Yes, completing tasks like the Luau soup or Secret Winter Star gives significant friendship point boosts."}
]

def test_golden_examples():
    for case in GOLDEN_EXAMPLES:
        response = get_review(case["q"])
        rating = judge_with_golden(case["q"], case["ref"], response)
        assert rating >= 6, f"Failed '{case['q']}' with rating {rating}.\nExpected: {case['ref']}\nBot Said: {response}"