from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Person


def person_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    people = Person.objects.all().order_by("id")
    if query:
        filters = Q(name__icontains=query)
        if query.isdigit():
            filters |= Q(age=int(query))
        people = people.filter(filters)
    context = {"people": people, "query": query}
    return render(request, "people/person_list.html", context)


def person_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        age = request.POST.get("age", "").strip()
        dob_str = request.POST.get("date_of_birth", "").strip()
        errors = {}
        if not name:
            errors["name"] = "Name is required"
        try:
            age_val = int(age)
            if age_val < 0:
                raise ValueError
        except ValueError:
            errors["age"] = "Age must be a non-negative integer"
        from datetime import datetime

        try:
            dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
        except ValueError:
            errors["date_of_birth"] = "Date must be in dd/mm/yyyy format"

        if not errors:
            Person.objects.create(name=name, age=age_val, date_of_birth=dob)
            return redirect(reverse("person_list"))
        return render(request, "people/person_form.html", {"errors": errors, "values": request.POST, "action": "Create"})
    return render(request, "people/person_form.html", {"errors": {}, "values": {}, "action": "Create"})


def person_update(request: HttpRequest, pk: int) -> HttpResponse:
    person = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        age = request.POST.get("age", "").strip()
        dob_str = request.POST.get("date_of_birth", "").strip()
        errors = {}
        if not name:
            errors["name"] = "Name is required"
        try:
            age_val = int(age)
            if age_val < 0:
                raise ValueError
        except ValueError:
            errors["age"] = "Age must be a non-negative integer"
        from datetime import datetime

        try:
            dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
        except ValueError:
            errors["date_of_birth"] = "Date must be in dd/mm/yyyy format"

        if not errors:
            person.name = name
            person.age = age_val
            person.date_of_birth = dob
            person.save()
            return redirect(reverse("person_list"))
        values = {"name": name, "age": age, "date_of_birth": dob_str}
        return render(request, "people/person_form.html", {"errors": errors, "values": values, "action": "Update"})
    values = {
        "name": person.name,
        "age": str(person.age),
        "date_of_birth": person.date_of_birth.strftime("%d/%m/%Y"),
    }
    return render(request, "people/person_form.html", {"errors": {}, "values": values, "action": "Update"})


def person_delete(request: HttpRequest, pk: int) -> HttpResponse:
    person = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        person.delete()
        return redirect(reverse("person_list"))
    return render(request, "people/person_confirm_delete.html", {"person": person})
