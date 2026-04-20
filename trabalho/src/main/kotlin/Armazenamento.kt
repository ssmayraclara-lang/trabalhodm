import java.io.File
import java.time.LocalDateTime

class Armazenamento {

    private val arquivo = File("tarefas.txt")

    fun salvar(tarefas: List<Tarefa>) {
        val conteudo = tarefas.joinToString("\n") {
            "${it.id};${it.titulo};${it.descricao};${it.dataHora};${it.concluida};${it.prioridade};${it.categoria}"
        }
        arquivo.writeText(conteudo)
    }

    fun carregar(): MutableList<Tarefa> {
        if (!arquivo.exists()) return mutableListOf()

        return arquivo.readLines().map {
            val partes = it.split(";")
            Tarefa(
                partes[0].toInt(),
                partes[1],
                partes[2],
                LocalDateTime.parse(partes[3]),
                partes[4].toBoolean(),
                partes[5].toInt(),
                partes[6]
            )
        }.toMutableList()
    }
}