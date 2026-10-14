from main import main


def test_main(capsys):
    main()

    captured = capsys.readouterr()

    assert captured.out == ("CRM Agent - Contract and Add-on Retrieval\n")
