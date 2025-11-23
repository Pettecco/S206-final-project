Feature: Rodar o jogo end-to-end
  Para registrar partidas completas no sistema
  Como usuário do Ultimate Tic Tac Toe
  Quero iniciar, concluir e resetar um jogo corretamente

  Scenario: Fluxo completo de uma partida
    Given a aplicação está carregada com acesso ao banco
    When eu inicio o jogo
    Then o jogo deve começar
    And o jogo deve terminar automaticamente
    And o resultado deve estar salvo no banco
    When eu resetar o jogo
    Then os botões devem voltar ao estado inicial
