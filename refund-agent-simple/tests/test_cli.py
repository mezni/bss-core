from refund_agent_simple.cli import main


def test_cli_exits_on_quit(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "quit")

    main()

    assert "Refund Agent" in capsys.readouterr().out
