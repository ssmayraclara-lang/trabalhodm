class Usuario(
    var nome: String,
    var tarefas: MutableList<Tarefa> = mutableListOf()
)