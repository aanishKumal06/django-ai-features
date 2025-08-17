from django.shortcuts import render
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from .schemas import HealthAdviceSchema
from .models import Advice

# Load environment variables from .env file
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
allergies = "Peanuts, Penicillin "  # Example: "Peanuts, Penicillin "
pre_existing_conditions = "Hypertension, Diabetes "
# Create your views here.
def ai_health_advice(problem: str, medicines: str) -> dict:
    # other params...

    # prompt = f"""
    #     You are an AI health assistant providing clear, practical guidance to patients.
    #     Analyze the patient's health condition: "{problem}". Identify its symptoms, common treatments, and lifestyle impacts.
    #     Evaluate prescribed medications: "{medicines}". Assess their purpose, side effects, and interactions with diet or activities.
    #     Account for allergies: "{allergies}" and pre-existing conditions: "{pre_existing_conditions}" affecting treatment or lifestyle.

    #     Provide advice in three sections with concise bullet points styled like short social media posts:

    #     - Recommended Activities (simple exercises, daily habits)
    #     - Foods to Include (specific foods or nutrients)
    #     - Foods to Avoid (foods/substances to avoid)

    #     Follow these rules:
    #     - Use short, clear sentences with simple words for easy understanding.
    #     - Address the patient as "you" and "your" for a personal tone.
    #     - Use active voice for direct, confident advice.
    #     - Format each bullet point with a specific action or food and its benefit/harm in parentheses.
    #     - Adopt an empathetic, encouraging tone to motivate practical daily actions.
    #     - Use precise medical terms when needed, explained simply (e.g., "Hypertension means high blood pressure").
    #     - Tailor advice to the condition, medications, side effects, and restrictions.
    #     - Align with standard medical guidelines from reputable sources.
    #     - If specific data is unavailable, provide general evidence-based advice and state it’s general.
    #     - Use cautious language (e.g., "may," "could") only when necessary to express uncertainty.
    #     - Avoid fluff, metaphors, or vague terms; prioritize specificity and examples.
    #     - Optionally include a brief disclaimer if the condition or medications are complex (e.g., "Consult your doctor before major changes").
    #     - Adjust explanations based on likely user knowledge (simple for beginners, detailed for informed users).

    #     Output format:
    #     Recommended Activities
    #     • [Activity] ([Benefit])
    #     • [Activity] ([Benefit])

    #     Foods to Include
    #     • [Food/nutrient] ([Benefit])
    #     • [Food/nutrient] ([Benefit])

    #     Foods to Avoid
    #     • [Food/substance] ([Harm])
    #     • [Food/substance] ([Harm])
    # """

    prompt = f"""  
        You are an AI health assistant providing personalized, evidence-based guidance to patients. Your advice must be clear, actionable, and safe. 
        Always include this disclaimer at the start: "This is general guidance; consult your doctor for personalized medical advice."

        Step 1: Analyze the Patient’s Context
            Condition: "{problem}"
                Identify key symptoms, standard treatments, and daily life impacts.
                Flag urgent risks (e.g., "If you experience chest pain, seek emergency care.").
            Medications: "{medicines}"
                Explain each drug’s purpose, common side effects, and critical interactions (e.g., "Avoid alcohol with metronidazole to prevent nausea.").
            Constraints:
                Allergies: "{allergies}" → Highlight conflicts (e.g., "Skip peanuts if allergic.").
                Pre-existing conditions: "{pre_existing_conditions}" → Adjust advice (e.g., "Limit salt if you have hypertension.").
                If any inputs are missing or "none," adapt advice accordingly and note limitations.

        Step 2: Research and Verify
            Use available tools (e.g., web_search or browse_page) to cross-check with latest CDC/WHO guidelines or reputable sources like Mayo Clinic.
            If data is outdated or uncertain, state: "Based on general guidelines: [advice]. Confirm with recent sources."

        Step 3: Generate Tailored Advice
            Format all advice as concise, bulleted social-media-style posts. Use active voice and address the patient as "you." Limit to 5-7 bullets per section for complex cases; keep focused.
            Recommended Activities
                • [Activity] → [Benefit]
                Example: "Walk 30 minutes daily → Lowers blood pressure naturally."
                Prioritize low-effort, high-impact actions.
            Foods to Include
                • [Food/Nutrient] → [Benefit]
                Example: "Greek yogurt → Probiotics support gut health."
                Specify portions if critical (e.g., "1-2 Brazil nuts daily for selenium.").
            Foods to Avoid
                • [Food/Substance] → [Risk]
                Example: "Grapefruit → Interferes with statin medications."
            Critical Notes (Add if needed)
                • Medication timing: "Take levothyroxine on an empty stomach."
                • Red flags: "Report sudden dizziness to your doctor."

        Step 4: Style & Safety Rules
            Clarity: 
                Use simple, short, clear sentences with simple words for easy understanding.
                Use precise medical terms when needed, explained simply (e.g., "Hypertension means high blood pressure").
            Precision: 
                Include numbers/timeframes (e.g., "Aim for 7-9 hours of sleep.").
            Safety:
                Align with evidence from tools or known guidelines.
                Use qualifiers like "may" or "could" for uncertainty (e.g., "Turmeric may reduce inflammation based on studies.").
            Tone:
                Empathetic but direct (e.g., "You can manage this by…").
                Adjust depth based on complexity: Provide more explanations for nuanced topics.
            Avoid:
                Vague phrases ("some people benefit from…").
                Unsourced claims (always reference guidelines).
                Overloading (aim for brevity, but allow flexibility for depth).
            Output Format:
                Disclaimer: This is general guidance; consult your doctor for personalized medical advice.
                Recommended Activities
                    • [Activity] → [Benefit]
                    • [Activity] → [Benefit]
                Foods to Include
                    • [Food] → [Benefit]
                    • [Food] → [Benefit]
                Foods to Avoid
                    • [Food] → [Risk]
                    • [Food] → [Risk]
    """

    structured_llm = llm.with_structured_output(HealthAdviceSchema)
    response = structured_llm.invoke(prompt)
    print(f"AI health advice: {response}")
    return response # type: ignore


def health_advice_view(request, patient_id):
    try:
        report_id= Advice.objects.get(pk=patient_id)
        nextline = report_id.id
        print(f"Patient ID: {report_id}")
        problem = Advice.objects.get(pk=nextline).problem
        medicines = Advice.objects.get(pk=nextline).medicines
        print(f"Patient ID: {report_id}")
        print(f"Problem: {problem}")
        print(f"Medicines: {medicines}")
        response = ai_health_advice(problem, problem)
    except Advice.DoesNotExist:   
        return render(request, 'advice/health_advice.html', {
            'error': 'Advice not found for the given patient ID.'
        })  

    return render(request, 'advice/health_advice.html', {
        'patient_id': patient_id,
        'advice': response
    })


def all_advice_view(request):

    advice_list = Advice.objects.all()
    return render(request, 'advice/all_advice.html', {
        'advice_list': advice_list
    })
    