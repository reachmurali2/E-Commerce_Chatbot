# 🔡 1. Import Required Modules
from semantic_router import Route                                           # Represents a class for defining a route (FAQ/SQL) with sample utterances.
from semantic_router.routers import SemanticRouter                          # Main router that uses vector similarity to pick a route
from semantic_router.encoders import HuggingFaceEncoder                     # Used for generating sentence embeddings from Huggingface Transformer models

# 🔤 2. Create an Embedding Model (Encoder)
encoder = HuggingFaceEncoder(
    name = 'sentence-transformers/all-MiniLM-L6-v2'                        # name => Chooses the model for semantic similarity :: all-MiniLM-L6-v2 => A fast and light-weight model good for semantic search or sentence similarity tasks.     
)

# 🛣️ 3. Define Routes with Sample Utterances 
faq = Route(                                                       
    name="faq",                                                            # name: Logical label of the route.
    utterances=[                                                           # utterances: Typical examples to teach the model what belongs to this category.
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "How long does it take to process a refund?",
        "Are there any ongoing sales or promotions?",
        "Can I cancel or modify my order after placing it?",
        "Do you offer international shipping?",
        "What are the modes of refund available after cancellation?",
        "Can I ask the delivery agent to reschedule the pickup date?",
        "How quickly can I get my order delivered?",

    ]
)

sql = Route(
    name="sql",
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)

# Create the route for small-talk and added it in the route layer
small_talk = Route(
    name='small-talk',
    utterances=[
        "How are you?",
        "What is your name?",
        "Are you a robot?",
        "What are you?",
        "What do you do?",
    ]
)

# 🔁 4. Combine All Routes
routes = [faq,sql, small_talk]

# 🧭 5. Create the Router
router = SemanticRouter(encoder=encoder, routes=routes, auto_sync="local")     # encoder             => Uses HuggingFace embeddings for similarity.
                                                                               # routes              => Contains the list of defined routes.
                                                                               # auto_sync = "local" => Enables quick local storage of embedding cache for performance.

# 🧪 6. Testing the Router  
if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)     # Detects faq 
    print(router("Pink Puma shoes in price range 5000 to 10000").name)  # Detects sql 
    print(router("Are you a robot?").name)                              # Detects small_talk 

    # Can be imporoved by using the below additional code   
    # router("query", threshold = 0.7)                                       # threshold: Minimum cosine similarity required to select a route.
    # result = router("query")                               
    # print(result.name, result.score)                                       # result.name => Selected route name. 
                                                                             # result.score: Confidence score of the match.
    '''
   ----------------------------
   Code Bock - Explanation
   ----------------------------     


    ✅ faq Route:
    Used for common support queries like:
    Return policy
    Tracking orders
    Cancellations

    ✅ sql Route:
    Used for queries that require fetching structured data from a database like:
    Discounts
    Product filtering
    Brand-specific queries
    
    
    '''