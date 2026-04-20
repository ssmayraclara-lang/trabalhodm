import java.time.LocalDateTime

class ServicoNotificacao {

    fun verificarNotificacoes(tarefas: List<Tarefa>) {
        val agora = LocalDateTime.now()

        for (tarefa in tarefas) {
            when {
                tarefa.dataHora.hour == agora.hour && tarefa.dataHora.minute == agora.minute -> {
                    println("Notificação: ${tarefa.titulo} agora")
                }
                tarefa.dataHora.isBefore(agora) && !tarefa.concluida -> {
                    println("Atrasada: ${tarefa.titulo}")
                }
            }
        }
    }
}