from django.db import models

# Create your models here.
class TarefaModel(models
                  .Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    concluida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nome