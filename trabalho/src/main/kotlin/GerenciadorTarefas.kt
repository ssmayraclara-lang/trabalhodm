import java.time.LocalDateTime

class GerenciadorTarefas {

    private var tarefas = mutableListOf<Tarefa>()
    private var contadorId = 1

    fun adicionarTarefa(titulo: String, descricao: String, dataHora: LocalDateTime, prioridade: Int, categoria: String) {
        val tarefa = Tarefa(contadorId++, titulo, descricao, dataHora, false, prioridade, categoria)
        tarefas.add(tarefa)
    }

    fun removerTarefa(id: Int) {
        tarefas.removeIf { it.id == id }
    }

    fun editarTarefa(id: Int, titulo: String, descricao: String, dataHora: LocalDateTime, prioridade: Int, categoria: String) {
        val tarefa = tarefas.find { it.id == id }
        if (tarefa != null) {
            tarefa.titulo = titulo
            tarefa.descricao = descricao
            tarefa.dataHora = dataHora
            tarefa.prioridade = prioridade
            tarefa.categoria = categoria
        }
    }

    fun obterTarefasDoDia(data: LocalDateTime): List<Tarefa> {
        return tarefas.filter { it.dataHora.toLocalDate() == data.toLocalDate() }
    }

    fun obterTarefasDaSemana(): List<Tarefa> {
        val agora = LocalDateTime.now()
        return tarefas.filter {
            it.dataHora.toLocalDate().isAfter(agora.toLocalDate().minusDays(1)) &&
                    it.dataHora.toLocalDate().isBefore(agora.toLocalDate().plusDays(7))
        }
    }

    fun obterTarefasAtrasadas(): List<Tarefa> {
        val agora = LocalDateTime.now()
        return tarefas.filter { it.dataHora.isBefore(agora) && !it.concluida }
    }

    fun marcarComoConcluida(id: Int) {
        val tarefa = tarefas.find { it.id == id }
        tarefa?.concluida = true
    }

    fun obterTodasTarefas(): MutableList<Tarefa> {
        return tarefas
    }
}