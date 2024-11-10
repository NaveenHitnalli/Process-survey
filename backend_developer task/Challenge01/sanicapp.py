import json
import logging
from sanic import Sanic
from sanic.response import json as sanic_json
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

# Load JSON data
def load_test_data():
    try:
        with open('test_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("test_data.json file not found")
        return None
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in test_data.json")
        return None

# Database setup
DATABASE_URL = "sqlite:///survey_db.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SurveyResult(Base):
    __tablename__ = 'survey_results'
    user_id = Column(String, primary_key=True)
    overall_analysis = Column(String)
    cat_dog = Column(String)
    fur_value = Column(String)
    tail_value = Column(String)
    description = Column(String)

Base.metadata.create_all(engine)

app = Sanic("SurveyApp")

@app.post("/process-survey")
async def process_survey(request):
    try:
        # Use JSON data from file if no request data is provided
        if not request.json:
            data = load_test_data()
            if not data:
                return sanic_json({"error": "No data provided and couldn't load test data"}, status=400)
        else:
            data = request.json

        user_id = data["user_id"]
        survey_results = data["survey_results"]

        # Process results
        values = [result["question_value"] for result in survey_results]
        average = sum(values) / len(values)

        # Calculate results
        overall_analysis = "unsure" if values[0] == 7 and values[3] < 3 else "certain"
        cat_dog = "cats" if values[9] > 5 and values[8] <= 5 else "dogs"
        fur_value = "long" if average > 5 else "short"
        tail_value = "long" if values[6] > 4 else "short"
        description = f"Analysis for user {user_id}: Preference for {fur_value} fur and {tail_value} tail."

        # Save to database
        session = Session()
        try:
            survey_result = SurveyResult(
                user_id=user_id,
                overall_analysis=overall_analysis,
                cat_dog=cat_dog,
                fur_value=fur_value,
                tail_value=tail_value,
                description=description
            )
            session.add(survey_result)
            session.commit()
        except IntegrityError:
            session.rollback()
            logger.error(f"Database error for user_id: {user_id}")
            return sanic_json({"error": "Database error"}, status=500)
        finally:
            session.close()

        return sanic_json({
            "overall_analysis": overall_analysis,
            "cat_dog": cat_dog,
            "fur_value": fur_value,
            "tail_value": tail_value,
            "description": description
        })

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return sanic_json({"error": "Internal server error"}, status=500)

# Add a route to test with JSON file directly
@app.get("/test")
async def test_with_json(request):
    data = load_test_data()
    if not data:
        return sanic_json({"error": "Could not load test data"}, status=500)
    
    # Process the test data
    try:
        values = [result["question_value"] for result in data["survey_results"]]
        average = sum(values) / len(values)

        overall_analysis = "unsure" if values[0] == 7 and values[3] < 3 else "certain"
        cat_dog = "cats" if values[9] > 5 and values[8] <= 5 else "dogs"
        fur_value = "long" if average > 5 else "short"
        tail_value = "long" if values[6] > 4 else "short"
        description = f"Test analysis for user {data['user_id']}: Preference for {fur_value} fur and {tail_value} tail."

        return sanic_json({
            "test_data": "success",
            "overall_analysis": overall_analysis,
            "cat_dog": cat_dog,
            "fur_value": fur_value,
            "tail_value": tail_value,
            "description": description
        })
    except Exception as e:
        logger.error(f"Error processing test data: {str(e)}")
        return sanic_json({"error": "Error processing test data"}, status=500)

@app.get("/")
async def home(request):
    return sanic_json({"message": "Survey API is running"})

if __name__ == "__main__":
    # Load test data on startup
    test_data = load_test_data()
    if test_data:
        logger.info("Test data loaded successfully")
    else:
        logger.warning("Failed to load test data")
    
    app.run(host="localhost", port=8000, debug=True)
