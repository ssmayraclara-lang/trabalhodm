import java.time.LocalDateTime

data class Tarefa(
    var id: Int,
    var titulo: String,
    var descricao: String,
    var dataHora: LocalDateTime,
    var concluida: Boolean = false,
    var prioridade: Int,
    var categoria: String
)