from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest
from .models import TarefaModel
from tarefas.forms import TarefaForm

# Create your views here.
def tarefas_home(request):
    contexto = {
        "nome": "Juan",
        "tarefas": TarefaModel.objects.all()
    }
    return render(request, 'tarefas/home.html', contexto)

def tarefas_adicionar(request: HttpRequest):
    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            contexto = {
                "form": TarefaForm(),
                "mensagem": "Tarefa adicionada com sucesso!"
            }
            return redirect("tarefas:home")

    
    contexto = {
        "form": TarefaForm()
    }
    return render(request, 'tarefas/adicionar.html', contexto)


def tarefas_remover(request: HttpRequest, id):
    tarefa = get_object_or_404(TarefaModel, id=id)
    tarefa.delete()
    return redirect("tarefas:home")


def tarefas_editar(request: HttpRequest, id):
    tarefa = get_object_or_404(TarefaModel, id=id)
    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect("tarefas:home")
    form = TarefaForm(instance=tarefa)
    context = {
        "form": form
    }
    return render(request, 'tarefas/editar.html', context)

