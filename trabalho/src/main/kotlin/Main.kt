import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

fun main() {

    val gerenciador = GerenciadorTarefas()
    val notificacao = ServicoNotificacao()
    val armazenamento = Armazenamento()

    val formatador = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")

    gerenciador.obterTodasTarefas().addAll(armazenamento.carregar())

    while (true) {
        println("1 Adicionar")
        println("2 Listar dia")
        println("3 Listar semana")
        println("4 Atrasadas")
        println("5 Editar")
        println("6 Excluir")
        println("7 Concluir")
        println("8 Sair")

        when (readln().toInt()) {
            1 -> {
                println("Titulo:")
                val titulo = readln()
                println("Descricao:")
                val descricao = readln()
                println("Data (yyyy-MM-dd HH:mm):")
                val data = LocalDateTime.parse(readln(), formatador)
                println("Prioridade:")
                val prioridade = readln().toInt()
                println("Categoria:")
                val categoria = readln()

                gerenciador.adicionarTarefa(titulo, descricao, data, prioridade, categoria)
            }

            2 -> {
                val tarefas = gerenciador.obterTarefasDoDia(LocalDateTime.now())
                for (t in tarefas) {
                    println(t)
                }
            }

            3 -> {
                val tarefas = gerenciador.obterTarefasDaSemana()
                for (t in tarefas) {
                    println(t)
                }
            }

            4 -> {
                val tarefas = gerenciador.obterTarefasAtrasadas()
                for (t in tarefas) {
                    println(t)
                }
            }

            5 -> {
                println("ID:")
                val id = readln().toInt()
                println("Novo titulo:")
                val titulo = readln()
                println("Nova descricao:")
                val descricao = readln()
                println("Nova data:")
                val data = LocalDateTime.parse(readln(), formatador)
                println("Prioridade:")
                val prioridade = readln().toInt()
                println("Categoria:")
                val categoria = readln()

                gerenciador.editarTarefa(id, titulo, descricao, data, prioridade, categoria)
            }

            6 -> {
                println("ID:")
                val id = readln().toInt()
                gerenciador.removerTarefa(id)
            }

            7 -> {
                println("ID:")
                val id = readln().toInt()
                gerenciador.marcarComoConcluida(id)
            }

            8 -> {
                armazenamento.salvar(gerenciador.obterTodasTarefas())
                break
            }
        }

        notificacao.verificarNotificacoes(gerenciador.obterTodasTarefas())
    }
}