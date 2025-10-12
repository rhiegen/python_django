from django import forms

from tarefas.models import TarefaModel

class TarefaForm(forms.ModelForm):
    class Meta:
        model = TarefaModel
        fields = ['nome', 'descricao', 'concluida']