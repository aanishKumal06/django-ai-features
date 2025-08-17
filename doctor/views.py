from django.shortcuts import render
from django.core.paginator import Paginator
from .models import  Doctor
from .schemas import DoctorSchema
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

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


def ai_specialty_search(query: str) -> str | None:
    # When we want to get the specialties in array.
    available_specialties = list(Doctor.objects.values_list("specialty", flat=True).distinct())
    print(f"Available specialties: {available_specialties}")


    prompt = f"""
    You are an AI assistant that helps users find relevant doctors based on their needs.
    The user described their condition or concern like this: "{query}".
    Based on that, suggest the most relevant medical specialty from the list below:
    {available_specialties}
    """

    structured_llm = llm.with_structured_output(DoctorSchema)
    response = structured_llm.invoke(prompt)
    print(f"AI response: {response}")
    return response.name  # type: ignore

def doctor_list(request):
    query = request.GET.get("query", "")
    if query:
        specialty = ai_specialty_search(query)
        print(f"AI suggested specialty: {specialty}")
        if specialty:
            doctors = Doctor.objects.filter(specialty__icontains=specialty).order_by('id')
    else:
        doctors = Doctor.objects.all().order_by('id') 

    page_number = request.GET.get("page", 1)
    paginator = Paginator(doctors, 5) 
    page_obj = paginator.get_page(page_number)

    context = {
        "doctors": page_obj,
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    }   
    return render(request, "doctor/index.html", context)




